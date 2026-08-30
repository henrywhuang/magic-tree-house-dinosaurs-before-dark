#!/usr/bin/env python3
"""Shared OCR-Word-doc chapter extractor for Books 13-16.

Each of these books ships a ~50KB text-only OCR Word doc (like Book 12).  This
module rebuilds clean paragraph-per-line chapter text: find each chapter heading
(number + title, body occurrence not the TOC), drop page numbers / watermark /
debris, join line wraps, straighten quotes.  A leading Prologue (series recap)
sits before the chapter-1 heading and is therefore excluded automatically — the
audiobook does not narrate it either.
"""
import glob
import os
import re
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[1]

PAGE_RE = re.compile(r'^\d{1,3}[฿·•]?$')
DEBRIS = {'THR', 'ER', '•THR', '฿', '·THR', 'THR•'}
WATERMARK_RE = re.compile(r'https?://\S+|youshengshu|taobao', re.I)


def find_docx(key):
    cands = [f for f in glob.glob(str(ROOT / '*.docx'))
             if key in os.path.basename(f) and 'Word' in os.path.basename(f)
             and 40000 < os.path.getsize(f) < 120000]
    if not cands:
        raise RuntimeError(f'No ~50KB Word doc for key {key!r}')
    return cands[0]


def full_text(docx_path):
    return '\n'.join(p.text for p in Document(docx_path).paragraphs)


def heading_pos(full, number, title):
    key = r'\s*'.join(re.escape(w) for w in title.split())
    pattern = re.compile(r'(?:^|\n)' + str(number) + r'\n\s*' + key + r'\s*\n')
    matches = list(pattern.finditer(full))
    if not matches:
        raise RuntimeError(f'Chapter {number} heading not found: {title}')
    return matches[-1].end(), matches[-1].start()


def chapter_spans(full, chapters):
    heads = [heading_pos(full, n, t) for n, t in chapters]
    spans = []
    for i, (body_start, _) in enumerate(heads):
        end = heads[i + 1][1] if i + 1 < len(heads) else len(full)
        spans.append((body_start, end))
    return spans


def clean_lines(segment):
    lines = []
    for raw in segment.split('\n'):
        line = raw.strip()
        if not line or PAGE_RE.match(line) or line in DEBRIS:
            continue
        if WATERMARK_RE.search(line):
            continue
        if len(re.sub(r'[^A-Za-z]', '', line)) == 0:
            continue
        if len(line) <= 3 and not re.search(r'[A-Za-z]{2}', line):
            continue
        line = re.sub(r'^\d{1,3}[฿·•]?\s*', '', line)
        lines.append(line)
    return lines


def fix_quotes(text):
    out, open_q = [], False
    for ch in text:
        if ch == '"':
            out.append('”' if open_q else '“')
            open_q = not open_q
        else:
            out.append(ch)
    text = ''.join(out)
    text = re.sub(r'“\s+', '“', text)
    text = re.sub(r'\s+”', '”', text)
    return text


def paragraphs(lines):
    paras = []
    for line in lines:
        starts = (not paras or line[:1] in '"“'
                  or (re.search(r'[.!?][)"”’]?$', paras[-1]) and line[:1].isupper()))
        if starts:
            paras.append(line)
        elif paras[-1].endswith('-'):
            paras[-1] = paras[-1][:-1] + line
        else:
            paras[-1] += ' ' + line
    cleaned = []
    for para in paras:
        para = fix_quotes(para)
        para = re.sub(r'\s+([,.;:!?])', r'\1', para)
        para = re.sub(r"(\w)['’]\s+(s|t|ll|ve|re|d|m)\b", r"\1’\2", para)
        para = para.replace('TIl', 'I’ll').replace('T ll', 'I’ll')
        para = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '’', para)
        para = re.sub(r'\s{2,}', ' ', para).strip()
        if para:
            cleaned.append(para)
    return cleaned


class BookText:
    """Bind the extractor to one book's docx + chapter list."""

    def __init__(self, docx_key, chapters):
        self.docx_key = docx_key
        self.chapters = chapters
        self.TITLES = [t for _, t in chapters]

    def _spans(self):
        full = full_text(find_docx(self.docx_key))
        return full, chapter_spans(full, self.chapters)

    def chapter_paragraphs(self, chapter_index):
        full, spans = self._spans()
        lo, hi = spans[chapter_index]
        return paragraphs(clean_lines(full[lo:hi]))

    def chapter_text(self, chapter_index):
        return '\n'.join(self.chapter_paragraphs(chapter_index))

    def dump(self, out_dir):
        out = ROOT / 'tmp' / out_dir
        out.mkdir(parents=True, exist_ok=True)
        for i, (num, title) in enumerate(self.chapters):
            text = self.chapter_text(i)
            (out / f'ch{num:02d}.txt').write_text(text, encoding='utf-8')
            print(f'ch{num:02d} "{title}": {len(text.split())} words, {text.count(chr(10)) + 1} paras')
