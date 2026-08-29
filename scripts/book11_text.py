#!/usr/bin/env python3
"""Book 11 (Lions at Lunchtime) story text extractor.

Book 11 has no bilingual PaddleOCR workbook JSON like Books 1-10; its source is
the scanned English PDF whose half-page OCR lives in work_book11/ocr_halves/.
This module rebuilds clean, paragraph-per-line chapter text from those halves,
reusing the wrap-joining logic from work_book11/build_word.py so the reader
pipeline (rebuild_book11.py) can consume it in place of `pages[i]['markdown']`.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / 'work_book11' / 'ocr_halves'

# Authoritative chapter heads: printed source page -> (chapter number, title).
CHAPTERS = {
    68: (1, 'Before Lunch'),
    75: (2, 'Jump, Beasts! Jump!'),
    82: (3, 'Disaster'),
    87: (4, 'Mud Bath'),
    93: (5, 'Ha-Ha'),
    99: (6, 'Spick-and-Span'),
    105: (7, 'Hi, There'),
    113: (8, 'Yum'),
    120: (9, 'Tiptoe'),
    128: (10, 'After Lunch'),
}
FIRST_PAGE = 68
LAST_PAGE = 131  # build_word.py iterates 64 half-pages: source pages 68..131.

TITLES = [title for _, (num, title) in sorted(CHAPTERS.items())]
CHAPTER_START_PAGES = [page for page, _ in sorted(CHAPTERS.items())]


def normalize_ocr(raw: str, source_page: int) -> list[str]:
    raw = raw.replace('­', '').replace('’ Il', '’ll').replace('I’ Il', 'I’ll')
    raw = raw.replace('I’ ve', 'I’ve').replace('we’ ve', 'we’ve').replace('they’ re', 'they’re')
    raw = raw.replace('don’ t', 'don’t').replace('couldn’ t', 'couldn’t').replace('didn’ t', 'didn’t')
    raw = raw.replace('wasn’ t', 'wasn’t').replace('aren’ t', 'aren’t').replace('there’ s', 'there’s')
    raw = raw.replace('Jack’ s', 'Jack’s').replace('Morgan’ s', 'Morgan’s')
    lines = raw.splitlines()
    cleaned = []
    for line in lines:
        line = line.replace('|', ' ').strip()
        line = re.sub(r'\s{2,}', ' ', line)
        if not line:
            cleaned.append('')
            continue
        if line == str(source_page):
            continue
        if re.fullmatch(r"[_~=<>«»—–\-.,;:'\"`*+\s]+", line):
            continue
        if '---__' in line:
            line = line.split('---__', 1)[0].rstrip()
        if '___' in line:
            line = line.split('___', 1)[0].rstrip()
        if not line or '= WR' in line:
            continue
        if len(re.sub(r'\W', '', line)) == 0:
            continue
        cleaned.append(line)

    if source_page in CHAPTERS:
        num, title = CHAPTERS[source_page]
        skip = {str(num), title, title.replace(', ', ','), title.replace(' ', '')}
        cleaned = [x for x in cleaned if x not in skip]

    blocks = []
    current = []
    for line in cleaned + ['']:
        if line:
            current.append(line)
            continue
        if not current:
            continue
        text = current[0]
        for nxt in current[1:]:
            if text.endswith('-') and nxt and nxt[0].islower():
                text = text[:-1] + nxt
            else:
                text += ' ' + nxt
        text = re.sub(r'\s+([,.;:!?])', r'\1', text)
        text = re.sub(r'([.!?])([A-Z“])', r'\1 \2', text)
        text = re.sub(r'\s{2,}', ' ', text).strip()
        if text:
            blocks.append(text)
        current = []
    merged = []
    for block in blocks:
        if merged and block and block[0].islower() and not re.search(r'[.!?][”’\"]?$', merged[-1]):
            if merged[-1].endswith('-'):
                merged[-1] = merged[-1][:-1] + block
            else:
                merged[-1] += ' ' + block
        else:
            merged.append(block)
    return merged


def page_paragraphs(source_page: int) -> list[str]:
    offset = source_page - FIRST_PAGE
    pdf_page = offset // 2 + 1
    side = 'L' if offset % 2 == 0 else 'R'
    ocr_file = OCR_DIR / f'page-{pdf_page:02}-{side}.txt'
    raw = ocr_file.read_text(encoding='utf-8', errors='ignore')
    return normalize_ocr(raw, source_page)


def chapter_paragraphs(chapter_index: int) -> list[str]:
    lo = CHAPTER_START_PAGES[chapter_index]
    hi = CHAPTER_START_PAGES[chapter_index + 1] if chapter_index < 9 else LAST_PAGE + 1
    paragraphs = []
    for source_page in range(lo, hi):
        paragraphs.extend(page_paragraphs(source_page))
    # Join wraps that span the page turn (lowercase continuation of an open sentence).
    merged = []
    for para in paragraphs:
        if merged and para and para[0].islower() and not re.search(r'[.!?][”’\"]?$', merged[-1]):
            if merged[-1].endswith('-'):
                merged[-1] = merged[-1][:-1] + para
            else:
                merged[-1] += ' ' + para
        else:
            merged.append(para)
    return merged


def chapter_text(chapter_index: int) -> str:
    return '\n'.join(chapter_paragraphs(chapter_index))


if __name__ == '__main__':
    out = ROOT / 'tmp' / 'book11_text'
    out.mkdir(parents=True, exist_ok=True)
    for i in range(10):
        text = chapter_text(i)
        (out / f'ch{i + 1:02d}.txt').write_text(text, encoding='utf-8')
        print(f'ch{i + 1:02d} "{TITLES[i]}": {len(text.split())} words, {text.count(chr(10)) + 1} paragraphs')
