#!/usr/bin/env python3
"""Book 20 vocabulary cards.

OVERRIDES fix ECDICT's wrong headword/pos/meaning for specific surfaces, each
checked against its Book 20 sentence.  Verb surfaces get a base-form headword +
pos 'v.'; verbforms_vocab then fills the inflections.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch1 — The Last Gift
    'faint': {'pos': 'adj.', 'meaning': '微弱的；隐约的'},
    'grabbed': {'word': 'grab', 'pos': 'v.', 'meaning': '抓起；一把抓住'},
    'oak': {'pos': 'n.', 'meaning': '橡树'},
    'special': {'pos': 'adj.', 'meaning': '特别的；特殊的'},
    'kangaroo': {'pos': 'n.', 'meaning': '袋鼠'},
    'eagle’s': {'word': 'eagle', 'pos': 'n.', 'meaning': '鹰；雕'},
    'scratched': {'word': 'scratch', 'pos': 'v.', 'meaning': '抓；挠'},
    'spin': {'pos': 'v.', 'meaning': '旋转；打转'},
    'absolutely': {'pos': 'adv.', 'meaning': '完全地；绝对地'},
    # ch2 — Sleepyhead
    'drought': {'pos': 'n.', 'meaning': '干旱；旱灾'},
    'sniffed': {'word': 'sniff', 'pos': 'v.', 'meaning': '嗅；闻'},
    'emu': {'pos': 'n.', 'meaning': '鸸鹋（澳洲大鸟，不会飞）'},
    'koala': {'pos': 'n.', 'meaning': '考拉；树袋熊'},
    'marsupial': {'pos': 'n.', 'meaning': '有袋动物'},
    'threat': {'pos': 'n.', 'meaning': '威胁；危险'},
    'moisture': {'pos': 'n.', 'meaning': '水分；湿气'},
    'thirsty': {'pos': 'adj.', 'meaning': '口渴的'},
    'harsh': {'pos': 'adj.', 'meaning': '刺耳的；粗厉的'},
    # ch3 — Big Foot
    'terrible': {'pos': 'adj.', 'meaning': '可怕的；吓人的'},
    'beak': {'pos': 'n.', 'meaning': '鸟嘴；喙'},
    'kookaburra': {'pos': 'n.', 'meaning': '笑翠鸟（澳洲鸟类）'},
    'stomach': {'pos': 'n.', 'meaning': '肚子；胃'},
    'pouch': {'pos': 'n.', 'meaning': '（袋鼠的）育儿袋'},
    'stamp': {'pos': 'n.', 'meaning': '跺脚'},
    'copying': {'word': 'copy', 'pos': 'v.', 'meaning': '模仿；照着做'},
    'contest': {'pos': 'n.', 'meaning': '比赛；竞赛'},
    'zigzagged': {'word': 'zigzag', 'pos': 'v.', 'meaning': '曲折前进；之字形行进'},
    # ch4 — Joey
    'enemy': {'pos': 'n.', 'meaning': '敌人；天敌'},
    'dingo': {'pos': 'n.', 'meaning': '澳洲野犬'},
    'chased': {'word': 'chase', 'pos': 'v.', 'meaning': '追赶；追逐'},
    'joey': {'pos': 'n.', 'meaning': '幼袋鼠'},
    'weight': {'pos': 'n.', 'meaning': '重量；分量'},
    'shy': {'pos': 'adj.', 'meaning': '害羞的；胆小的'},
    'backward': {'pos': 'adv.', 'meaning': '反着地；向后'},
    'burst': {'pos': 'v.', 'meaning': '突然（燃起）；爆发'},
    'wildfire': {'pos': 'n.', 'meaning': '野火；森林大火'},
    # ch5 — Wildfire
    'choice': {'pos': 'n.', 'meaning': '选择'},
    'spreading': {'word': 'spread', 'pos': 'v.', 'meaning': '蔓延；扩散'},
    'stung': {'word': 'sting', 'pos': 'v.', 'meaning': '刺痛；蜇'},
    'dashed': {'word': 'dash', 'pos': 'v.', 'meaning': '猛冲；飞奔'},
    'choked': {'word': 'choke', 'pos': 'v.', 'meaning': '呛；窒息'},
    'coughed': {'word': 'cough', 'pos': 'v.', 'meaning': '咳嗽'},
    'stumbled': {'word': 'stumble', 'pos': 'v.', 'meaning': '跌跌撞撞地走；绊倒'},
    'haze': {'pos': 'n.', 'meaning': '烟雾；薄雾'},
    'smoky': {'pos': 'adj.', 'meaning': '烟雾弥漫的'},
    # ch6 — Hand to Hand
    'thump': {'pos': 'v.', 'meaning': '重重地撞；砰地敲击'},
    'howl': {'pos': 'n.', 'meaning': '嚎叫；长嗥'},
    'amazing': {'pos': 'adj.', 'meaning': '惊人的；令人惊奇的'},
    'handprints': {'word': 'handprint', 'pos': 'n.', 'meaning': '手印'},
    'despite': {'pos': 'prep.', 'meaning': '尽管；虽然'},
    'breathe': {'pos': 'v.', 'meaning': '呼吸'},
    'whistling': {'pos': 'adj.', 'meaning': '呼啸的；发出哨声的'},
    'boom': {'pos': 'n.', 'meaning': '隆隆声；轰响'},
    'pouring': {'pos': 'adj.', 'meaning': '倾盆的；瓢泼的'},
    # ch7 — Rain, Rain, Rain
    'steam': {'pos': 'n.', 'meaning': '水汽；蒸汽'},
    'charred': {'pos': 'adj.', 'meaning': '烧焦的；烧黑的'},
    'pretend': {'pos': 'v.', 'meaning': '假装；假想'},
    'disturbed': {'word': 'disturb', 'pos': 'v.', 'meaning': '打扰；惊动'},
    'lucky': {'pos': 'adj.', 'meaning': '幸运的'},
    'stirred': {'word': 'stir', 'pos': 'v.', 'meaning': '微微动弹；扭动'},
    'drizzle': {'pos': 'n.', 'meaning': '毛毛雨；细雨'},
    'sprinkle': {'pos': 'n.', 'meaning': '小雨；零星小雨'},
    'slapping': {'word': 'slap', 'pos': 'v.', 'meaning': '啪啪地拍打；啪嗒啪嗒地走'},
    # ch8 — The Rainbow Serpent
    'nod': {'pos': 'n.', 'meaning': '点头'},
    'studied': {'word': 'study', 'pos': 'v.', 'meaning': '仔细察看；端详'},
    'myths': {'word': 'myth', 'pos': 'n.', 'meaning': '神话；传说'},
    'artists': {'word': 'artist', 'pos': 'n.', 'meaning': '艺术家；画家'},
    'ceremony': {'pos': 'n.', 'meaning': '仪式；典礼'},
    'frowned': {'word': 'frown', 'pos': 'v.', 'meaning': '皱眉'},
    'explain': {'pos': 'v.', 'meaning': '解释；说明'},
    'steamy': {'pos': 'adj.', 'meaning': '湿热的；水汽弥漫的'},
    'wiggled': {'word': 'wiggle', 'pos': 'v.', 'meaning': '扭动；扭动着钻出'},
    # ch9 — What Boy?
    'lovely': {'pos': 'adj.', 'meaning': '可爱的；美妙的'},
    'wasted': {'word': 'waste', 'pos': 'v.', 'meaning': '浪费'},
    'precious': {'pos': 'adj.', 'meaning': '宝贵的；珍贵的'},
    'wisely': {'pos': 'adv.', 'meaning': '明智地'},
    'mystery': {'pos': 'n.', 'meaning': '神秘；奥秘'},
    'traditions': {'word': 'tradition', 'pos': 'n.', 'meaning': '传统；习俗'},
    'lessons': {'word': 'lesson', 'pos': 'n.', 'meaning': '教训；功课'},
    'flutter': {'pos': 'n.', 'meaning': '一阵飘动；（眨眼般的）一瞬'},
    'whirlwind': {'pos': 'n.', 'meaning': '旋风'},
    # ch10 — Dreamtime
    'helper': {'pos': 'n.', 'meaning': '助手；帮手'},
    'sheepishly': {'pos': 'adv.', 'meaning': '不好意思地；腼腆地'},
    'exciting': {'pos': 'adj.', 'meaning': '令人兴奋的；刺激的'},
    'shock': {'pos': 'n.', 'meaning': '震惊；惊愕'},
    'rare': {'pos': 'adj.', 'meaning': '罕见的；难得的'},
    'flock': {'pos': 'n.', 'meaning': '（鸟）群'},
    'silvery': {'pos': 'adj.', 'meaning': '银色的；银白的'},
    'searched': {'word': 'search', 'pos': 'v.', 'meaning': '寻找；搜寻'},
    'exactly': {'pos': 'adv.', 'meaning': '恰好；正是'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(20, OVERRIDES)
