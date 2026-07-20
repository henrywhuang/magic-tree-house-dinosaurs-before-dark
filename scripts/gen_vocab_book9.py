#!/usr/bin/env python3
"""Generate Book 9 vocabulary learning data with the shared schema."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gen_vocab_book4 as base
from book9_content import TITLES


# ECDICT is a general-purpose dictionary and occasionally picks the wrong headword
# or part of speech for an inflected word.  These overrides are deliberately
# contextual: every meaning below has been checked against the sentence in Book 9.
# ``word`` is used only when the learner should practise the base form.
OVERRIDES = {
    'early': {'pos': 'adv.', 'meaning': '早；提早'},
    'pale': {'pos': 'adj.', 'meaning': '浅色的；苍白的'},
    'lovely': {'pos': 'adj.', 'meaning': '可爱的；美好的'},
    'paper': {'pos': 'n.', 'meaning': '纸；纸张'},
    'mysteriously': {'pos': 'adv.', 'meaning': '神秘地'},
    'pink': {'pos': 'adj.', 'meaning': '粉红色的'},
    'reef': {'pos': 'n.', 'meaning': '礁；珊瑚礁'},
    'skeletons': {'word': 'skeleton', 'pos': 'n.', 'meaning': '骨骼；骨架'},
    'oceanographers': {'word': 'oceanographer', 'pos': 'n.', 'meaning': '海洋学家'},
    'submersibles': {'word': 'submersible', 'pos': 'n.', 'meaning': '潜水器'},
    'seats': {'word': 'seat', 'pos': 'n.', 'meaning': '座位'},
    'computer': {'pos': 'n.', 'meaning': '计算机；电脑'},
    'panel': {'pos': 'n.', 'meaning': '控制面板；仪表板'},
    'hatch': {'pos': 'n.', 'meaning': '舱口；舱盖'},
    'screen': {'pos': 'n.', 'meaning': '屏幕；显示屏'},
    'arrow': {'pos': 'n.', 'meaning': '箭头；方向标记'},
    'relief': {'pos': 'n.', 'meaning': '宽慰；安心'},
    'steer': {'pos': 'v.', 'meaning': '驾驶；操纵'},
    'glued': {'pos': 'adj.', 'meaning': '紧盯着的；目不转睛的'},
    'planet': {'pos': 'n.', 'meaning': '行星'},
    'valleys': {'word': 'valley', 'pos': 'n.', 'meaning': '山谷；谷地'},
    'caves': {'word': 'cave', 'pos': 'n.', 'meaning': '洞穴；山洞'},
    'visit': {'pos': 'v.', 'meaning': '参观；游览'},
    'peeping': {'pos': 'v.', 'meaning': '窥看；探头看'},
    'antlers': {'word': 'antler', 'pos': 'n.', 'meaning': '鹿角'},
    'clam': {'pos': 'n.', 'meaning': '蛤蜊；蛤'},
    'dolphins': {'word': 'dolphin', 'pos': 'n.', 'meaning': '海豚'},
    'peering': {'pos': 'v.', 'meaning': '仔细看；凝视'},
    'flashed': {'pos': 'v.', 'meaning': '闪现；突然显示'},
    'crack': {'word': 'crack', 'pos': 'n.', 'meaning': '裂缝；裂纹'},
    'hull': {'word': 'hull', 'pos': 'n.', 'meaning': '船体；艇身'},
    'defective': {'word': 'defective', 'pos': 'adj.', 'meaning': '有缺陷的；故障的'},
    'helicopter': {'word': 'helicopter', 'pos': 'n.', 'meaning': '直升机'},
    'junkyard': {'word': 'junkyard', 'pos': 'n.', 'meaning': '废品场；旧货场'},
    'broken': {'pos': 'adj.', 'meaning': '损坏的；破裂的'},
    'rise': {'pos': 'v.', 'meaning': '上升；升起'},
    'gasped': {'pos': 'v.', 'meaning': '喘着气说；倒吸气'},
    'horror': {'pos': 'n.', 'meaning': '惊恐；恐惧'},
    'plant': {'pos': 'n.', 'meaning': '植物'},
    'hugged': {'pos': 'v.', 'meaning': '抱住；紧紧环绕'},
    'suckers': {'word': 'sucker', 'pos': 'n.', 'meaning': '吸盘'},
    'shy': {'pos': 'adj.', 'meaning': '胆小的；怕生的'},
    'tentacles': {'word': 'tentacle', 'pos': 'n.', 'meaning': '触手；触须'},
    'ceiling': {'pos': 'n.', 'meaning': '天花板；舱顶'},
    'drop': {'pos': 'n.', 'meaning': '一滴；少量'},
    'breaks': {'pos': 'v.', 'meaning': '破裂；裂开'},
    'enemies': {'word': 'enemy', 'pos': 'n.', 'meaning': '敌人；天敌'},
    'hammerhead': {'pos': 'n.', 'meaning': '锤头鲨'},
    'shadowy': {'pos': 'adj.', 'meaning': '模糊的；影影绰绰的'},
    'breathed': {'pos': 'v.', 'meaning': '轻声说；呼吸'},
    'spurting': {'pos': 'v.', 'meaning': '喷涌；喷射'},
    'suddenly': {'word': 'suddenly', 'pos': 'adv.', 'meaning': '突然；忽然'},
    'burst': {'pos': 'v.', 'meaning': '突然冲出；爆裂'},
    'bobbed': {'pos': 'v.', 'meaning': '上下浮动'},
    'sparkled': {'pos': 'v.', 'meaning': '闪耀；闪闪发光'},
    'bare': {'pos': 'adj.', 'meaning': '赤裸的；未穿鞋袜的'},
    'bottom': {'pos': 'n.', 'meaning': '底部；底面'},
    'ankles': {'word': 'ankle', 'pos': 'n.', 'meaning': '脚踝'},
    'blank': {'pos': 'adj.', 'meaning': '空白的；无显示的'},
    'summer': {'pos': 'n.', 'meaning': '夏天；夏季'},
    'breast': {'pos': 'n.', 'meaning': '胸部；（breast stroke）蛙泳'},
    'fin': {'pos': 'n.', 'meaning': '鱼鳍；鳍'},
    'life': {'pos': 'n.', 'meaning': '生命'},
    'zigzagging': {'pos': 'v.', 'meaning': '曲折前进；之字形移动'},
    'struggling': {'pos': 'v.', 'meaning': '挣扎；艰难前进'},
    'float': {'word': 'float', 'pos': 'v.', 'meaning': '漂浮；浮在水面'},
    'sink': {'pos': 'v.', 'meaning': '下沉；沉没'},
    'clinging': {'pos': 'v.', 'meaning': '紧紧抓住；依附'},
    'smoothly': {'pos': 'adv.', 'meaning': '平稳地；顺畅地'},
    'flippers': {'word': 'flipper', 'pos': 'n.', 'meaning': '鳍状肢'},
    'chattered': {'pos': 'v.', 'meaning': '吱吱叫；快速交谈'},
    'gracefully': {'pos': 'adv.', 'meaning': '优美地；轻盈地'},
    'shallow': {'pos': 'adj.', 'meaning': '浅的；水浅的'},
    'soaked': {'pos': 'adj.', 'meaning': '湿透的；浸透的'},
    'ridges': {'word': 'ridge', 'pos': 'n.', 'meaning': '隆起的纹路；脊'},
    'pearl': {'pos': 'n.', 'meaning': '珍珠'},
    "oyster’s": {'word': 'oyster', 'pos': 'n.', 'meaning': '牡蛎；蚝'},
    'slanted': {'pos': 'v.', 'meaning': '斜射；倾斜'},
    'tucked': {'pos': 'v.', 'meaning': '塞进；收好'},
    'shadows': {'word': 'shadow', 'pos': 'n.', 'meaning': '阴影；树荫'},
    'patch': {'pos': 'n.', 'meaning': '一小块；斑片'},
    'along': {'pos': 'adv.', 'meaning': '一直；自始至终'},
    'squeezed': {'pos': 'v.', 'meaning': '挤压；紧紧夹住'},
    'chased': {'pos': 'v.', 'meaning': '追赶；追逐'},
    'true': {'pos': 'adj.', 'meaning': '真正的；真实的'},
    'grinned': {'pos': 'v.', 'meaning': '咧嘴笑'},
}


def build_chapter(chapter):
    data = json.loads((ROOT / f'data/book-09-chapter-{chapter:02d}.json').read_text(encoding='utf-8'))
    words = data['words']
    text, spans = base.build_text(words)
    sentences = base.sentence_spans(text)
    keyed = [(word['word'], spans[index]) for index, word in enumerate(words) if word.get('key')]
    seen, order = {}, []
    for surface, span in keyed:
        if surface not in seen:
            seen[surface] = span
            order.append(surface)
    headwords = [value.get('word', surface) for surface in order
                 if (value := OVERRIDES.get(surface.lower()))]
    dictionary = base.load_ecdict(order + headwords)

    def resolve(surface):
        override = OVERRIDES.get(surface.lower(), {})
        headword = override.get('word', surface)
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
            'sentenceAudio': f'assets/audio/sentences/book-09-chapter-{chapter:02d}/{word_id}.mp3',
        }
        if surface in core:
            entry['phonics'] = base.phonics(headword)
            choices = [value for key, value in core_meanings.items() if key != surface and value != meaning]
            entry['options'] = [meaning] + base.stable_pick(sorted(set(choices)), 2, surface)
        entries.append(entry)
    return {'book': 9, 'chapter': chapter, 'title': TITLES[chapter - 1], 'words': entries}


def main():
    for chapter in range(1, 11):
        result = build_chapter(chapter)
        target = ROOT / 'data' / f'vocabulary-book-09-chapter-{chapter:02d}.json'
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        core = sum(1 for word in result['words'] if word['tier'] == 'core')
        print(f'{target.name}: {len(result["words"])} words ({core} core)')


if __name__ == '__main__':
    main()
