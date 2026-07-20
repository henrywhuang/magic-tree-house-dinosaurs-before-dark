#!/usr/bin/env python3
"""Transcribe Book 9 chapter audio to word-level timestamps."""
import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser()
parser.add_argument('--chapter', type=int, choices=range(1, 11))
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tmp' / 'asr'
OUT.mkdir(parents=True, exist_ok=True)
model = WhisperModel('large-v3', device='cpu', compute_type='int8')

chapters = [args.chapter] if args.chapter else range(1, 11)
for chapter in chapters:
    source = ROOT / 'assets' / 'audio' / f'book-09-chapter-{chapter:02d}.mp3'
    if not source.exists():
        print(f'skip missing {source.name}', flush=True)
        continue
    target = OUT / f'book9-ch{chapter:02d}.json'
    segments, info = model.transcribe(
        str(source), language='en', word_timestamps=True,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
        beam_size=5, temperature=[0.0, 0.2, 0.4, 0.6],
        condition_on_previous_text=False, compression_ratio_threshold=2.2,
        initial_prompt='A chapter from Magic Tree House: Dolphins at Daybreak, American English narration.',
    )
    words = [
        {'word': word.word, 'start': round(word.start, 3), 'end': round(word.end, 3),
         'prob': round(word.probability, 3)}
        for segment in segments for word in (segment.words or [])
    ]
    target.write_text(json.dumps({'duration': round(info.duration, 2), 'words': words}, indent=1), encoding='utf-8')
    print(f'{target.name}: {len(words)} words, {info.duration:.1f}s', flush=True)
