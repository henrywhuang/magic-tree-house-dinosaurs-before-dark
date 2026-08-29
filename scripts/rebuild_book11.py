#!/usr/bin/env python3
"""Build Book 11 (Lions at Lunchtime / 狮口大逃亡) reader JSON.

Book 11 has no bilingual PaddleOCR workbook JSON, so the story text comes from
the scanned-English half-page OCR via book11_text. Everything else reuses the
Book 7 base engine (OCR/ASR alignment, keyword marking, 3-scene paging). All ten
chapter tracks are present and use word-level ASR anchors from tmp/asr/.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base
import book11_text as bt
from book11_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

base.TITLES = TITLES
base.SCENE_ANCHORS = SCENE_ANCHORS
base.SCENES = SCENES
base.VOCABULARY = VOCABULARY

# Per-chapter literal fixes: OCR debris cleanup and back-filled narration that the
# scan rendered as handwriting/scroll art (read aloud on the audio but absent from
# the printed English text).  Applied to the joined chapter text before tokenizing.
FIXES = {
    0: [
        ('The book’ s cover', 'The book’s cover'),
        ('hordes of zebras, _ tall\n~ ~~ giraffes,', 'hordes of zebras, tall giraffes,'),
    ],
    1: [
        ('A rustling sound came from outside the window. ees',
         'A rustling sound came from outside the window.'),
        ('“Don’ tbe silly.', '“Don’t be silly.'),
        ('wildebeests(WILL-dubbeests)migrate',
         'wildebeests (WILL-dubbeests) migrate'),
        # Morgan's third riddle is scroll art the OCR dropped; recovered verbatim from
        # this chapter's own narration (audio present) so it aligns to the reading.
        ('Jack unrolled the ancient scroll and read aloud:\nAnnie started down again.',
         'Jack unrolled the ancient scroll and read aloud:\n'
         'I’m the color of gold and as sweet as can be. '
         'But beware of the danger that’s all around me. What am I?\n'
         'Annie started down again.'),
    ],
    2: [
        # Jack's two notebook jottings are handwriting the OCR dropped; recovered
        # verbatim from this chapter's narration (audio present) so they align to it.
        ('Jack pulled out his notebook and wrote:\nHe turned the page and read more:',
         'Jack pulled out his notebook and wrote:\nNotes on Africa. Lions avoid giraffes.\n'
         'He turned the page and read more:'),
        ('Each animal depends on the one that goes before.\nHe wrote:',
         'Each animal depends on the one that goes before.\nHe wrote:\nAnimals all connected.'),
    ],
    3: [
        ('a pool of mud = ~——~——~~—~—~~-—— near the water', 'a pool of mud near the water'),
        ('The mud was up to her neck,', 'The mud was up to her neck.'),
        ('You can do it! ] know you can!', 'You can do it! I know you can!'),
    ],
    4: [
        ('“Oh, no! No! = No!” shouted Annie.; She raced down ie the bank, until she reached a sandy, clear ~ — —_—— spot.',
         '“Oh, no! No! No!” shouted Annie. She raced down the bank, until she reached a sandy, clear spot.'),
        ('The wildebeests followed her with a their wild eyes.:',
         'The wildebeests followed her with their wild eyes.'),
        ('the hyena Chi-EE-nuh)', 'the hyena (hi-EE-nuh)'),
    ],
    5: [
        ('Jack and Annie stood frozenasanelephant stepped out — of the shadows.',
         'Jack and Annie stood frozen as an elephant stepped out of the shadows.'),
        ('“I guess the elephant doesn’t like ‘dirty kids!” said Annie',
         '“I guess the elephant doesn’t like dirty kids!” said Annie'),
        ('“__a snake ora lion, ” Jack said', '“…a snake or a lion,” Jack said'),
        ('It did feel like a shower-a strong shower.',
         'It did feel like a shower—a strong shower.'),
    ],
    6: [
        ('the Masai(muh-SDpeople', 'the Masai (muh-SY) people'),
        # Jack recites the same riddle aloud here; recovered verbatim from this
        # chapter's narration so the spoken riddle aligns to the printed text.
        ('Jack said Morgan’s riddle:\n“T get it,” Annie whispered. “Honey...”',
         'Jack said Morgan’s riddle:\n'
         'I’m the color of gold and as sweet as can be. '
         'But beware of the danger that’s all around me. What am I?\n'
         '“T get it,” Annie whispered. “Honey...”'),
    ],
    7: [
        ('The warrior stared [ back at Jack and Annie.', 'The warrior stared back at Jack and Annie.'),
        ('“We were helping ee = one of your honey an guides, ” said Annie. ae The warrior was as still as a statue.',
         '“We were helping one of your honey guides,” said Annie. The warrior was as still as a statue.'),
        ('“Lots of good honey still there, ” i} i}\nAnnie said, smiling.',
         '“Lots of good honey still there,” Annie said, smiling.'),
        ('He had a kind, dignified smile. oe Jack and Annie', 'He had a kind, dignified smile. Jack and Annie'),
        ('There were still some crossing the river. P', 'There were still some crossing the river.'),
        ('They saw a family of zebras grazing together.!', 'They saw a family of zebras grazing together.'),
        ('it’s all yours. we’ve had enough.', 'it’s all yours. We’ve had enough.'),
    ],
    8: [
        ('He pulled the Africa book from his ra pack', 'He pulled the Africa book from his pack'),
        ('“Good plan,” Annie teased.\nok cm lus lid', '“Good plan,” Annie teased.'),
        ('They began tipto- L eing through the grass', 'They began tiptoeing through the grass'),
        ('When the rope ladder was just a few fect away', 'When the rope ladder was just a few feet away'),
        ('the zebras and giraffes didn’t seen to be bothered',
         'the zebras and giraffes didn’t seem to be bothered'),
        # The glowing answer is rendered as scroll art and therefore absent from OCR.
        ('The riddle was gone. In its place was one shimmering word:\n'
         'Jack grabbed the Pennsylvania book.',
         'The riddle was gone. In its place was one shimmering word:\n'
         'HONEY\nJack grabbed the Pennsylvania book.'),
    ],
    9: [
        ('Annie put the scroll with the other two scro- Ils.', 'Annie put the scroll with the other two scrolls.'),
        ('the honey from a bechive that a honey guide led us to', 'the honey from a beehive that a honey guide led us to'),
        ('And ail that was before a giraffe saved us from a lion.', 'And all that was before a giraffe saved us from a lion.'),
        ('“Ready?” i “Ready.”', '“Ready?” “Ready.”'),
        ('“Y’m full from our picnic,”', '“I’m full from our picnic,”'),
    ],
}


def cleanup(text):
    # Re-join broken contractions: ’ + space + suffix, and OCR's "ll"->"II"/"Il".
    text = text.replace('’ II', '’ll').replace('’ Il', '’ll')
    text = re.sub(r'’ (ll|t|s|d|re|ve|m)\b', r'’\1', text)
    # A capital I at the start of a quote is frequently mis-read as T.
    text = re.sub(r'“Tt\b', '“It', text)
    text = re.sub(r'“T(?=[ ’])', '“I', text)
    # Dialogue tags split across a line break before the speaker's name.
    text = re.sub(r'\bsaid\n(Annie|Jack|Morgan)\b', r'said \1', text)
    # Drop a space wedged before a closing double quote.
    text = re.sub(r'[ \t]+”', '”', text)
    text = text.replace('…', '...')
    return text


def chapter_text(pages, chapter_index):
    text = bt.chapter_text(chapter_index)
    for old, new in FIXES.get(chapter_index, []):
        if old not in text:
            raise RuntimeError(f'Chapter {chapter_index + 1}: fix target missing: {old[:50]!r}')
        text = text.replace(old, new)
    text = cleanup(text)
    return text.strip()


base.chapter_text = chapter_text


def synth_timestamps(words, seconds_per_word=0.36):
    """Even reading-pace timing for chapters whose narration was not supplied."""
    t = 0.0
    for word in words:
        word['start'] = round(t, 3)
        word['end'] = round(t + seconds_per_word * 0.85, 3)
        t += seconds_per_word


def build_chapter(chapter_index):
    words, paragraphs = base.ocr_words(None, chapter_index)
    asr_path = ROOT / 'tmp' / 'asr' / f'book11-ch{chapter_index + 1:02d}.json'
    has_audio = asr_path.exists()
    if has_audio:
        asr = json.loads(asr_path.read_text())
        base.assign_timestamps(words, asr['words'])
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
        [title, f'assets/images/book-11-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}, has_audio


def main():
    for chapter_index in range(10):
        data, has_audio = build_chapter(chapter_index)
        target = ROOT / 'data' / f'book-11-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        flag = '' if has_audio else '  [SYNTH timing — audio pending]'
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes{flag}')


if __name__ == '__main__':
    main()
