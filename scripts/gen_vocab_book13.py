#!/usr/bin/env python3
"""Book 13 vocabulary cards. OVERRIDES fix ECDICT wrong headword/pos/meaning."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch01
    'secret': {'pos': 'adj.', 'meaning': '秘密的；机密的'},
    'shimmering': {'pos': 'adj.', 'meaning': '闪光的；微微发亮的'},
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '低声说；耳语'},
    'wondered': {'word': 'wonder', 'pos': 'v.', 'meaning': '想知道；纳闷'},
    'mission': {'pos': 'n.', 'meaning': '任务；使命'},
    # ch02
    'shivered': {'word': 'shiver', 'pos': 'v.', 'meaning': '颤抖；哆嗦'},
    'bridge': {'pos': 'n.', 'meaning': '桥；桥梁'},
    'shop': {'pos': 'n.', 'meaning': '商店；店铺'},
    'cloak': {'pos': 'n.', 'meaning': '斗篷；披风'},
    # ch03
    'peered': {'word': 'peer', 'pos': 'v.', 'meaning': '凝视；仔细看'},
    'soothsayers': {'word': 'soothsayer', 'pos': 'n.', 'meaning': '预言者；占卜者'},
    'columns': {'word': 'column', 'pos': 'n.', 'meaning': '圆柱；柱子'},
    'temple': {'pos': 'n.', 'meaning': '神庙；庙宇'},
    'shields': {'word': 'shield', 'pos': 'n.', 'meaning': '盾；盾牌'},
    # ch04
    'fight': {'pos': 'n.', 'meaning': '打斗；搏斗'},
    'cheered': {'word': 'cheer', 'pos': 'v.', 'meaning': '欢呼；喝彩'},
    'guard': {'pos': 'n.', 'meaning': '卫兵；守卫'},
    'spine': {'pos': 'n.', 'meaning': '脊柱；脊背'},
    # ch05
    'ceiling': {'pos': 'n.', 'meaning': '天花板；顶棚'},
    'pillows': {'word': 'pillow', 'pos': 'n.', 'meaning': '枕头；靠垫'},
    'patio': {'pos': 'n.', 'meaning': '露台；天井'},
    'fountain': {'pos': 'n.', 'meaning': '喷泉'},
    'scrolls': {'word': 'scroll', 'pos': 'n.', 'meaning': '卷轴；画卷'},
    'papyrus': {'pos': 'n.', 'meaning': '纸莎草纸；莎草纸'},
    # ch06
    'title': {'pos': 'n.', 'meaning': '标题；题目'},
    'erupting': {'word': 'erupt', 'pos': 'v.', 'meaning': '（火山）喷发；爆发'},
    'sundial': {'pos': 'n.', 'meaning': '日晷'},
    'shadow': {'pos': 'n.', 'meaning': '影子；阴影'},
    'blast': {'pos': 'n.', 'meaning': '爆炸声；巨响'},
    # ch07
    'trembling': {'word': 'tremble', 'pos': 'v.', 'meaning': '颤抖；抖动'},
    'crashing': {'word': 'crash', 'pos': 'v.', 'meaning': '轰然倒下；猛撞'},
    'roof': {'pos': 'n.', 'meaning': '屋顶；房顶'},
    'cracks': {'word': 'crack', 'pos': 'n.', 'meaning': '裂缝；裂纹'},
    'plaster': {'pos': 'n.', 'meaning': '灰泥；灰浆'},
    # ch08
    'rushed': {'word': 'rush', 'pos': 'v.', 'meaning': '冲；奔'},
    'collapsed': {'word': 'collapse', 'pos': 'v.', 'meaning': '倒塌；坍塌'},
    'shouted': {'word': 'shout', 'pos': 'v.', 'meaning': '呼喊；喊叫'},
    'walls': {'word': 'wall', 'pos': 'n.', 'meaning': '墙；墙壁'},
    'crumbling': {'word': 'crumble', 'pos': 'v.', 'meaning': '崩塌；碎裂'},
    'billowed': {'word': 'billow', 'pos': 'v.', 'meaning': '翻腾；滚滚升起'},
    # ch09
    'drifts': {'word': 'drift', 'pos': 'n.', 'meaning': '（风吹积成的）堆；漂积物'},
    'trapped': {'word': 'trap', 'pos': 'v.', 'meaning': '困住；使动弹不得'},
    'dazed': {'pos': 'adj.', 'meaning': '头昏眼花的；发懵的'},
    'save': {'pos': 'v.', 'meaning': '拯救；挽救'},
    # ch10
    'home': {'pos': 'n.', 'meaning': '家；家乡'},
    'brave': {'pos': 'adj.', 'meaning': '勇敢的；无畏的'},
    'famous': {'pos': 'adj.', 'meaning': '著名的；出名的'},
    'escape': {'pos': 'v.', 'meaning': '逃脱；逃走'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(13, OVERRIDES)
