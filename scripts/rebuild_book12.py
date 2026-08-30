#!/usr/bin/env python3
"""Build Book 12 (Polar Bears Past Bedtime / 雪原上的北极熊) reader JSON.

Text comes from the supplied OCR Word doc via book12_text; timing from
tmp/asr/book12-chNN.json.  Reuses the Book 7 base engine.  Chapters 1-9 have
narration (raw tracks 032-040); chapter 10 (raw 041) was not supplied, so its
text is built with synthesised timing until the mp3 arrives.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base
import book12_text as bt
from book12_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

base.TITLES = TITLES
base.SCENE_ANCHORS = SCENE_ANCHORS
base.SCENES = SCENES
base.VOCABULARY = VOCABULARY

FIXES = {
    0: [  # ch1
        ('How did Annie Know exactly', 'How did Annie know exactly'),
        ('R0E/69 The moon lit their way', 'The moon lit their way'),
        ('N 0 2 6010|71', ''),
    ],
    1: [  # ch2 — Morgan's fourth riddle, OCR garbled "reat"/"1"
        ('I cover what’s reat and hide', 'I cover what’s real and hide'),
        ('What am 1?', 'What am I?'),
    ],
    2: [  # ch3 — riddle re-read, "i"/"i?" mis-cased
        ('But sometimes i bring out the courage in you.', 'But sometimes I bring out the courage in you.'),
        ('What am i?', 'What am I?'),
        ('R6018/83 Jack grabbed the Arctic book', 'Jack grabbed the Arctic book'),
    ],
    3: [  # ch4
        ('threw his notebook and the Aretic book', 'threw his notebook and the Arctic book'),
    ],
    4: [  # ch5
        ('up the snowbank.He clutched', 'up the snowbank. He clutched'),
        ('he said He reached into his pack', 'he said. He reached into his pack'),
    ],
    5: [  # ch6
        ('“Maybe she’ Il think we’re polar bears. too.”',
         '“Maybe she’ll think we’re polar bears, too.”'),
    ],
    7: [  # ch8 — riddle re-read solved; only "1" needs the pronoun
        ('“Where’d she go?” saked Annie.', '“Where’d she go?” asked Annie.'),
        ('ended in darkness.Jack had no', 'ended in darkness. Jack had no'),
        ('What am 1?', 'What am I?'),
    ],
    6: [  # ch7
        ('the words of the scal hunter', 'the words of the seal hunter'),
        ('Jack scrambled to his feet.Still wearing', 'Jack scrambled to his feet. Still wearing'),
    ],
    8: [  # ch9 — the four solved-riddle answers run together on one scroll line
        ('said: OYSTER The scroll from their trip to the Wild West said: ECHO The scroll '
         'from their journey to Africa said: HONEY Their scroll from the Arctic said: MASK',
         'said: OYSTER. The scroll from their trip to the Wild West said: ECHO. The scroll '
         'from their journey to Africa said: HONEY. Their scroll from the Arctic said: MASK.'),
    ],
    9: [  # ch10 — OCR interleaved the closing sentences across two paragraphs
        ('These will be the people who can help you.“', 'These will be the people who can help you.”'),
        ('They came out of the woods. ked warm and cozy. overhead.',
         'They came out of the woods.'),
        ('Jack saw their house in the distance. It looThe porch light glowed. The moon shone '
         'She started running. Jack took off after her, running to the place that they both loved the best.',
         'Jack saw their house in the distance. It looked warm and cozy. The porch light glowed. '
         'The moon shone overhead. She started running. Jack took off after her, running to the '
         'place that they both loved the best.'),
    ],
}


def cleanup(text):
    text = re.sub(r'([a-z,])\.([A-Z])', r'\1. \2', text)   # missing space after a period
    text = re.sub(r'[ \t]+”', '”', text)
    text = re.sub(r'“\s+', '“', text)
    text = text.replace('…', '...')
    return text


def chapter_text(pages, chapter_index):
    text = bt.chapter_text(chapter_index)
    for old, new in FIXES.get(chapter_index, []):
        if old in text:
            text = text.replace(old, new)
    text = cleanup(text)
    return text.strip()


base.chapter_text = chapter_text


def synth_timestamps(words, seconds_per_word=0.36):
    t = 0.0
    for word in words:
        word['start'] = round(t, 3)
        word['end'] = round(t + seconds_per_word * 0.85, 3)
        t += seconds_per_word


def build_chapter(chapter_index):
    words, paragraphs = base.ocr_words(None, chapter_index)
    asr_path = ROOT / 'tmp' / 'asr' / f'book12-ch{chapter_index + 1:02d}.json'
    has_audio = asr_path.exists()
    if has_audio:
        base.assign_timestamps(words, json.loads(asr_path.read_text())['words'])
    else:
        synth_timestamps(words)
    standard, extension = base.extract_vocab(None, chapter_index)
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
        [title, f'assets/images/book-12-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}, has_audio


def main():
    for chapter_index in range(10):
        data, has_audio = build_chapter(chapter_index)
        target = ROOT / 'data' / f'book-12-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        flag = '' if has_audio else '  [SYNTH timing — audio pending]'
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes{flag}')


if __name__ == '__main__':
    main()
