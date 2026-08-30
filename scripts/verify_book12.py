#!/usr/bin/env python3
"""Narration-gap audit for Book 11: align each chapter's reader text against its
ASR and report (1) ASR runs with no OCR match = narration the printed text is
missing, (2) OCR runs with no ASR match = text with no spoken counterpart
(art/hallucination). Only chapters whose audio is present are checked."""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(word):
    return re.sub(r'[^a-z]', '', word.lower())


def load_ocr(chapter):
    data = json.loads((ROOT / f'data/book-12-chapter-{chapter:02d}.json').read_text())
    return [w['word'] for w in data['words']]


def load_asr(chapter):
    path = ROOT / 'tmp' / 'asr' / f'book12-ch{chapter:02d}.json'
    if not path.exists():
        return None
    return json.loads(path.read_text())['words']


def audit(chapter):
    ocr = load_ocr(chapter)
    asr_words = load_asr(chapter)
    if asr_words is None:
        print(f'ch{chapter:02d}: no audio (skip)')
        return
    ocr_n = [norm(w) for w in ocr]
    asr_n = [norm(w['word']) for w in asr_words]
    matcher = difflib.SequenceMatcher(None, ocr_n, asr_n, autojunk=False)
    asr_only, ocr_only = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ('insert', 'replace') and j2 - j1 >= 4:
            span = asr_words[j2 - 1]['end'] - asr_words[j1]['start']
            text = ' '.join(w['word'].strip() for w in asr_words[j1:j2])
            if span >= 1.2:
                asr_only.append((round(asr_words[j1]['start'], 1), round(span, 1), text))
        if tag in ('delete', 'replace') and i2 - i1 >= 4:
            ocr_only.append(' '.join(ocr[i1:i2]))
    print(f'ch{chapter:02d}: {len(ocr)} OCR / {len(asr_words)} ASR words')
    for start, span, text in asr_only:
        print(f'   ASR-ONLY @{start}s (+{span}s): {text[:110]}')
    for text in ocr_only:
        print(f'   OCR-ONLY: {text[:110]}')


def main():
    chapters = [int(x) for x in sys.argv[1:]] or range(1, 11)
    for chapter in chapters:
        audit(chapter)


if __name__ == '__main__':
    main()
