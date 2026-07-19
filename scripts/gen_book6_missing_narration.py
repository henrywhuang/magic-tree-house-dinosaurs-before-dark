#!/usr/bin/env python3
"""Generate missing Book 6 chapter narration with local Qwen3-TTS."""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from qwen_tts import Qwen3TTSModel

from generate_qwen3_word_audio import LOCAL_MODEL, MODEL_ID, encode_mp3, generate_batch, pick_device
from rebuild_book6 import SOURCE, chapter_text

ROOT = Path(__file__).resolve().parents[1]
INSTRUCT = "Read this children's story clearly and warmly in natural American English. Do not add or omit any words."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, choices=[9, 10], required=True)
    parser.add_argument('--device', default='auto', choices=['auto', 'mps', 'cpu', 'cuda:0'])
    parser.add_argument('--batch-size', type=int, default=4)
    parser.add_argument('--speaker', default='Aiden')
    parser.add_argument('--temperature', type=float, default=0.15)
    args = parser.parse_args()

    pages = json.loads(SOURCE.read_text(encoding='utf-8'))
    paragraphs = [line.strip() for line in chapter_text(pages, args.chapter - 1).splitlines() if line.strip()]
    output = ROOT / 'assets' / 'audio' / f'book-06-chapter-{args.chapter:02d}.mp3'
    device, dtype = pick_device(args.device)
    model_source = str(LOCAL_MODEL) if LOCAL_MODEL.exists() else MODEL_ID
    print(f'Loading {MODEL_ID} on {device} ({dtype}); paragraphs={len(paragraphs)}', flush=True)
    model = Qwen3TTSModel.from_pretrained(
        model_source, device_map=device, dtype=dtype, attn_implementation='sdpa'
    )

    audio, sample_rate = [], None
    for offset in range(0, len(paragraphs), args.batch_size):
        batch = paragraphs[offset:offset + args.batch_size]
        wavs, sample_rate = generate_batch(
            model, batch, args.speaker, 'English', INSTRUCT, 512, args.temperature
        )
        for wav in wavs:
            audio.append(np.asarray(wav, dtype=np.float32))
            audio.append(np.zeros(int(sample_rate * 0.22), dtype=np.float32))
        print(f'{min(offset + len(batch), len(paragraphs))}/{len(paragraphs)} paragraphs', flush=True)

    combined = np.concatenate(audio[:-1])
    encode_mp3(combined, sample_rate, output)
    print(f'Wrote {output.relative_to(ROOT)} ({len(combined) / sample_rate:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
