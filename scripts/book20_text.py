#!/usr/bin/env python3
"""Book 20 (Dingoes at Dinnertime) chapter text.

The only Word/PDF copies of this book are a garbled listener's transcript, so
the text is proofread from a whisper-large-v3-turbo transcript of the
unabridged audiobook (read by the author) and kept in book20_source.txt:
one paragraph per line, chapters introduced by `## <n> <title>`.
"""
import re
from pathlib import Path

SOURCE = Path(__file__).resolve().with_name('book20_source.txt')
CHAPTERS = [(1, 'The Last Gift'), (2, 'Sleepyhead'), (3, 'Big Foot'), (4, 'Joey'), (5, 'Wildfire'),
            (6, 'Hand to Hand'), (7, 'Rain, Rain, Rain'), (8, 'The Rainbow Serpent'),
            (9, 'What Boy?'), (10, 'Dreamtime')]
TITLES = [t for _, t in CHAPTERS]


def _chapters():
    blocks = re.split(r'^## \d+ .*$', SOURCE.read_text(encoding='utf-8'), flags=re.M)[1:]
    if len(blocks) != len(CHAPTERS):
        raise RuntimeError(f'{SOURCE.name}: expected {len(CHAPTERS)} chapters, found {len(blocks)}')
    return [[line.strip() for line in block.splitlines() if line.strip()] for block in blocks]


def chapter_paragraphs(chapter_index):
    return _chapters()[chapter_index]


def chapter_text(chapter_index):
    return '\n'.join(chapter_paragraphs(chapter_index))


if __name__ == '__main__':
    out = Path(__file__).resolve().parents[1] / 'tmp' / 'book20_text'
    out.mkdir(parents=True, exist_ok=True)
    for i, (num, title) in enumerate(CHAPTERS):
        text = chapter_text(i)
        (out / f'ch{num:02d}.txt').write_text(text, encoding='utf-8')
        print(f'ch{num:02d} "{title}": {len(text.split())} words, {text.count(chr(10)) + 1} paras')
