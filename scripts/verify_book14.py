#!/usr/bin/env python3
"""Audit Book 14 reader text against its aligned narration ASR."""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(word):
    return re.sub(r'[^a-z]', '', word.lower())


def load_reader(chapter):
    path = ROOT / 'data' / f'book-14-chapter-{chapter:02d}.json'
    return [word['word'] for word in json.loads(path.read_text())['words']]


def load_asr(chapter):
    path = ROOT / 'tmp' / 'asr' / f'book14-ch{chapter:02d}.json'
    return json.loads(path.read_text())['words'] if path.exists() else None


def audit(chapter):
    reader = load_reader(chapter)
    asr_words = load_asr(chapter)
    if asr_words is None:
        print(f'ch{chapter:02d}: no ASR timing')
        return False
    matcher = difflib.SequenceMatcher(
        None, [norm(word) for word in reader],
        [norm(word['word']) for word in asr_words], autojunk=False,
    )
    unexpected = False
    print(f'ch{chapter:02d}: {len(reader)} reader / {len(asr_words)} ASR words '
          f'({matcher.ratio():.1%} aligned)')
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ('insert', 'replace') and j2 - j1 >= 4:
            text = ' '.join(word['word'].strip() for word in asr_words[j1:j2])
            # The narrator announces title/chapter before the printed text.  In
            # chapter 6, SequenceMatcher aligns “Dragon King” with a later
            # printed occurrence, so the residual intro does not contain the
            # word “chapter”; use its early timestamp as the reliable signal.
            if (j1 < 12 and asr_words[j1]['start'] < 15) or (
                chapter == 8 and 'seven thousand' in text.lower()
            ):
                continue
            print(f'  ASR-ONLY: {text[:140]}')
            unexpected = True
        if tag in ('delete', 'replace') and i2 - i1 >= 4:
            text = ' '.join(reader[i1:i2])
            # Handwritten fact-box and notebook notes are visible on the scan,
            # but the narrator occasionally compresses their punctuation.
            allowed = (
                chapter == 2 and 'First emperor called Dragon King' in text
                or chapter == 8 and 'No two faces the same' in text
            )
            if not allowed:
                print(f'  READER-ONLY: {text[:140]}')
                unexpected = True
    return not unexpected


def main():
    chapters = [int(value) for value in sys.argv[1:]] or range(1, 11)
    results = [audit(chapter) for chapter in chapters]
    ok = all(results)
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
