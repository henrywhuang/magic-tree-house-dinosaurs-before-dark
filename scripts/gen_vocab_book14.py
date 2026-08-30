#!/usr/bin/env python3
"""Book 14 vocabulary cards. OVERRIDES fix ECDICT wrong headword/pos/meaning.

Each surface key is the lowercased original word form; every meaning is checked
against its Book 14 sentence (tmp/book14_text/chNN.txt).  Verb surfaces are
tagged 'v.' with their base form so verbforms_vocab rewrites them to 原形.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ---- verbs mis-tagged as n./other (base form -> verbforms conjugates) ----
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '低声说；耳语'},
    'wonder': {'pos': 'v.', 'meaning': '想知道；纳闷'},
    'hurried': {'word': 'hurry', 'pos': 'v.', 'meaning': '匆忙；急忙赶'},
    'lurched': {'word': 'lurch', 'pos': 'v.', 'meaning': '突然晃动；猛地前倾'},
    'blazed': {'word': 'blaze', 'pos': 'v.', 'meaning': '熊熊燃烧；升腾烈焰'},
    'snatched': {'word': 'snatch', 'pos': 'v.', 'meaning': '抢夺；一把抓起'},
    'ducked': {'word': 'duck', 'pos': 'v.', 'meaning': '迅速低身；闪躲'},
    'embraced': {'word': 'embrace', 'pos': 'v.', 'meaning': '拥抱；抱住'},
    'separated': {'word': 'separate', 'pos': 'v.', 'meaning': '分开；隔开'},
    'panic': {'pos': 'v.', 'meaning': '惊慌；慌乱'},
    # ---- garbled meanings (proper name / acronym / 'should' / self-ref / English) ----
    'ladder': {'pos': 'n.', 'meaning': '梯子；阶梯'},
    'shoulder': {'pos': 'n.', 'meaning': '肩；肩膀'},
    'driver': {'pos': 'n.', 'meaning': '驾车人；车夫'},
    'danger': {'pos': 'n.', 'meaning': '危险；危险处境'},
    'power': {'pos': 'n.', 'meaning': '力量；权力'},
    'summer': {'pos': 'n.', 'meaning': '夏天；夏季'},
    'soldier’s': {'word': 'soldier', 'pos': 'n.', 'meaning': '士兵；军人'},
    # ---- wrong sense for this story / misleading second gloss ----
    'field': {'pos': 'n.', 'meaning': '田野；田地'},
    'twilight': {'pos': 'n.', 'meaning': '黄昏；暮色'},
    'grain': {'pos': 'n.', 'meaning': '谷物；粮食'},
    'spirits': {'word': 'spirit', 'pos': 'n.', 'meaning': '鬼魂；亡灵'},
    'tomb': {'pos': 'n.', 'meaning': '坟墓；陵墓'},
    'crowd': {'pos': 'n.', 'meaning': '人群；一群人'},
    'clay': {'pos': 'n.', 'meaning': '黏土；陶土'},
    'armor': {'pos': 'n.', 'meaning': '盔甲；铠甲'},
    'relief': {'pos': 'n.', 'meaning': '宽慰；轻松'},
    'legend': {'pos': 'n.', 'meaning': '传说；传奇故事'},
    # ---- adjectives mis-tagged as n. ----
    'honored': {'pos': 'adj.', 'meaning': '受尊敬的；尊贵的'},
    'heavenly': {'pos': 'adj.', 'meaning': '天上的；天国的'},
    'lost': {'pos': 'adj.', 'meaning': '迷路的；迷失方向的'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(14, OVERRIDES)
