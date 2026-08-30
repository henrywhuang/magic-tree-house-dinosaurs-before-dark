#!/usr/bin/env python3
"""Generic reader-JSON builder for the docx-sourced books (13-16).

Same Book 7 base engine as everything else; parameterised by book number, its
text module (bookNN_text), content module (bookNN_content) and a per-book FIXES
dict (OCR-debris cleanup + narration back-fills recovered from the audio).
"""
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base


def _cleanup(text):
    text = re.sub(r'([a-z,])\.([A-Z])', r'\1. \2', text)   # missing space after a period
    text = re.sub(r'[ \t]+”', '”', text)
    text = re.sub(r'“\s+', '“', text)
    text = text.replace('…', '...')
    return text


def _synth(words, spw=0.36):
    t = 0.0
    for w in words:
        w['start'] = round(t, 3)
        w['end'] = round(t + spw * 0.85, 3)
        t += spw


def run(book, fixes):
    bt = importlib.import_module(f'book{book}_text')
    content = importlib.import_module(f'book{book}_content')
    base.TITLES = content.TITLES
    base.SCENE_ANCHORS = content.SCENE_ANCHORS
    base.SCENES = content.SCENES
    base.VOCABULARY = content.VOCABULARY

    def chapter_text(pages, chapter_index):
        text = bt.chapter_text(chapter_index)
        for old, new in fixes.get(chapter_index, []):
            if old in text:
                text = text.replace(old, new)
        return _cleanup(text).strip()

    base.chapter_text = chapter_text

    for ci in range(10):
        words, paragraphs = base.ocr_words(None, ci)
        asr_path = ROOT / 'tmp' / 'asr' / f'book{book}-ch{ci + 1:02d}.json'
        has_audio = asr_path.exists()
        if has_audio:
            base.assign_timestamps(words, json.loads(asr_path.read_text())['words'])
        else:
            _synth(words)
        standard, extension = base.extract_vocab(None, ci)
        base.apply_keywords(words, standard + extension)
        first, second = base.scene_boundaries(paragraphs, ci)
        for w in words:
            w['page'] = 0 if w['para'] < first else 1 if w['para'] < second else 2
        flat = [
            {'i': i, 'word': w['word'], 'before': w['before'], 'after': w['after'],
             'start': w['start'], 'end': w['end'], 'key': w['key'], 'page': w['page']}
            for i, w in enumerate(words)
        ]
        pages_out = []
        for page in range(3):
            grouped = {}
            for i, w in enumerate(words):
                if w['page'] == page:
                    grouped.setdefault(w['para'], []).append(flat[i])
            pages_out.append([{'words': grouped[k]} for k in sorted(grouped)])
        scenes = [
            [title, f'assets/images/book-{book:02d}-scenes/chapter-{ci + 1:02d}-scene-{si + 1:02d}.webp', desc]
            for si, (title, desc) in enumerate(content.SCENES[ci])
        ]
        data = {'chapter': ci + 1, 'scenes': scenes, 'words': flat, 'pages': pages_out}
        target = ROOT / 'data' / f'book-{book:02d}-chapter-{ci + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for w in flat if w['key'])
        flag = '' if has_audio else '  [SYNTH]'
        print(f'{target.name}: {len(flat)} words, {keys} key, 3 scenes{flag}')
