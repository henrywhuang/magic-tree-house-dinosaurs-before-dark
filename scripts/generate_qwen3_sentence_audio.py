#!/usr/bin/env python3
"""Generate the vocabulary demo's full-sentence audio with local Qwen3-TTS."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from qwen_tts import Qwen3TTSModel

from generate_qwen3_word_audio import (
    LOCAL_MODEL,
    MODEL_ID,
    SPEAKER,
    encode_mp3,
    generate_batch,
    pick_device,
)


ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / "data" / "vocabulary-book-02-chapter-01.json"
INSTRUCT = "Read this English story sentence clearly and naturally for a child learning English."


def load_items() -> list[tuple[str, str, Path]]:
    data = json.loads(VOCABULARY.read_text(encoding="utf-8"))
    return [
        (item["id"], item["sentence"], ROOT / item["sentenceAudio"])
        for item in data["words"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="auto", choices=["auto", "mps", "cpu", "cuda:0"])
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--temperature", type=float, default=0.15)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--ids", nargs="*", help="Only generate selected vocabulary IDs")
    args = parser.parse_args()

    items = load_items()
    if args.ids:
        selected = set(args.ids)
        items = [item for item in items if item[0] in selected]
    pending = [item for item in items if args.overwrite or not item[2].exists()]
    if not pending:
        print("No pending sentences.")
        return

    device, dtype = pick_device(args.device)
    source = str(LOCAL_MODEL) if LOCAL_MODEL.exists() else MODEL_ID
    print(f"Loading {MODEL_ID} on {device} ({dtype}); pending={len(pending)}", flush=True)
    model = Qwen3TTSModel.from_pretrained(
        source,
        device_map=device,
        dtype=dtype,
        attn_implementation="sdpa",
    )

    started = time.time()
    generated = 0
    for offset in range(0, len(pending), args.batch_size):
        batch = pending[offset : offset + args.batch_size]
        texts = [sentence for _, sentence, _ in batch]
        wavs, sample_rate = generate_batch(
            model,
            texts,
            SPEAKER,
            "English",
            INSTRUCT,
            384,
            args.temperature,
        )
        for (item_id, _, destination), wav in zip(batch, wavs):
            encode_mp3(np.asarray(wav), sample_rate, destination)
            generated += 1
            print(f"{generated}/{len(pending)} | {item_id} -> {destination.relative_to(ROOT)}", flush=True)

    print(f"Completed {generated} sentence clips in {time.time() - started:.1f}s", flush=True)


if __name__ == "__main__":
    main()
