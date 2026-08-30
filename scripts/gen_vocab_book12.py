#!/usr/bin/env python3
"""Generate Book 11 (Polar Bears Past Bedtime) vocabulary learning data.

Same shared schema and generator (gen_vocab_book4) as Books 4-10.  OVERRIDES fix
ECDICT's wrong headword/pos/meaning for specific surfaces, each checked against
its Book 11 sentence.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gen_vocab_book4 as base
from book12_content import TITLES

OVERRIDES = {
    'wondered': {'word': 'wonder', 'pos': 'v.', 'meaning': '想知道；纳闷'},
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '低声说；耳语'},
    'enchantress': {'pos': 'n.', 'meaning': '女巫；女魔法师'},
    'arctic': {'pos': 'adj.', 'meaning': '北极的；北极地区的'},
    'chattering': {'word': 'chatter', 'pos': 'v.', 'meaning': '（牙齿）打战；喋喋不休'},
    'hunter': {'pos': 'n.', 'meaning': '猎人；狩猎者'},
    'puzzled': {'pos': 'adj.', 'meaning': '困惑的；迷惑不解的'},
    'parkas': {'word': 'parka', 'pos': 'n.', 'meaning': '派克大衣；连帽皮大衣'},
    'mittens': {'word': 'mitten', 'pos': 'n.', 'meaning': '连指手套'},
    'huskies': {'word': 'husky', 'pos': 'n.', 'meaning': '哈士奇；雪橇犬'},
    'drifting': {'word': 'drift', 'pos': 'v.', 'meaning': '飘落；漂移'},
    'igloo': {'pos': 'n.', 'meaning': '（爱斯基摩人的）圆顶雪屋；冰屋'},
    'platform': {'pos': 'n.', 'meaning': '台；平台'},
    'snorting': {'word': 'snort', 'pos': 'v.', 'meaning': '喷鼻息；打响鼻'},
    'wrestling': {'word': 'wrestle', 'pos': 'v.', 'meaning': '扭打；摔跤'},
    'panting': {'word': 'pant', 'pos': 'v.', 'meaning': '喘气；气喘吁吁'},
    'whimpered': {'word': 'whimper', 'pos': 'v.', 'meaning': '呜咽；啜泣'},
    'growled': {'word': 'growl', 'pos': 'v.', 'meaning': '咆哮；低吼'},
    'paced': {'word': 'pace', 'pos': 'v.', 'meaning': '踱步；来回走'},
    'crept': {'word': 'creep', 'pos': 'v.', 'meaning': '悄悄地走；爬行'},
    'moan': {'pos': 'n.', 'meaning': '低吼；呻吟'},
    'protect': {'pos': 'v.', 'meaning': '保护；防卫'},
    'bowing': {'word': 'bow', 'pos': 'v.', 'meaning': '鞠躬；弯腰'},
    'twirled': {'word': 'twirl', 'pos': 'v.', 'meaning': '旋转；转动'},
    'exploded': {'word': 'explode', 'pos': 'v.', 'meaning': '爆发；炸开'},
    'dazzling': {'pos': 'adj.', 'meaning': '耀眼的；令人目眩的'},
    'hushed': {'pos': 'adj.', 'meaning': '低声的；寂静的'},
    'shimmered': {'word': 'shimmer', 'pos': 'v.', 'meaning': '闪烁；发出微光'},
    'shimmering': {'pos': 'adj.', 'meaning': '闪着微光的'},
    'sighed': {'word': 'sigh', 'pos': 'v.', 'meaning': '叹气；叹息'},
    'shrugged': {'word': 'shrug', 'pos': 'v.', 'meaning': '耸肩'},
    'discover': {'pos': 'v.', 'meaning': '发现；找到'},
    'battered': {'word': 'batter', 'pos': 'v.', 'meaning': '猛击；连续拍打'},
    'unscramble': {'pos': 'v.', 'meaning': '整理；解读（打乱的字母）'},
    'succeeded': {'word': 'succeed', 'pos': 'v.', 'meaning': '成功；做到'},
    'quest': {'pos': 'n.', 'meaning': '探索；追寻'},
    'soothing': {'pos': 'adj.', 'meaning': '抚慰的；令人宽心的'},
    'tingly': {'pos': 'adj.', 'meaning': '微微刺痛的；发麻的'},
    'ordinary': {'pos': 'adj.', 'meaning': '普通的；平常的'},
}


def build_chapter(chapter):
    data = json.loads((ROOT / f'data/book-12-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
    words = data['words']
    text, spans = base.build_text(words)
    sentences = base.sentence_spans(text)
    keyed = [(word['word'], spans[index]) for index, word in enumerate(words) if word.get('key')]
    seen, order = {}, []
    for surface, span in keyed:
        if surface not in seen:
            seen[surface] = span
            order.append(surface)
    headwords = [value.get('word', surface.lower()) for surface in order
                 if (value := OVERRIDES.get(surface.lower()))]
    dictionary = base.load_ecdict(order + headwords)

    def resolve(surface):
        override = OVERRIDES.get(surface.lower(), {})
        headword = override.get('word', surface.lower())
        return (headword, base.get_phonetic(headword, dictionary) or base.get_phonetic(surface, dictionary),
                override.get('pos') or base.get_pos(surface, dictionary),
                override.get('meaning') or base.get_meaning(surface, dictionary) or surface)

    eligible = [surface for surface in order if base.eligible_core(surface)]
    eligible.sort(key=lambda surface: (-base.rarity(surface, dictionary), surface.lower()))
    core = set(eligible[:10])
    core_meanings = {surface: resolve(surface)[3] for surface in order if surface in core}
    entries, used_ids = [], set()
    for surface in order:
        word_id = re.sub(r'[^a-z0-9]', '', surface.lower()) or 'w'
        original, suffix = word_id, 2
        while word_id in used_ids:
            word_id = f'{original}{suffix}'
            suffix += 1
        used_ids.add(word_id)
        headword, phonetic, part_of_speech, meaning = resolve(surface)
        forms = list(dict.fromkeys([headword, surface]))
        entry = {
            'id': word_id, 'word': headword, 'forms': forms,
            'tier': 'core' if surface in core else 'recognition',
            'phonetic': phonetic, 'partOfSpeech': part_of_speech, 'meaning': meaning,
            'wordForms': f'原文词形：{surface}',
            'sentence': base.find_sentence(text, sentences, seen[surface]),
            'sentenceAudio': f'assets/audio/sentences/book-12-chapter-{chapter:02d}/{word_id}.mp3',
        }
        if surface in core:
            entry['phonics'] = base.phonics(headword)
            choices = [value for key, value in core_meanings.items() if key != surface and value != meaning]
            entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
        entries.append(entry)
    return {'book': 12, 'chapter': chapter, 'title': TITLES[chapter - 1], 'words': entries}


def main():
    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-12-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for word in result['words'] if word['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')


if __name__ == '__main__':
    main()
