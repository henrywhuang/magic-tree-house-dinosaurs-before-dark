#!/usr/bin/env python3
"""Generate Book 8 vocabulary learning data with the shared schema."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gen_vocab_book4 as base
from book8_content import TITLES


def build_chapter(chapter):
    data = json.loads((ROOT / f'data/book-08-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
    words = data['words']
    text, spans = base.build_text(words)
    sentences = base.sentence_spans(text)
    keyed = [(word['word'], spans[index]) for index, word in enumerate(words) if word.get('key')]
    seen, order = {}, []
    for surface, span in keyed:
        if surface not in seen:
            seen[surface] = span
            order.append(surface)
    dictionary = base.load_ecdict(order)

    def resolve(surface):
        return (base.get_phonetic(surface, dictionary), base.get_pos(surface, dictionary),
                base.get_meaning(surface, dictionary) or surface)

    eligible = [surface for surface in order if base.eligible_core(surface)]
    eligible.sort(key=lambda surface: (-base.rarity(surface, dictionary), surface.lower()))
    core = set(eligible[:10])
    core_meanings = {surface: resolve(surface)[2] for surface in order if surface in core}
    entries, used_ids = [], set()
    for surface in order:
        word_id = re.sub(r'[^a-z0-9]', '', surface.lower()) or 'w'
        original, suffix = word_id, 2
        while word_id in used_ids:
            word_id = f'{original}{suffix}'
            suffix += 1
        used_ids.add(word_id)
        phonetic, part_of_speech, meaning = resolve(surface)
        entry = {
            'id': word_id, 'word': surface, 'forms': [surface],
            'tier': 'core' if surface in core else 'recognition',
            'phonetic': phonetic, 'partOfSpeech': part_of_speech, 'meaning': meaning,
            'wordForms': f'原文词形：{surface}',
            'sentence': base.find_sentence(text, sentences, seen[surface]),
            'sentenceAudio': f'assets/audio/sentences/book-08-chapter-{chapter:02d}/{word_id}.mp3',
        }
        if surface in core:
            entry['phonics'] = base.phonics(surface)
            choices = [value for key, value in core_meanings.items() if key != surface and value != meaning]
            entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
        entries.append(entry)
    return {'book': 8, 'chapter': chapter, 'title': TITLES[chapter - 1], 'words': entries}


def main():
    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-08-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for word in result['words'] if word['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')


if __name__ == '__main__':
    main()
