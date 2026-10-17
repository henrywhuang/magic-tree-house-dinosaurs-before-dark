#!/usr/bin/env python3
"""Book 17 vocabulary cards.

OVERRIDES fix ECDICT's wrong headword/pos/meaning for specific surfaces, each
checked against its Book 17 sentence (tmp/book17_text/chNN.txt).  Verb surfaces
get a base-form headword + pos 'v.'; verbforms_vocab then fills the inflections.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch1 — A New Mission
    'terrier': {'pos': 'n.', 'meaning': '㹴犬；小猎犬'},
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '低声说；耳语'},
    'spell': {'pos': 'n.', 'meaning': '魔咒；咒语'},
    'mission': {'pos': 'n.', 'meaning': '任务；使命'},
    # ch2 — The Unsinkable Ship
    'cloak': {'pos': 'n.', 'meaning': '斗篷；披风'},
    'glittered': {'word': 'glitter', 'pos': 'v.', 'meaning': '闪烁；闪耀'},
    'smokestacks': {'word': 'smokestack', 'pos': 'n.', 'meaning': '烟囱'},
    'passengers': {'word': 'passenger', 'pos': 'n.', 'meaning': '乘客；旅客'},
    'iceberg': {'pos': 'n.', 'meaning': '冰山'},
    'jolt': {'pos': 'n.', 'meaning': '震动；颠簸'},
    # ch3 — SOS
    'gushed': {'word': 'gush', 'pos': 'v.', 'meaning': '喷涌；涌出'},
    'engines': {'word': 'engine', 'pos': 'n.', 'meaning': '发动机；引擎'},
    'scampered': {'word': 'scamper', 'pos': 'v.', 'meaning': '蹦跳；奔跑'},
    'shrugged': {'word': 'shrug', 'pos': 'v.', 'meaning': '耸肩'},
    'operator': {'pos': 'n.', 'meaning': '报务员；操作员'},
    'distress': {'pos': 'n.', 'meaning': '遇险；危难'},
    # ch4 — Put on Your Life Belts!
    'hallway': {'pos': 'n.', 'meaning': '走廊；过道'},
    'staterooms': {'word': 'stateroom', 'pos': 'n.', 'meaning': '（轮船的）客舱；特等舱'},
    'slanting': {'word': 'slant', 'pos': 'v.', 'meaning': '倾斜；歪斜'},
    'robes': {'word': 'robe', 'pos': 'n.', 'meaning': '长袍；睡袍'},
    'cheerfully': {'pos': 'adv.', 'meaning': '高兴地；愉快地'},
    # ch5 — William and Lucy
    'freckles': {'word': 'freckle', 'pos': 'n.', 'meaning': '雀斑'},
    'confused': {'pos': 'adj.', 'meaning': '困惑的；迷惑不解的'},
    'kissed': {'word': 'kiss', 'pos': 'v.', 'meaning': '亲吻；吻'},
    'freezing': {'pos': 'adj.', 'meaning': '冰冷的；严寒的'},
    # ch6 — Women and Children First
    'rescued': {'word': 'rescue', 'pos': 'v.', 'meaning': '营救；解救'},
    'soothing': {'pos': 'adj.', 'meaning': '抚慰的；使人平静的'},
    'crowd': {'pos': 'n.', 'meaning': '人群；一群人'},
    'lively': {'pos': 'adj.', 'meaning': '欢快的；活泼的'},
    'streaked': {'word': 'streak', 'pos': 'v.', 'meaning': '飞驰；掠过'},
    # ch7 — The Gift
    'cables': {'word': 'cable', 'pos': 'n.', 'meaning': '缆索；缆绳'},
    'uniformed': {'pos': 'adj.', 'meaning': '穿制服的'},
    'brightly': {'pos': 'adv.', 'meaning': '明亮地；鲜艳地'},
    'danger': {'pos': 'n.', 'meaning': '危险；危难'},
    'straightened': {'word': 'straighten', 'pos': 'v.', 'meaning': '挺直；弄直'},
    'silver': {'pos': 'adj.', 'meaning': '银的；银色的'},
    'tossed': {'word': 'toss', 'pos': 'v.', 'meaning': '抛；扔'},
    'jerked': {'word': 'jerk', 'pos': 'v.', 'meaning': '猛地一动；急拉'},
    # ch8 — Every Man for Himself
    'railing': {'pos': 'n.', 'meaning': '栏杆；护栏'},
    'peered': {'word': 'peer', 'pos': 'v.', 'meaning': '凝视；盯着看'},
    'glassy': {'pos': 'adj.', 'meaning': '平滑如镜的；光滑的'},
    'panic': {'pos': 'v.', 'meaning': '惊慌；恐慌'},
    'crew': {'pos': 'n.', 'meaning': '全体船员；全体乘务员'},
    'tilted': {'word': 'tilt', 'pos': 'v.', 'meaning': '倾斜；倾侧'},
    'crawled': {'word': 'crawl', 'pos': 'v.', 'meaning': '爬行；匍匐前进'},
    # ch9 — Time Stops
    'crashing': {'word': 'crash', 'pos': 'v.', 'meaning': '猛撞；哗啦作响'},
    'furniture': {'pos': 'n.', 'meaning': '家具'},
    'steep': {'pos': 'adj.', 'meaning': '陡峭的；陡的'},
    'barely': {'pos': 'adv.', 'meaning': '几乎不；勉强'},
    # ch10 — A Touch of Magic
    'cheeks': {'word': 'cheek', 'pos': 'n.', 'meaning': '脸颊；面颊'},
    'whined': {'word': 'whine', 'pos': 'v.', 'meaning': '呜咽；哀鸣'},
    'stroked': {'word': 'stroke', 'pos': 'v.', 'meaning': '抚摸；轻抚'},
    'furry': {'pos': 'adj.', 'meaning': '毛茸茸的；覆盖着毛的'},
    'shuddered': {'word': 'shudder', 'pos': 'v.', 'meaning': '战栗；发抖'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(17, OVERRIDES)
