#!/usr/bin/env python3
"""Generate one MP3 per H5 dictionary word with Alibaba Qwen3-TTS."""

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
OUTPUT_DIR = ROOT / "assets" / "audio" / "words"
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
LOCAL_MODEL = ROOT / ".models" / "Qwen3-TTS-12Hz-0.6B-CustomVoice"


def load_words() -> list[str]:
    raw = WORDS_JS.read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.WORDS=(.*);\s*", raw, re.S)
    if not match:
        raise RuntimeError(f"Cannot parse {WORDS_JS}")
    data = json.loads(match.group(1))
    return sorted(w for w in data if re.fullmatch(r"[a-z]+(?:['-][a-z]+)*", w))


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


def encode_mp3(wav: np.ndarray, sample_rate: int, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
        wav_path = Path(temp.name)
    try:
        sf.write(wav_path, wav, sample_rate, subtype="PCM_16")
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(wav_path),
                # Only trim leading silence. Cutting at the first quiet interval can
                # destroy English fricatives and internal consonant transitions.
                "-af", "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-50dB,apad=pad_dur=0.10",
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
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    words = [w.lower() for w in args.words] if args.words else load_words()
    pending = [w for w in words if args.overwrite or not output_path(w).exists()]
    if args.limit:
        pending = pending[: args.limit]
    if not pending:
        print("No pending words.")
        return

    device, dtype = pick_device(args.device)
    print(f"Loading {MODEL_ID} on {device} ({dtype}); pending={len(pending)}", flush=True)
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
        wavs, sample_rate = model.generate_custom_voice(
            text=texts,
            language=["English"] * len(batch),
            speaker=["Aiden"] * len(batch),
            instruct=[""] * len(batch),
            # 12 Hz codec: 48 tokens cap each isolated word at roughly 4 seconds
            # and prevents rare non-terminating samples from stalling a batch.
            max_new_tokens=48,
        )
        for word, wav in zip(batch, wavs):
            encode_mp3(np.asarray(wav), sample_rate, output_path(word))
            generated += 1
        elapsed = time.time() - started
        rate = generated / elapsed if elapsed else 0
        print(f"{generated}/{len(pending)} | {', '.join(batch)} | {rate:.2f} words/s", flush=True)

    manifest = {
        "model": MODEL_ID,
        "speaker": "Aiden",
        "language": "English",
        "format": "mp3/24kHz/mono/64kbps",
        "count": len(list(OUTPUT_DIR.glob("*.mp3"))),
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
