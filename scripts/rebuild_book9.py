#!/usr/bin/env python3
"""Build Book 9 reader JSON from proofread OCR and ASR timestamps."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_book7 as base
from book9_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

SOURCE = ROOT / '9与海豚共舞.pdf_by_PaddleOCR-VL-1.6.json'
CHAPTER_STARTS = [3, 14, 26, 32, 41, 48, 54, 62, 69, 82]
STORY_END = 91

base.CHAPTER_STARTS = CHAPTER_STARTS
base.STORY_END = STORY_END
base.TITLES = TITLES
base.SCENE_ANCHORS = SCENE_ANCHORS
base.SCENES = SCENES
base.VOCABULARY = VOCABULARY
BASE_CHAPTER_TEXT = base.chapter_text


def chapter_text(pages, chapter_index):
    text = BASE_CHAPTER_TEXT(pages, chapter_index)
    text = text.replace(
        '“You must show that you know how to do research,” said Morgan, “and show that you can find answers”\n'
        'to hard questions.“\n”How?“ said Annie.\n”By solving four riddles,“ said Morgan.',
        '“You must show that you know how to do research,” said Morgan, “and show that you can find answers '
        'to hard questions.”\n“How?” said Annie.\n“By solving four riddles,” said Morgan.',
    )
    text = text.replace('“Where you going so early?” his dad called.',
                        '“Where are you going so early?” his dad called.')
    text = text.replace('Someone looked out the window of the tree house—a lovely old woman with long white hair. Morgan le Fay.\n'
                        'Jack and Annie climbed up the rope ladder',
                        'Someone looked out the window of the tree house—a lovely old woman with long white hair. Morgan le Fay.\n'
                        '“Come up!” called the magical librarian.\nJack and Annie climbed up the rope ladder')
    text = text.replace('Nearly\n5,000 different species', 'Nearly 5,000 different species')
    text = text.replace('“No kidding,” said Jack. He added “giant clam” to his list.\nJack looked up.',
                        '“No kidding,” said Jack. He added “giant clam” to his list.\n“Hey!” cried Annie.\nJack looked up.')
    text = text.replace('the computer,“ said Jack.',
                        '“Yeah, the oceanographer was writing notes on the computer,” said Jack.')
    text = text.replace('now— it was spurting', 'now—it was spurting')
    if chapter_index == 5:
        missing = (
            '\n“Come on, Annie,” said Jack. “It doesn’t care if you’re polite.”\n'
            'The octopus blinked at Jack.\n'
            '“Get out of here!” Jack yelled at it. “Now! Beat it! Scram! Go!”\n'
            'The octopus shot a cloud of black liquid into the water and disappeared into the dark cloud. '
            'Its long tentacles trailed through the water.\n'
            'The mini-sub started to rise slowly again.\n'
            '“You hurt his feelings,” Annie said.\n'
            '“I don’t think so.” Something bothered Jack. He looked back at the ocean book. He read to himself:\n'
            'The octopus squirts black ink to escape its enemies. One of its main enemies is the shark.\n'
            '“Oh, no,” said Jack.\n“What’s wrong?” asked Annie.\n'
            'Jack looked out the window. The water was growing clear again.\n'
            'A shadowy figure moved toward the mini-sub.\n“What is that?” whispered Annie.\n'
            'The fish was way bigger than the dolphins. And it had a very weird head.\n'
            'Jack could feel his heart nearly stop.\n'
            '“A hammerhead shark,” he breathed. “We’re really in trouble now.”'
        )
        text += missing
    text = text.replace('“And I swam faster so you would swim faster,”\nsaid Annie.',
                        '“And I swam faster so you would swim faster,” said Annie.')
    text = text.replace('“My research is all wet.\nWe’ll never be Master Librarians now.”',
                        '“My research is all wet. We’ll never be Master Librarians now.”')
    duplicate = ('\nget between the oyster’s shell and its skin. This irritates the oyster. So it makes a pearly '
                 'material to surround the grain of sand. In this way, over a few years, a pearl is formed.\n'
                 '“I can’t tell if there’s a pearl in there or not,” said Annie.\n'
                 '“Maybe we should bang it against a rock,” said Jack.\n'
                 '“Now that would really irritate the oyster,” said Annie.\n“Yeah.”\n'
                 '“Maybe we should just leave it alone,” said Annie.')
    text = text.replace(duplicate, '')
    text = text.replace('if oyster is the right answer', 'if the oyster is the right answer')
    text = re.sub(r'(?m)^\s*Chapter\s+\d+\s*$', '', text)
    return text.strip()


base.chapter_text = chapter_text


def build_chapter(pages, chapter_index):
    words, paragraphs = base.ocr_words(pages, chapter_index)
    asr = json.loads((ROOT / 'tmp' / 'asr' / f'book9-ch{chapter_index + 1:02d}.json').read_text())
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
        [title, f'assets/images/book-09-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}


def main():
    pages = json.loads(SOURCE.read_text(encoding='utf-8'))
    for chapter_index in range(10):
        data = build_chapter(pages, chapter_index)
        target = ROOT / 'data' / f'book-09-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes')


if __name__ == '__main__':
    main()
