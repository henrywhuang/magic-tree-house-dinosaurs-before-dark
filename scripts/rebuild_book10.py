#!/usr/bin/env python3
"""Build Book 10 (Ghost Town at Sundown / 孤独的牛仔) reader JSON from proofread OCR
and ASR timestamps. Reuses the Book7 base engine, parameterized for Book 10."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base
from book10_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

SOURCE = ROOT / '10孤独的牛仔.pdf_by_PaddleOCR-VL-1.6.json'
CHAPTER_STARTS = [3, 11, 23, 34, 42, 52, 62, 71, 80, 87]
STORY_END = 96

base.CHAPTER_STARTS = CHAPTER_STARTS
base.STORY_END = STORY_END
base.TITLES = TITLES
base.SCENE_ANCHORS = SCENE_ANCHORS
base.SCENES = SCENES
base.VOCABULARY = VOCABULARY
BASE_CHAPTER_TEXT = base.chapter_text


def chapter_text(pages, chapter_index):
    text = BASE_CHAPTER_TEXT(pages, chapter_index)
    # The workbook OCR preserves the Chapter 4 notebook as an HTML table.  The
    # reader stores plain word tokens, so keep the list content without leaking
    # markup into the story.
    text = re.sub(
        r"<table\b.*?</table>",
        "Horse Rules: 1. Soft hand. 2. Firm voice. 3. Sunny attitude. "
        "4. Praise. 5. Reward.",
        text,
        flags=re.S | re.I,
    )
    # The final source page continues with the complete Red River Valley lyrics.
    # They are back matter, not Chapter 10, and are not present in its narration.
    if chapter_index == 9:
        text = text.split("Here are the words to RED RIVER VALLEY", 1)[0]
    text = text.replace(
        "the two mustangs rubbed against one another and weighed.",
        "the two mustangs rubbed against one another and neighed.",
    )
    text = text.replace(
        "He reached into his backpack and took out his notebook and pencil.\nHe wrote:\n"
        "“What’s that sound?” said Annie.",
        "He reached into his backpack and took out his notebook and pencil.\n"
        "He wrote:\nRabbits with long legs\n“What’s that sound?” said Annie.",
    )
    text = text.replace(
        "The scroll had one glowing word on it:\n“We got it right!” said Annie.",
        "The scroll had one glowing word on it:\nECHO\n“We got it right!” said Annie.",
    )
    # Join sentences that the source PDF split across page turns.  These are
    # single dialogue paragraphs, not new speakers.
    text = text.replace(
        "“Slim,” said the cowboy. “My name is Slim Cooley.\n"
        "And this is Dusty.” He patted his horse.",
        "“Slim,” said the cowboy. “My name is Slim Cooley. "
        "And this is Dusty.” He patted his horse.",
    )
    text = text.replace(
        "“Okay, pardners,” said Slim. “See ya soon, Smiley.\n"
        "Come on, Shorty.”",
        "“Okay, pardners,” said Slim. “See ya soon, Smiley. "
        "Come on, Shorty.”",
    )
    text = text.replace(
        "“Oh, yeah?” Slim chuckled. “Well, lucky for us,\n"
        "Lonesome Luke sometimes likes to help folks out.”",
        "“Oh, yeah?” Slim chuckled. “Well, lucky for us, "
        "Lonesome Luke sometimes likes to help folks out.”",
    )
    # Keep Annie's reply as a separate paragraph so the change of speaker is
    # unambiguous in the reader.
    text = text.replace(
        "He looked at Annie. “So?” “Keep reading,” said Annie.",
        "He looked at Annie. “So?”\n“Keep reading,” said Annie.",
    )
    text = text.replace("rustlers'", "rustlers’")
    text = re.sub(r'(?m)^\s*Chapter\s+\d+\s*$', '', text)
    return text.strip()


base.chapter_text = chapter_text


def build_chapter(pages, chapter_index):
    words, paragraphs = base.ocr_words(pages, chapter_index)
    asr = json.loads((ROOT / 'tmp' / 'asr' / f'book10-ch{chapter_index + 1:02d}.json').read_text())
    base.assign_timestamps(words, asr['words'])
    standard, extension = base.extract_vocab(pages, chapter_index)
    base.apply_keywords(words, standard + extension)
    # Prefer the lowercase adjective uses over the earlier title/name uses so
    # the vocabulary card receives a sentence that demonstrates the meaning.
    preferred_occurrences = {0: 'wild', 4: 'slim'}
    if chapter_index in preferred_occurrences:
        surface = preferred_occurrences[chapter_index]
        preferred_index = next(index for index, word in enumerate(words) if word['word'] == surface)
        for index, word in enumerate(words):
            if word['word'].lower() == surface:
                word['key'] = index == preferred_index
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
        [title, f'assets/images/book-10-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}


def main():
    pages = json.loads(SOURCE.read_text(encoding='utf-8'))
    for chapter_index in range(10):
        data = build_chapter(pages, chapter_index)
        target = ROOT / 'data' / f'book-10-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes')


if __name__ == '__main__':
    main()
