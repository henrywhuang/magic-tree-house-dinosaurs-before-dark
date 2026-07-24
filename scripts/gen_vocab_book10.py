#!/usr/bin/env python3
"""Generate Book 10 vocabulary learning data with the shared schema."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gen_vocab_book4 as base
from book10_content import TITLES


# ECDICT is a general-purpose dictionary and occasionally picks the wrong headword
# or part of speech for an inflected word.  These overrides are deliberately
# contextual: every meaning below has been checked against the sentence in Book 10.
# ``word`` is used only when the learner should practise the base form.
OVERRIDES = {
    'porch': {'pos': 'n.', 'meaning': '门廊；门厅'},
    'feeling': {'pos': 'n.', 'meaning': '感觉；直觉'},
    'ready': {'pos': 'adj.', 'meaning': '准备好的'},
    'odd': {'pos': 'adj.', 'meaning': '奇怪的；古怪的'},
    'wild': {'pos': 'adj.', 'meaning': '野生的；荒野的'},
    'west': {'pos': 'n.', 'meaning': '西部；西方'},
    'prairie': {'pos': 'n.', 'meaning': '大草原；草原'},
    'lone': {'pos': 'adj.', 'meaning': '孤零零的；单独的'},
    'low': {'pos': 'adj.', 'meaning': '低的；低垂的'},
    'town': {'pos': 'n.', 'meaning': '城镇；小镇'},
    'spooky': {'pos': 'adj.', 'meaning': '阴森的；吓人的'},
    'flats': {'word': 'flat', 'pos': 'n.', 'meaning': '平地；平坦地区'},
    'store': {'pos': 'n.', 'meaning': '商店；店铺'},
    'building': {'pos': 'n.', 'meaning': '建筑物；房屋'},
    'dusty': {'pos': 'adj.', 'meaning': '布满灰尘的'},
    'hat': {'pos': 'n.', 'meaning': '帽子'},
    'stiff': {'pos': 'adj.', 'meaning': '僵硬的；不易弯曲的'},
    'outside': {'pos': 'adv.', 'meaning': '在外面；向外面'},
    'hotel': {'word': 'hotel', 'pos': 'n.', 'meaning': '旅馆；酒店'},
    'daylight': {'pos': 'n.', 'meaning': '日光；白昼'},
    'piano': {'pos': 'n.', 'meaning': '钢琴'},
    'electricity': {'pos': 'n.', 'meaning': '电；电力'},
    'band': {'pos': 'n.', 'meaning': '一群；一队'},
    'pinched': {'word': 'pinch', 'pos': 'v.', 'meaning': '捏住；掐'},
    'angry': {'pos': 'adj.', 'meaning': '生气的；愤怒的'},
    'mother': {'pos': 'n.', 'meaning': '母亲；母兽'},
    'colt': {'pos': 'n.', 'meaning': '小马；马驹'},
    'mustang': {'word': 'mustang', 'pos': 'n.', 'meaning': '野马'},
    'mare': {'pos': 'n.', 'meaning': '母马'},
    'treat': {'word': 'treat', 'pos': 'v.', 'meaning': '对待；处理'},
    'cowboy': {'pos': 'n.', 'meaning': '牛仔'},
    'reckon': {'pos': 'v.', 'meaning': '认为；估计'},
    'thieves': {'word': 'thief', 'pos': 'n.', 'meaning': '小偷；盗贼'},
    'rustlers': {'word': 'rustler', 'pos': 'n.', 'meaning': '偷牛马贼'},
    'stole': {'word': 'steal', 'pos': 'v.', 'meaning': '偷走；盗取'},
    'brave': {'pos': 'adj.', 'meaning': '勇敢的'},
    'throat': {'pos': 'n.', 'meaning': '喉咙；咽喉'},
    'nickname': {'pos': 'n.', 'meaning': '绰号；昵称'},
    'slim': {'pos': 'adj.', 'meaning': '瘦的；苗条的'},
    'name': {'pos': 'n.', 'meaning': '名字；姓名'},
    'stagecoach': {'pos': 'n.', 'meaning': '驿站马车；公共马车'},
    'bounced': {'word': 'bounce', 'pos': 'v.', 'meaning': '上下颠簸；跳动'},
    'rise': {'pos': 'n.', 'meaning': '高地；斜坡'},
    'halt': {'pos': 'n.', 'meaning': '停止；停下'},
    'voice': {'pos': 'n.', 'meaning': '声音；嗓音'},
    'campfire': {'pos': 'n.', 'meaning': '营火；篝火'},
    'clump': {'pos': 'n.', 'meaning': '一丛；一群'},
    'camp': {'pos': 'n.', 'meaning': '营地；宿营地'},
    'have': {'pos': 'v.', 'meaning': '进行；享受（have fun 玩得开心）'},
    'fun': {'pos': 'n.', 'meaning': '乐趣；快乐'},
    'firm': {'pos': 'adj.', 'meaning': '坚定的；有力的'},
    'sunny': {'pos': 'adj.', 'meaning': '乐观的；阳光般的'},
    'fine': {'pos': 'adj.', 'meaning': '安好的；没问题的'},
    'chance': {'pos': 'n.', 'meaning': '机会；时机'},
    'trusted': {'word': 'trust', 'pos': 'v.', 'meaning': '信任；相信'},
    'howdy': {'word': 'howdy', 'pos': 'int.', 'meaning': '你好；嗨'},
    'boss': {'pos': 'n.', 'meaning': '领头人；老板'},
    'canyon': {'word': 'canyon', 'pos': 'n.', 'meaning': '峡谷'},
    'neck': {'pos': 'n.', 'meaning': '脖子；颈部'},
    'unsaddled': {'word': 'unsaddle', 'pos': 'v.', 'meaning': '给马卸下马鞍'},
    'bags': {'word': 'bag', 'pos': 'n.', 'meaning': '袋子；行囊'},
    'over': {'pos': 'adv.', 'meaning': '反复地（over and over）'},
    'and': {'pos': 'conj.', 'meaning': '和；又（连接重复成分）'},
    'sad': {'pos': 'adj.', 'meaning': '悲伤的；伤心的'},
    'drinking': {'word': 'drink', 'pos': 'v.', 'meaning': '喝；饮用'},
    'coffee': {'word': 'coffee', 'pos': 'n.', 'meaning': '咖啡'},
    'biscuit': {'word': 'biscuit', 'pos': 'n.', 'meaning': '饼干'},
    'canteen': {'pos': 'n.', 'meaning': '水壶；军用水壶'},
    'bitter': {'pos': 'adj.', 'meaning': '苦的；有苦味的'},
    'south': {'pos': 'adv.', 'meaning': '向南；朝南'},
    'herder': {'pos': 'n.', 'meaning': '牧人；放牧者'},
    'writer': {'pos': 'n.', 'meaning': '作家；作者'},
    'stay': {'word': 'stay', 'pos': 'v.', 'meaning': '待着；停留'},
    'echo': {'pos': 'n.', 'meaning': '回声；回音'},
    'reached': {'word': 'reach', 'pos': 'v.', 'meaning': '到达；抵达'},
    'sure': {'pos': 'adj.', 'meaning': '确信的；确定的'},
    'winked': {'word': 'wink', 'pos': 'v.', 'meaning': '眨眼；使眼色'},
    'short': {'pos': 'adj.', 'meaning': '矮的；短的'},
    'snapped': {'word': 'snap', 'pos': 'v.', 'meaning': '猛抖；啪地甩动'},
    'lonesome': {'word': 'lonesome', 'pos': 'adj.', 'meaning': '孤独的；寂寞的'},
    'inside': {'pos': 'adv.', 'meaning': '在里面；进入里面'},
    'frog': {'word': 'frog', 'pos': 'n.', 'meaning': 'Frog Creek 地名的一部分'},
    'trip': {'pos': 'n.', 'meaning': '旅行；旅程'},
    'author’s': {'word': 'author', 'pos': 'n.', 'meaning': '作者的（所有格）'},
    'below': {'pos': 'adv.', 'meaning': '在下面；下方'},
}


def build_chapter(chapter):
    data = json.loads((ROOT / f'data/book-10-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
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
            'sentenceAudio': f'assets/audio/sentences/book-10-chapter-{chapter:02d}/{word_id}.mp3',
        }
        if surface in core:
            entry['phonics'] = base.phonics(headword)
            choices = [value for key, value in core_meanings.items() if key != surface and value != meaning]
            entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
        entries.append(entry)
    return {'book': 10, 'chapter': chapter, 'title': TITLES[chapter - 1], 'words': entries}


def main():
    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-10-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for word in result['words'] if word['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')


if __name__ == '__main__':
    main()
