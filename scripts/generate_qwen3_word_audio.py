#!/usr/bin/env python3
"""Generate one MP3 per H5 dictionary word with Alibaba Qwen3-TTS.

Voice config (per product decision 2026-07-14):
  * temperature = 0  -> deterministic greedy decoding (do_sample=False), no random
    prosody drift and no run-on "rambling" clips.
  * instruct = "念单词不要有情绪" -> flat, emotionless citation reading. The installed
    qwen-tts library silently drops `instruct` for the 0.6B CustomVoice model, so we
    build the instruct tokens ourselves and call `model.model.generate(...)` directly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


ROOT = Path(__file__).resolve().parents[1]
WORDS_JS = ROOT / "data" / "words.js"
CHAPTER_PATTERNS = ("chapter-*.json", "book-02-chapter-*.json", "vocabulary-*.json")
OUTPUT_DIR = ROOT / "assets" / "audio" / "words"
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
LOCAL_MODEL = ROOT / ".models" / "Qwen3-TTS-12Hz-0.6B-CustomVoice"
SPEAKER = "Aiden"                    # English-native timbre (also available: Ryan)
INSTRUCT = "Read this English word clearly in a flat, neutral tone with no emotion."  # emotionless single-word reading
TEMPERATURE = 0.15                   # low-temperature sampling (0 = greedy)


def load_words() -> list[str]:
    """Load every clickable story token, plus dictionary entries used by word cards."""
    raw = WORDS_JS.read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.WORDS=(.*);\s*", raw, re.S)
    if not match:
        raise RuntimeError(f"Cannot parse {WORDS_JS}")
    data = json.loads(match.group(1))
    words = {w.lower() for w in data if re.fullmatch(r"[a-z]+(?:['-][a-z]+)*", w)}
    for pattern in CHAPTER_PATTERNS:
        for chapter_path in sorted((ROOT / "data").glob(pattern)):
            chapter = json.loads(chapter_path.read_text(encoding="utf-8"))
            for item in chapter.get("words", []):
                word = re.sub(r"[^A-Za-z'-]", "", item.get("word", "")).lower()
                if re.fullmatch(r"[a-z]+(?:['-][a-z]+)*", word):
                    words.add(word)
    return sorted(words)


def output_path(word: str) -> Path:
    return OUTPUT_DIR / f"{word}.mp3"


def pick_device(requested: str) -> tuple[str, torch.dtype]:
    if requested != "auto":
        return requested, torch.float32 if requested in {"cpu", "mps"} else torch.float16
    if torch.backends.mps.is_available():
        # Qwen3-TTS code-predictor sampling can produce NaNs with fp16 on MPS.
        return "mps", torch.float32
    if torch.cuda.is_available():
        return "cuda:0", torch.bfloat16
    return "cpu", torch.float32


def generate_batch(model, texts, speaker, language, instruct, max_new_tokens, temperature):
    """Greedy (temperature=0) CustomVoice generation that KEEPS the instruct.

    The library's `generate_custom_voice` forces `instruct=None` for the 0.6B model
    (see qwen_tts/inference/qwen3_tts_model.py: ``if tts_model_size in "0b6"``), which
    disables emotion control. We replicate its flow but feed the instruct tokens through.
    """
    languages = [language] * len(texts)
    speakers = [speaker] * len(texts)
    model._validate_languages(languages)
    model._validate_speakers(speakers)
    input_ids = model._tokenize_texts([model._build_assistant_text(t) for t in texts])
    if instruct:
        instruct_ids = [model._tokenize_texts([model._build_instruct_text(instruct)])[0] for _ in texts]
    else:
        instruct_ids = [None] * len(texts)
    if temperature and temperature > 0:
        sampling = dict(do_sample=True, temperature=temperature, top_p=0.9, top_k=50, repetition_penalty=1.05)
    else:
        sampling = dict(do_sample=False)
    gen_kwargs = model._merge_generate_kwargs(max_new_tokens=max_new_tokens, **sampling)
    codes, _ = model.model.generate(
        input_ids=input_ids,
        instruct_ids=instruct_ids,
        languages=languages,
        speakers=speakers,
        non_streaming_mode=True,
        **gen_kwargs,
    )
    wavs, fs = model.model.speech_tokenizer.decode([{"audio_codes": c} for c in codes])
    return wavs, fs


def encode_mp3(wav: np.ndarray, sample_rate: int, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
        wav_path = Path(temp.name)
    try:
        sf.write(wav_path, wav, sample_rate, subtype="PCM_16")
        # Trim silence on BOTH ends (leading, then trailing via reverse), gently
        # normalise loudness, and add a tiny tail pad. Thresholds are kept mild so
        # English onsets/fricatives (e.g. the /s/ in "castle") are not clipped.
        audio_filter = (
            "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,"
            "areverse,"
            "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB,"
            "areverse,"
            "dynaudnorm=f=150:g=15,"
            "apad=pad_dur=0.06"
        )
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(wav_path),
                "-af", audio_filter,
                "-codec:a", "libmp3lame", "-b:a", "64k", "-ar", "24000", "-ac", "1", str(destination),
            ],
            check=True,
        )
    finally:
        wav_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Only generate first N pending words")
    parser.add_argument("--words", nargs="*", help="Generate only these words")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", default="auto", choices=["auto", "mps", "cpu", "cuda:0"])
    parser.add_argument("--speaker", default=SPEAKER)
    parser.add_argument("--instruct", default=INSTRUCT, help='Style instruction; "" disables it')
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=TEMPERATURE, help="0 = greedy; low values (e.g. 0.15) stay stable")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source_words = load_words()
    words = [w.lower() for w in args.words] if args.words else source_words
    pending = [w for w in words if args.overwrite or not output_path(w).exists()]
    if args.limit:
        pending = pending[: args.limit]
    if not pending:
        print("No pending words.")
        return

    device, dtype = pick_device(args.device)
    print(f"Loading {MODEL_ID} on {device} ({dtype}); pending={len(pending)}", flush=True)
    print(f"config: speaker={args.speaker} temperature={args.temperature} instruct={args.instruct!r}", flush=True)
    model_source = str(LOCAL_MODEL) if LOCAL_MODEL.exists() else MODEL_ID
    model = Qwen3TTSModel.from_pretrained(
        model_source,
        device_map=device,
        dtype=dtype,
        attn_implementation="sdpa",
    )
    print("Speakers:", model.get_supported_speakers(), flush=True)

    generated = 0
    started = time.time()
    for offset in range(0, len(pending), args.batch_size):
        batch = pending[offset : offset + args.batch_size]
        # A short sentence boundary helps the model make a complete, clean word clip.
        texts = [f"{word}." for word in batch]
        wavs, sample_rate = generate_batch(
            model, texts, args.speaker, "English", args.instruct, args.max_new_tokens, args.temperature
        )
        for word, wav in zip(batch, wavs):
            encode_mp3(np.asarray(wav), sample_rate, output_path(word))
            generated += 1
        elapsed = time.time() - started
        rate = generated / elapsed if elapsed else 0
        print(f"{generated}/{len(pending)} | {', '.join(batch)} | {rate:.2f} words/s", flush=True)

    manifest = {
        "model": MODEL_ID,
        "speaker": args.speaker,
        "language": "English",
        "sampling": (f"temperature={args.temperature}" if args.temperature else "greedy(temperature=0)"),
        "instruct": args.instruct,
        "format": "mp3/24kHz/mono/64kbps",
        "source_word_count": len(source_words),
        "count": len(list(OUTPUT_DIR.glob("*.mp3"))),
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
