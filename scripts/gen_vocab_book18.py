#!/usr/bin/env python3
"""Book 18 vocabulary cards.

OVERRIDES fix ECDICT's wrong headword/pos/meaning for specific surfaces, each
checked against its Book 18 sentence.  Verb surfaces get a base-form headword +
pos 'v.'; verbforms_vocab then fills the inflections.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch1 — Teddy's Back!
    'floppy': {'pos': 'adj.', 'meaning': '松软下垂的；耷拉着的'},
    'scruffy': {'pos': 'adj.', 'meaning': '脏兮兮的；邋遢的'},
    'mission': {'pos': 'n.', 'meaning': '任务；使命'},
    'spell': {'pos': 'n.', 'meaning': '魔咒；咒语'},
    'wagged': {'word': 'wag', 'pos': 'v.', 'meaning': '摇动（尾巴）；摆动'},
    'swooped': {'word': 'swoop', 'pos': 'v.', 'meaning': '俯冲；猛扑'},
    'ladder': {'pos': 'n.', 'meaning': '梯子'},
    'prairie': {'pos': 'n.', 'meaning': '大草原'},
    'sighed': {'word': 'sigh', 'pos': 'v.', 'meaning': '叹气；叹息'},
    # ch2 — Ocean of Grass
    'buckskin': {'pos': 'n.', 'meaning': '鹿皮；鹿皮衣'},
    'fringed': {'pos': 'adj.', 'meaning': '带流苏的；有缘饰的'},
    'vast': {'pos': 'adj.', 'meaning': '广阔的；巨大的'},
    'whispered': {'word': 'whisper', 'pos': 'v.', 'meaning': '（风）沙沙作响；低声说'},
    'ocean': {'pos': 'n.', 'meaning': '海洋；一大片'},
    'tickled': {'word': 'tickle', 'pos': 'v.', 'meaning': '使发痒；挠痒'},
    'sneezed': {'word': 'sneeze', 'pos': 'v.', 'meaning': '打喷嚏'},
    'rippling': {'pos': 'adj.', 'meaning': '起伏的；泛起波纹的'},
    'slope': {'pos': 'n.', 'meaning': '斜坡；山坡'},
    # ch3 — Black Hawk
    'grazed': {'word': 'graze', 'pos': 'v.', 'meaning': '吃草；放牧'},
    'tribe': {'pos': 'n.', 'meaning': '部落；部族'},
    'quiver': {'pos': 'n.', 'meaning': '箭袋；箭筒'},
    'arrows': {'word': 'arrow', 'pos': 'n.', 'meaning': '箭'},
    'warrior': {'pos': 'n.', 'meaning': '战士；勇士'},
    'rustled': {'word': 'rustle', 'pos': 'v.', 'meaning': '沙沙作响'},
    'galloped': {'word': 'gallop', 'pos': 'v.', 'meaning': '（马）飞奔；疾驰'},
    'halted': {'word': 'halt', 'pos': 'v.', 'meaning': '停下；停止'},
    'admire': {'pos': 'v.', 'meaning': '钦佩；欣赏'},
    # ch4 — Good Manners
    'brave': {'pos': 'adj.', 'meaning': '勇敢的；无畏的'},
    'glanced': {'word': 'glance', 'pos': 'v.', 'meaning': '瞥一眼；匆匆一看'},
    'beads': {'word': 'bead', 'pos': 'n.', 'meaning': '珠子'},
    'moccasin': {'pos': 'n.', 'meaning': '鹿皮软鞋'},
    'carved': {'word': 'carve', 'pos': 'v.', 'meaning': '雕刻；削制'},
    'pounded': {'word': 'pound', 'pos': 'v.', 'meaning': '捶打；舂'},
    'claws': {'word': 'claw', 'pos': 'n.', 'meaning': '爪子'},
    'strength': {'pos': 'n.', 'meaning': '力量；力气'},
    'gasped': {'word': 'gasp', 'pos': 'v.', 'meaning': '倒吸一口气；喘息'},
    # ch5 — Sunlight and Midnight
    'snarled': {'word': 'snarl', 'pos': 'v.', 'meaning': '龇牙低吼；咆哮'},
    'hide': {'pos': 'n.', 'meaning': '兽皮'},
    'slit': {'pos': 'n.', 'meaning': '狭长的开口；裂缝'},
    'powerful': {'pos': 'adj.', 'meaning': '强大的；有力的'},
    'grip': {'pos': 'v.', 'meaning': '夹紧；紧握'},
    'whoop': {'pos': 'n.', 'meaning': '高喊；欢呼声'},
    'mane': {'pos': 'n.', 'meaning': '（马的）鬃毛'},
    'shadows': {'word': 'shadow', 'pos': 'n.', 'meaning': '影子；阴影'},
    # ch6 — Stampede!
    'herd': {'pos': 'n.', 'meaning': '（兽）群'},
    'bison': {'pos': 'n.', 'meaning': '美洲野牛'},
    'creeping': {'word': 'creep', 'pos': 'v.', 'meaning': '悄悄爬行；蹑手蹑脚地走'},
    'alarmed': {'pos': 'adj.', 'meaning': '受惊的；惊恐的'},
    'stampede': {'pos': 'n.', 'meaning': '（兽群）受惊狂奔'},
    'moaning': {'pos': 'adj.', 'meaning': '呻吟般的；低鸣的'},
    'charged': {'word': 'charge', 'pos': 'v.', 'meaning': '猛冲；冲锋'},
    'shaggy': {'pos': 'adj.', 'meaning': '毛发蓬乱的；毛茸茸的'},
    'dodging': {'word': 'dodge', 'pos': 'v.', 'meaning': '躲闪；避开'},
    # ch7 — White Buffalo Woman
    'medicine': {'pos': 'n.', 'meaning': '（印第安文化中的）神力；药'},
    'escape': {'pos': 'v.', 'meaning': '逃脱；逃离'},
    'disappeared': {'word': 'disappear', 'pos': 'v.', 'meaning': '消失；不见'},
    'bounding': {'word': 'bound', 'pos': 'v.', 'meaning': '跳跃着跑；蹦跳'},
    'scooped': {'word': 'scoop', 'pos': 'v.', 'meaning': '（用手）舀起；一把抱起'},
    'licked': {'word': 'lick', 'pos': 'v.', 'meaning': '舔'},
    'spirit': {'pos': 'n.', 'meaning': '灵魂；神灵'},
    'ghost': {'pos': 'n.', 'meaning': '鬼魂；幽灵'},
    'peacefully': {'pos': 'adv.', 'meaning': '平静地；安宁地'},
    # ch8 — Sacred Circle
    'sternly': {'pos': 'adv.', 'meaning': '严厉地；严肃地'},
    'pride': {'pos': 'n.', 'meaning': '骄傲；自负'},
    'frightened': {'word': 'frighten', 'pos': 'v.', 'meaning': '使惊吓；吓唬'},
    'courage': {'pos': 'n.', 'meaning': '勇气；胆量'},
    'drum': {'pos': 'n.', 'meaning': '鼓'},
    'twilight': {'pos': 'n.', 'meaning': '暮色；黄昏'},
    'sacred': {'pos': 'adj.', 'meaning': '神圣的'},
    'messenger': {'pos': 'n.', 'meaning': '信使；使者'},
    'ceremony': {'pos': 'n.', 'meaning': '仪式；典礼'},
    # ch9 — Lakota School
    'dawn': {'pos': 'n.', 'meaning': '黎明；拂晓'},
    'strapped': {'word': 'strap', 'pos': 'v.', 'meaning': '用带子捆绑'},
    'poles': {'word': 'pole', 'pos': 'n.', 'meaning': '长杆；杆子'},
    'platform': {'pos': 'n.', 'meaning': '平台；托架'},
    'stuffed': {'word': 'stuff', 'pos': 'v.', 'meaning': '塞进；填满'},
    'rawhide': {'pos': 'n.', 'meaning': '生牛皮'},
    'belongs': {'word': 'belong', 'pos': 'v.', 'meaning': '属于'},
    'journey': {'pos': 'n.', 'meaning': '旅程；旅行'},
    'vanish': {'pos': 'v.', 'meaning': '消失；绝迹'},
    # ch10 — Good Medicine
    'flooded': {'word': 'flood', 'pos': 'v.', 'meaning': '（光线）涌入；充满'},
    'feather': {'pos': 'n.', 'meaning': '羽毛'},
    'tilted': {'word': 'tilt', 'pos': 'v.', 'meaning': '倾斜；歪（头）'},
    'distance': {'pos': 'n.', 'meaning': '远处；距离'},
    'porch': {'pos': 'n.', 'meaning': '门廊'},
    'gusted': {'word': 'gust', 'pos': 'v.', 'meaning': '（风）猛刮；阵阵吹'},
    'branches': {'word': 'branch', 'pos': 'n.', 'meaning': '树枝'},
    'waved': {'word': 'wave', 'pos': 'v.', 'meaning': '挥动；摇摆'},
    'related': {'pos': 'adj.', 'meaning': '相关的；有亲缘关系的'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(18, OVERRIDES)
