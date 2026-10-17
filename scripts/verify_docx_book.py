#!/usr/bin/env python3
"""Narration-gap audit for a docx-sourced book. Flags ASR runs (>=5 words, >=1.5s,
starting after 3s so chapter-title announcements are skipped) with no OCR match.
Usage: verify_docx_book.py <book>"""
import difflib, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
book = int(sys.argv[1])
def norm(w): return re.sub(r'[^a-z]', '', w.lower())
flagged = 0
for c in range(1, 11):
    dp = ROOT / f'data/book-{book:02d}-chapter-{c:02d}.json'
    ap = ROOT / f'tmp/asr/book{book}-ch{c:02d}.json'
    if not ap.exists(): 
        print(f'ch{c:02d}: no ASR'); continue
    ocr = [norm(w['word']) for w in json.loads(dp.read_text())['words']]
    asr = json.loads(ap.read_text())['words']; asrn = [norm(w['word']) for w in asr]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ocr, asrn, autojunk=False).get_opcodes():
        if tag in ('insert', 'replace') and j2 - j1 >= 5:
            span = asr[j2-1]['end'] - asr[j1]['start']
            if span >= 1.5 and asr[j1]['start'] > 3:
                txt = ' '.join(x['word'].strip() for x in asr[j1:j2])[:90]
                print(f'  ch{c:02d} ASR-ONLY @{asr[j1]["start"]:.0f}s (+{span:.0f}s): {txt}')
                flagged += 1
print(f'book{book}: {flagged} gap(s) flagged')
