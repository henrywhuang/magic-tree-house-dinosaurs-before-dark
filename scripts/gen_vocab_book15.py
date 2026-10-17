#!/usr/bin/env python3
"""Book 15 (Viking Ships at Sunrise) vocabulary cards. OVERRIDES fix ECDICT's
wrong headword/pos/meaning for specific surfaces, each checked against its Book
15 sentence (tmp/book15_text/chNN.txt)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch01
    'damp': {'pos': 'adj.', 'meaning': '潮湿的；湿润的'},
    'dangled': {'word': 'dangle', 'pos': 'v.', 'meaning': '悬垂；晃荡'},
    # ch02
    'leather': {'pos': 'n.', 'meaning': '皮革'},
    'monks': {'word': 'monk', 'pos': 'n.', 'meaning': '修道士；僧侣'},
    'glided': {'word': 'glide', 'pos': 'v.', 'meaning': '滑翔；滑行'},
    'steep': {'pos': 'adj.', 'meaning': '陡峭的；险峻的'},
    # ch03
    'invader': {'pos': 'n.', 'meaning': '入侵者；侵略者'},
    'coast': {'pos': 'n.', 'meaning': '海岸；海滨'},
    'serpent': {'pos': 'n.', 'meaning': '（大）蛇；巨蛇'},
    'prows': {'word': 'prow', 'pos': 'n.', 'meaning': '船首'},
    'monastery': {'pos': 'n.', 'meaning': '修道院'},
    # ch04
    'candles': {'word': 'candle', 'pos': 'n.', 'meaning': '蜡烛'},
    'myths': {'word': 'myth', 'pos': 'n.', 'meaning': '神话；传说'},
    'gleaming': {'pos': 'adj.', 'meaning': '闪闪发光的；闪亮的'},
    'jewels': {'word': 'jewel', 'pos': 'n.', 'meaning': '宝石；珠宝'},
    'quill': {'pos': 'n.', 'meaning': '羽毛笔；翎管'},
    # ch05
    'ocean': {'pos': 'n.', 'meaning': '海洋；大海'},
    'gulls': {'word': 'gull', 'pos': 'n.', 'meaning': '海鸥'},
    'clutching': {'word': 'clutch', 'pos': 'v.', 'meaning': '抓紧；紧握'},
    'ledge': {'pos': 'n.', 'meaning': '岩架；突出的岩石'},
    'blazed': {'word': 'blaze', 'pos': 'v.', 'meaning': '闪耀；发出光辉'},
    # ch06
    'scrambled': {'word': 'scramble', 'pos': 'v.', 'meaning': '爬；攀爬'},
    'fog': {'pos': 'n.', 'meaning': '雾；雾气'},
    'gather': {'pos': 'v.', 'meaning': '收集；聚拢'},
    # ch07
    'screeched': {'word': 'screech', 'pos': 'v.', 'meaning': '尖叫；发出尖厉声'},
    'pebbles': {'word': 'pebble', 'pos': 'n.', 'meaning': '鹅卵石；小圆石'},
    'crept': {'word': 'creep', 'pos': 'v.', 'meaning': '蹑手蹑脚地走；悄悄爬行'},
    'jagged': {'pos': 'adj.', 'meaning': '参差不齐的；锯齿状的'},
    'shallow': {'pos': 'adj.', 'meaning': '浅的；不深的'},
    'warriors': {'word': 'warrior', 'pos': 'n.', 'meaning': '战士；勇士'},
    'helmets': {'word': 'helmet', 'pos': 'n.', 'meaning': '头盔；钢盔'},
    'shields': {'word': 'shield', 'pos': 'n.', 'meaning': '盾；盾牌'},
    # ch08
    'deck': {'pos': 'n.', 'meaning': '甲板'},
    'crew': {'pos': 'n.', 'meaning': '全体船员；船员'},
    'row': {'pos': 'v.', 'meaning': '划（船）；划桨'},
    'oar': {'pos': 'n.', 'meaning': '桨；船桨'},
    'current': {'pos': 'n.', 'meaning': '水流；潮流'},
    'crawled': {'word': 'crawl', 'pos': 'v.', 'meaning': '爬行；匍匐前进'},
    # ch09
    'scales': {'word': 'scale', 'pos': 'n.', 'meaning': '鳞；鳞片'},
    'slime': {'pos': 'n.', 'meaning': '黏液；黏滑物'},
    'ducked': {'word': 'duck', 'pos': 'v.', 'meaning': '迅速低下头；躲闪'},
    'glittered': {'word': 'glitter', 'pos': 'v.', 'meaning': '闪闪发光；闪耀'},
    'rearing': {'word': 'rear', 'pos': 'v.', 'meaning': '昂起；高高扬起'},
    'dove': {'word': 'dive', 'pos': 'v.', 'meaning': '俯冲；潜入'},
    'gasped': {'word': 'gasp', 'pos': 'v.', 'meaning': '倒吸气；喘息'},
    # ch10
    'enchantress': {'pos': 'n.', 'meaning': '女巫；女魔法师'},
    'sighed': {'word': 'sigh', 'pos': 'v.', 'meaning': '叹气；叹息'},
    'sparkling': {'pos': 'adj.', 'meaning': '闪闪发光的；闪耀的'},
    'heroes': {'word': 'hero', 'pos': 'n.', 'meaning': '英雄；勇士'},
    'thrilled': {'pos': 'adj.', 'meaning': '非常激动的；兴奋的'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(15, OVERRIDES)
