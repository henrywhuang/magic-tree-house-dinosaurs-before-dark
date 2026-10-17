#!/usr/bin/env python3
"""Fast timing-only ASR for Books 13-16: small.en, model loaded once, skips
chapters that already have output. ASR is used purely as timing anchors aligned
to the authoritative OCR text (difflib in rebuild), so small.en is ample."""
import json
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tmp' / 'asr'
OUT.mkdir(parents=True, exist_ok=True)
TITLES = {13: 'Vacation Under the Volcano', 14: 'Day of the Dragon King',
          15: 'Viking Ships at Sunrise', 16: 'Hour of the Olympics'}
model = WhisperModel('small.en', device='cpu', compute_type='int8')

for book in (13, 14, 15, 16):
    for chapter in range(1, 11):
        target = OUT / f'book{book}-ch{chapter:02d}.json'
        if target.exists():
            print(f'skip existing {target.name}', flush=True)
            continue
        source = ROOT / 'assets' / 'audio' / f'book-{book}-chapter-{chapter:02d}.mp3'
        if not source.exists():
            print(f'skip missing {source.name}', flush=True)
            continue
        segments, info = model.transcribe(
            str(source), language='en', word_timestamps=True,
            vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
            beam_size=1, temperature=[0.0, 0.2, 0.4, 0.6],
            condition_on_previous_text=False, compression_ratio_threshold=2.2,
            initial_prompt=f'A chapter from Magic Tree House: {TITLES[book]}, American English narration.',
        )
        words = [
            {'word': w.word, 'start': round(w.start, 3), 'end': round(w.end, 3), 'prob': round(w.probability, 3)}
            for seg in segments for w in (seg.words or [])
        ]
        target.write_text(json.dumps({'duration': round(info.duration, 2), 'words': words}, indent=1), encoding='utf-8')
        print(f'{target.name}: {len(words)} words, {info.duration:.1f}s', flush=True)
print('ALL DONE', flush=True)
