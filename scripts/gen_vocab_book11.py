#!/usr/bin/env python3
"""Generate Book 11 (Lions at Lunchtime) vocabulary learning data.

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
from book11_content import TITLES

OVERRIDES = {
    # ch1
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '低声说；耳语'},
    'shadows': {'word': 'shadow', 'pos': 'n.', 'meaning': '阴影；暗处'},
    # ch2
    'wildebeests': {'word': 'wildebeest', 'pos': 'n.', 'meaning': '角马；牛羚'},
    'migrate': {'pos': 'v.', 'meaning': '迁徙；迁移'},
    'beasts': {'word': 'beast', 'pos': 'n.', 'meaning': '野兽；牲畜'},
    'nervously': {'pos': 'adv.', 'meaning': '紧张地；不安地'},
    'grazing': {'word': 'graze', 'pos': 'v.', 'meaning': '吃草；放牧'},
    # ch3
    'pattern': {'pos': 'n.', 'meaning': '图案；花纹；样式'},
    'layer': {'pos': 'n.', 'meaning': '层；地层'},
    'depends': {'word': 'depend', 'pos': 'v.', 'meaning': '依靠；取决于'},
    # ch4
    'wailed': {'word': 'wail', 'pos': 'v.', 'meaning': '哀号；恸哭'},
    'concentrate': {'pos': 'v.', 'meaning': '集中注意力；专心'},
    # ch5
    'trampled': {'word': 'trample', 'pos': 'v.', 'meaning': '践踏；踩踏'},
    'mocking': {'pos': 'adj.', 'meaning': '嘲弄的；讥讽的'},
    'hyena': {'pos': 'n.', 'meaning': '鬣狗'},
    'scurried': {'word': 'scurry', 'pos': 'v.', 'meaning': '急匆匆地跑；快步疾走'},
    # ch6
    'trunk': {'pos': 'n.', 'meaning': '象鼻；树干'},
    'relief': {'pos': 'n.', 'meaning': '宽慰；如释重负'},
    'sidetracked': {'word': 'sidetrack', 'pos': 'v.', 'meaning': '使分心；岔开话题'},
    'grunt': {'pos': 'n.', 'meaning': '哼声；呼噜声'},
    'flitted': {'word': 'flit', 'pos': 'v.', 'meaning': '轻快地飞；掠过'},
    'twittered': {'word': 'twitter', 'pos': 'v.', 'meaning': '（鸟）鸣啭；叽喳叫'},
    # ch7
    'dappled': {'pos': 'adj.', 'meaning': '斑驳的；有斑点的'},
    'scatter': {'pos': 'v.', 'meaning': '驱散；使四散'},
    # ch8
    'gifts': {'word': 'gift', 'pos': 'n.', 'meaning': '礼物；赠品'},
    'screwed': {'word': 'screw', 'pos': 'v.', 'meaning': '拧紧；旋上'},
    'gracefully': {'pos': 'adv.', 'meaning': '优雅地；从容地'},
    # ch9
    'crouched': {'word': 'crouch', 'pos': 'v.', 'meaning': '蹲伏；蜷缩'},
    'lionesses': {'word': 'lioness', 'pos': 'n.', 'meaning': '雌狮；母狮'},
    'cubs': {'word': 'cub', 'pos': 'n.', 'meaning': '幼崽；幼兽'},
    'pride': {'pos': 'n.', 'meaning': '（狮）群；一群狮子'},
    'flicked': {'word': 'flick', 'pos': 'v.', 'meaning': '轻弹；甩动'},
    'gleamed': {'word': 'gleam', 'pos': 'v.', 'meaning': '闪烁；发光'},
    'piercing': {'pos': 'adj.', 'meaning': '锐利的；刺人的'},
    'growled': {'word': 'growl', 'pos': 'v.', 'meaning': '咆哮；低吼'},
    # ch10
    'racing': {'word': 'race', 'pos': 'v.', 'meaning': '（心）狂跳；飞奔'},
    'calm': {'pos': 'v.', 'meaning': '使平静；镇定下来'},
    'mudhole': {'pos': 'n.', 'meaning': '泥坑；泥沼'},
}


def build_chapter(chapter):
    data = json.loads((ROOT / f'data/book-11-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
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
            'sentenceAudio': f'assets/audio/sentences/book-11-chapter-{chapter:02d}/{word_id}.mp3',
        }
        if surface in core:
            entry['phonics'] = base.phonics(headword)
            choices = [value for key, value in core_meanings.items() if key != surface and value != meaning]
            entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
        entries.append(entry)
    return {'book': 11, 'chapter': chapter, 'title': TITLES[chapter - 1], 'words': entries}


def main():
    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-11-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for word in result['words'] if word['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')


if __name__ == '__main__':
    main()
