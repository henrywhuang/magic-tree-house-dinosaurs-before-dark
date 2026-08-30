#!/usr/bin/env python3
"""Audit Book 13 reader text against its aligned narration ASR.

Reports long narration-only runs (missing printed text) and reader-only runs
(OCR debris or text absent from the supplied narration). Chapter-title intros
are expected narration-only runs.
"""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(word):
    return re.sub(r'[^a-z]', '', word.lower())


def load_reader(chapter):
    path = ROOT / 'data' / f'book-13-chapter-{chapter:02d}.json'
    return [word['word'] for word in json.loads(path.read_text())['words']]


def load_asr(chapter):
    path = ROOT / 'tmp' / 'asr' / f'book13-ch{chapter:02d}.json'
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
            # Every track begins with its book/chapter announcement.
            if j1 == 0 and ('chapter' in text.lower() or chapter == 3):
                continue
            print(f'  ASR-ONLY: {text[:140]}')
            unexpected = True
        if tag in ('delete', 'replace') and i2 - i1 >= 4:
            text = ' '.join(reader[i1:i2])
            # The chapter-9 ASR says "They He leaped" while the scan correctly
            # reads "They jumped ... They leaped"; retain the printed sentence.
            if chapter == 9 and text == 'jumped over fallen branches They':
                continue
            print(f'  READER-ONLY: {text[:140]}')
            unexpected = True
    return not unexpected


def main():
    chapters = [int(value) for value in sys.argv[1:]] or range(1, 11)
    ok = all(audit(chapter) for chapter in chapters)
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
