#!/usr/bin/env python3
"""Book 12 (Polar Bears Past Bedtime) story text extractor.

Source is the supplied OCR Word doc (text only, no scans).  The doc is one long
line-wrapped OCR stream with page numbers and debris mixed in and no paragraph
delimiters, so this rebuilds clean paragraph-per-line chapter text: locate each
chapter heading (number + title), drop page numbers / OCR debris, join wraps, and
re-break paragraphs at sentence boundaries / dialogue turns.
"""
import re
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'Book 12_ Polar Bears Past Bedtime-()--_Word版.docx'

# (number, title) — titles as they appear in the chapter heading.
CHAPTERS = [
    (1, 'Are You Serious?'), (2, 'The Howling'), (3, 'Mush!'), (4, 'Snow House'),
    (5, "You're It!"), (6, 'Flying Bears'), (7, 'Spirit Lights'), (8, 'Riddle Solved'),
    (9, 'Oh, No, One More!'), (10, 'Master Librarians'),
]
TITLES = [title for _, title in CHAPTERS]


def _full_text():
    doc = Document(DOCX)
    return '\n'.join(p.text for p in doc.paragraphs)


def _heading_pos(full, number, title):
    """Position of the chapter heading (the story-body occurrence, not the TOC)."""
    key = r'\s*'.join(re.escape(word) for word in title.split())
    pattern = re.compile(r'\n' + str(number) + r'\n\s*' + key + r'\s*\n')
    matches = list(pattern.finditer(full))
    if not matches:
        raise RuntimeError(f'Chapter {number} heading not found: {title}')
    return matches[-1].end(), matches[-1].start()


def _chapter_spans(full):
    heads = [_heading_pos(full, n, t) for n, t in CHAPTERS]
    spans = []
    for index, (body_start, _head_start) in enumerate(heads):
        end = heads[index + 1][1] if index + 1 < len(heads) else len(full)
        spans.append((body_start, end))
    return spans


PAGE_RE = re.compile(r'^\d{1,3}[฿·•]?$')
DEBRIS = {'THR', 'ER', '•THR', '฿', '·THR', 'THR•', 'THE END'}


def _clean_lines(segment):
    lines = []
    for raw in segment.split('\n'):
        line = raw.strip()
        if not line:
            continue
        if PAGE_RE.match(line):
            continue
        if line in DEBRIS:
            continue
        # OCR debris: a token with no letters, or an isolated 1-3 char non-word blob.
        if len(re.sub(r'[^A-Za-z]', '', line)) == 0:
            continue
        if len(line) <= 3 and not re.search(r'[A-Za-z]{2}', line):
            continue
        # A page number fused to the next line, e.g. "130฿Jack saw" or "86 The".
        line = re.sub(r'^\d{1,3}[฿·•]?\s*', '', line)
        lines.append(line)
    return lines


def _paragraphs(lines):
    paras = []
    for line in lines:
        starts_para = (
            not paras
            or line[:1] in '"“'                       # a new dialogue turn
            or (re.search(r'[.!?][)"”’]?$', paras[-1]) and line[:1].isupper())
        )
        if starts_para:
            paras.append(line)
        elif paras[-1].endswith('-'):
            paras[-1] = paras[-1][:-1] + line
        else:
            paras[-1] += ' ' + line
    cleaned = []
    for para in paras:
        para = _fix_quotes(para)
        para = re.sub(r'\s+([,.;:!?])', r'\1', para)
        # OCR splits contraction apostrophes: "Morgan' s" / "don' t" / "I' ll".
        para = re.sub(r"(\w)['’]\s+(s|t|ll|ve|re|d|m)\b", r"\1’\2", para)
        para = para.replace('TIl', 'I’ll').replace('T ll', 'I’ll').replace('Tll', 'I’ll')
        para = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '’', para)
        para = re.sub(r'\s{2,}', ' ', para).strip()
        if para:
            cleaned.append(para)
    return cleaned


def _fix_quotes(text):
    out, open_q = [], False
    for ch in text:
        if ch == '"':
            out.append('”' if open_q else '“')
            open_q = not open_q
        else:
            out.append(ch)
    text = ''.join(out)
    text = re.sub(r'“\s+', '“', text)   # no space after an opening quote
    text = re.sub(r'\s+”', '”', text)   # no space before a closing quote
    return text


def chapter_paragraphs(chapter_index):
    full = _full_text()
    body_start, body_end = _chapter_spans(full)[chapter_index]
    return _paragraphs(_clean_lines(full[body_start:body_end]))


def chapter_text(chapter_index):
    return '\n'.join(chapter_paragraphs(chapter_index))


if __name__ == '__main__':
    out = ROOT / 'tmp' / 'book12_text'
    out.mkdir(parents=True, exist_ok=True)
    full = _full_text()
    for index, (number, title) in enumerate(CHAPTERS):
        text = chapter_text(index)
        (out / f'ch{number:02d}.txt').write_text(text, encoding='utf-8')
        print(f'ch{number:02d} "{title}": {len(text.split())} words, {text.count(chr(10)) + 1} paras')
