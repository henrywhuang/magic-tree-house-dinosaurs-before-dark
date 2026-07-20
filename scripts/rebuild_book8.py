#!/usr/bin/env python3
"""Build Book 8 reader JSON from proofread OCR and ASR timestamps."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base
from book8_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

SOURCE = ROOT / '8.月球漫游记.pdf_by_PaddleOCR-VL-1.6.json'
CHAPTER_STARTS = [7, 16, 24, 32, 42, 50, 58, 64, 73, 79]
STORY_END = 87

base.CHAPTER_STARTS = CHAPTER_STARTS
base.STORY_END = STORY_END
base.TITLES = TITLES
base.SCENE_ANCHORS = SCENE_ANCHORS
base.SCENES = SCENES
base.VOCABULARY = VOCABULARY
BASE_CHAPTER_TEXT = base.chapter_text


def chapter_text(pages, chapter_index):
    text = BASE_CHAPTER_TEXT(pages, chapter_index)
    text = text.replace('moon-light', 'moonlight').replace('twoway', 'two-way')
    text = text.replace('blueand-white', 'blue-and-white').replace('spacecrafts', 'spacecraft')
    text = text.replace('twenty seven', 'twenty-seven')
    text = text.replace('Jack-almost', 'Jack—almost')
    text = re.sub(r'\$\s*\\underline\{\\text\{Boing! Boing! Boing!\}\}\s*\$', 'Boing! Boing! Boing!', text)
    text = re.sub(r'bu\s*\$.*?\$\s*qu', 'buggy', text, flags=re.S)
    text = re.sub(r'([,;:])\n([a-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])\n([0-9])', r'\1 \2', text)
    text = re.sub(r'([0-9])\n([a-z])', r'\1 \2', text)
    text = text.replace('behind them and the door to the hallway.\nopened.',
                        'behind them, and the door to the hallway opened.')
    if chapter_index == 9:
        duplicate = ('The midnight woods woke up.\nA breeze rustled the leaves.\nAn owl hooted.\n'
                     'The sounds were soft, but very alive.\nJack opened his eyes. He pushed his glasses into place.\n'
                     'He smiled. Morgan was still with them. He could see her in the moonlight. Her long white hair was shining.\n'
                     '“Morgan, can you and the tree house stay here?” said Annie. “In Frog Creek?”\n'
                     '“No, I must leave again, I’m afraid,” said Morgan.\n'
                     '“I’ve been gone from Camelot for a long time.”\n'
                     'She handed Jack his pack. She brushed his cheek. Her hand felt soft and cool.\n'
                     '“A bit of moondust still on you,” she said. “Thank you, Jack, for your great love of knowledge.”')
        text = text.replace(duplicate + '\n' + duplicate, duplicate)
    return text


base.chapter_text = chapter_text


def build_chapter(pages, chapter_index):
    words, paragraphs = base.ocr_words(pages, chapter_index)
    asr = json.loads((ROOT / 'tmp' / 'asr' / f'book8-ch{chapter_index + 1:02d}.json').read_text())
    base.assign_timestamps(words, asr['words'])
    standard, extension = base.extract_vocab(pages, chapter_index)
    base.apply_keywords(words, standard + extension)
    first, second = base.scene_boundaries(paragraphs, chapter_index)
    for word in words:
        word['page'] = 0 if word['para'] < first else 1 if word['para'] < second else 2
    flat = [
        {'i': index, 'word': word['word'], 'before': word['before'], 'after': word['after'],
         'start': word['start'], 'end': word['end'], 'key': word['key'], 'page': word['page']}
        for index, word in enumerate(words)
    ]
    output_pages = []
    for page in range(3):
        grouped = {}
        for index, word in enumerate(words):
            if word['page'] == page:
                grouped.setdefault(word['para'], []).append(flat[index])
        output_pages.append([{'words': grouped[key]} for key in sorted(grouped)])
    scenes = [
        [title, f'assets/images/book-08-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}


def main():
    pages = json.loads(SOURCE.read_text(encoding='utf-8'))
    for chapter_index in range(10):
        data = build_chapter(pages, chapter_index)
        target = ROOT / 'data' / f'book-08-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes')


if __name__ == '__main__':
    main()
