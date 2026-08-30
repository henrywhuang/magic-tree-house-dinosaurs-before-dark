#!/usr/bin/env python3
"""Generic vocabulary-card builder for the docx-sourced books (13-16).
Same schema/generator as Books 4-12; per-book OVERRIDES fix ECDICT's wrong
headword/pos/meaning. Call run(book, OVERRIDES)."""
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gen_vocab_book4 as base


def run(book, overrides):
    content = importlib.import_module(f'book{book}_content')
    titles = content.TITLES

    def build_chapter(chapter):
        data = json.loads((ROOT / f'data/book-{book:02d}-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
        words = data['words']
        text, spans = base.build_text(words)
        sentences = base.sentence_spans(text)
        keyed = [(w['word'], spans[i]) for i, w in enumerate(words) if w.get('key')]
        seen, order = {}, []
        for surface, span in keyed:
            if surface not in seen:
                seen[surface] = span
                order.append(surface)
        headwords = [value.get('word', s.lower()) for s in order if (value := overrides.get(s.lower()))]
        dictionary = base.load_ecdict(order + headwords)

        def resolve(surface):
            ov = overrides.get(surface.lower(), {})
            head = ov.get('word', surface.lower())
            return (head, base.get_phonetic(head, dictionary) or base.get_phonetic(surface, dictionary),
                    ov.get('pos') or base.get_pos(surface, dictionary),
                    ov.get('meaning') or base.get_meaning(surface, dictionary) or surface)

        eligible = [s for s in order if base.eligible_core(s)]
        eligible.sort(key=lambda s: (-base.rarity(s, dictionary), s.lower()))
        core = set(eligible[:10])
        core_meanings = {s: resolve(s)[3] for s in order if s in core}
        entries, used_ids = [], set()
        for surface in order:
            wid = re.sub(r'[^a-z0-9]', '', surface.lower()) or 'w'
            base_id, suffix = wid, 2
            while wid in used_ids:
                wid = f'{base_id}{suffix}'
                suffix += 1
            used_ids.add(wid)
            head, phon, pos, meaning = resolve(surface)
            entry = {
                'id': wid, 'word': head, 'forms': list(dict.fromkeys([head, surface])),
                'tier': 'core' if surface in core else 'recognition',
                'phonetic': phon, 'partOfSpeech': pos, 'meaning': meaning,
                'wordForms': f'原文词形：{surface}',
                'sentence': base.find_sentence(text, sentences, seen[surface]),
                'sentenceAudio': f'assets/audio/sentences/book-{book:02d}-chapter-{chapter:02d}/{wid}.mp3',
            }
            if surface in core:
                entry['phonics'] = base.phonics(head)
                choices = [v for k, v in core_meanings.items() if k != surface and v != meaning]
                entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
            entries.append(entry)
        return {'book': book, 'chapter': chapter, 'title': titles[chapter - 1], 'words': entries}

    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-{book:02d}-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for w in result['words'] if w['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')
