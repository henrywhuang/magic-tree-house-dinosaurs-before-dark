#!/usr/bin/env python3
"""Book 19 vocabulary cards.

OVERRIDES fix ECDICT's wrong headword/pos/meaning for specific surfaces, each
checked against its Book 19 sentence.  Verb surfaces get a base-form headword +
pos 'v.'; verbforms_vocab then fills the inflections.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    # ch1 — How Far Away?
    'brave': {'pos': 'adj.', 'meaning': '勇敢的；无畏的'},
    'peeking': {'word': 'peek', 'pos': 'v.', 'meaning': '偷看；探出头来'},
    'glowed': {'word': 'glow', 'pos': 'v.', 'meaning': '发光；发亮'},
    'ladder': {'pos': 'n.', 'meaning': '梯子'},
    'sneezed': {'word': 'sneeze', 'pos': 'v.', 'meaning': '打喷嚏'},
    'spell': {'pos': 'n.', 'meaning': '魔咒；咒语'},
    'research': {'pos': 'n.', 'meaning': '研究；资料查找'},
    # ch2 — Kah and Ko
    'screeching': {'pos': 'n.', 'meaning': '尖叫声；刺耳的叫声'},
    'creatures': {'word': 'creature', 'pos': 'n.', 'meaning': '生物；动物'},
    'peered': {'word': 'peer', 'pos': 'v.', 'meaning': '凝视；盯着看'},
    'parkas': {'word': 'parka', 'pos': 'n.', 'meaning': '派克大衣；连帽防寒外套'},
    'chattered': {'word': 'chatter', 'pos': 'v.', 'meaning': '（猴子）吱吱叫；喋喋不休'},
    'twinkled': {'word': 'twinkle', 'pos': 'v.', 'meaning': '闪烁；闪闪发亮'},
    'scampered': {'word': 'scamper', 'pos': 'v.', 'meaning': '蹦蹦跳跳地跑；奔跑'},
    'peacocks': {'word': 'peacock', 'pos': 'n.', 'meaning': '孔雀'},
    'gashes': {'word': 'gash', 'pos': 'n.', 'meaning': '深长的划痕；深口子'},
    # ch3 — Life or Death
    'growl': {'pos': 'n.', 'meaning': '低吼声；咆哮声'},
    'twilight': {'pos': 'n.', 'meaning': '暮色；黄昏'},
    'slithering': {'word': 'slither', 'pos': 'v.', 'meaning': '蜿蜒滑行；爬行'},
    'python': {'pos': 'n.', 'meaning': '蟒蛇；巨蟒'},
    'prey': {'pos': 'n.', 'meaning': '猎物'},
    'squeezes': {'word': 'squeeze', 'pos': 'v.', 'meaning': '挤压；勒紧'},
    'swallow': {'pos': 'v.', 'meaning': '吞下；咽下'},
    # ch4 — Swing Time
    'vine': {'pos': 'n.', 'meaning': '藤蔓；藤条'},
    'roar': {'pos': 'n.', 'meaning': '吼叫声；咆哮'},
    'blazed': {'word': 'blaze', 'pos': 'v.', 'meaning': '（眼睛）冒火；闪耀'},
    'daggers': {'word': 'dagger', 'pos': 'n.', 'meaning': '匕首；短剑'},
    'crunching': {'word': 'crunch', 'pos': 'v.', 'meaning': '嘎吱嘎吱地嚼'},
    'gloom': {'pos': 'n.', 'meaning': '昏暗；幽暗'},
    'herd': {'pos': 'n.', 'meaning': '（兽）群'},
    'munched': {'word': 'munch', 'pos': 'v.', 'meaning': '大声咀嚼；津津有味地嚼'},
    # ch5 — Night Walk
    'escape': {'pos': 'v.', 'meaning': '逃脱；逃离'},
    'rumbling': {'pos': 'adj.', 'meaning': '隆隆作响的'},
    'wrinkled': {'pos': 'adj.', 'meaning': '有皱纹的；起皱的'},
    'fireflies': {'word': 'firefly', 'pos': 'n.', 'meaning': '萤火虫'},
    'chill': {'pos': 'n.', 'meaning': '寒意；凉意'},
    'spine': {'pos': 'n.', 'meaning': '脊柱；脊梁'},
    'moaning': {'pos': 'n.', 'meaning': '呻吟声；哀鸣'},
    'rhythm': {'pos': 'n.', 'meaning': '节奏；节拍'},
    'drifting': {'word': 'drift', 'pos': 'v.', 'meaning': '漂流；（意识）恍惚飘移'},
    # ch6 — Swamp Creature
    'stream': {'pos': 'n.', 'meaning': '小溪；溪流'},
    'breeze': {'pos': 'n.', 'meaning': '微风；轻风'},
    'weird': {'pos': 'adj.', 'meaning': '奇怪的；怪异的'},
    'rhinoceros': {'pos': 'n.', 'meaning': '犀牛'},
    'endangered': {'pos': 'adj.', 'meaning': '濒临灭绝的；濒危的'},
    'poachers': {'word': 'poacher', 'pos': 'n.', 'meaning': '偷猎者'},
    'swamp': {'pos': 'n.', 'meaning': '沼泽'},
    'grunted': {'word': 'grunt', 'pos': 'v.', 'meaning': '发出呼噜声；咕哝'},
    # ch7 — Trapped!
    'trap': {'pos': 'n.', 'meaning': '陷阱；捕兽夹'},
    'struggling': {'word': 'struggle', 'pos': 'v.', 'meaning': '挣扎；奋力'},
    'steel': {'pos': 'n.', 'meaning': '钢；钢铁'},
    'species': {'pos': 'n.', 'meaning': '物种；种类'},
    'extinction': {'pos': 'n.', 'meaning': '灭绝；绝种'},
    'majestic': {'pos': 'adj.', 'meaning': '威严的；雄伟的'},
    'lever': {'pos': 'n.', 'meaning': '杠杆；控制杆'},
    'tiptoeing': {'word': 'tiptoe', 'pos': 'v.', 'meaning': '踮着脚走'},
    'snarled': {'word': 'snarl', 'pos': 'v.', 'meaning': '龇牙低吼；咆哮'},
    # ch8 — Wonder Dog
    'clapped': {'word': 'clap', 'pos': 'v.', 'meaning': '拍（手）；鼓掌'},
    'silence': {'pos': 'n.', 'meaning': '寂静；沉默'},
    'disappeared': {'word': 'disappear', 'pos': 'v.', 'meaning': '消失；不见'},
    'wonder': {'pos': 'n.', 'meaning': '奇迹；令人惊叹的人或物'},
    'scruffy': {'pos': 'adj.', 'meaning': '脏兮兮的；邋遢的'},
    'scooped': {'word': 'scoop', 'pos': 'v.', 'meaning': '（用手）舀起；一把抱起'},
    'wild': {'pos': 'adj.', 'meaning': '野生的；野性的'},
    'shimmered': {'word': 'shimmer', 'pos': 'v.', 'meaning': '闪烁微光；粼粼发光'},
    # ch9 — The Hermit
    'stroked': {'word': 'stroke', 'pos': 'v.', 'meaning': '抚摸；轻抚'},
    'blind': {'pos': 'adj.', 'meaning': '失明的；瞎的'},
    'nature': {'pos': 'n.', 'meaning': '大自然；天性'},
    'petals': {'word': 'petal', 'pos': 'n.', 'meaning': '花瓣'},
    'lotus': {'pos': 'n.', 'meaning': '莲花；荷花'},
    'graceful': {'pos': 'adj.', 'meaning': '优雅的；优美的'},
    'savage': {'pos': 'adj.', 'meaning': '凶猛的；野性的'},
    'complete': {'pos': 'adj.', 'meaning': '完整的；齐全的'},
    # ch10 — Who Are You, Really?
    'blossom': {'pos': 'n.', 'meaning': '花朵；花'},
    'shrugged': {'word': 'shrug', 'pos': 'v.', 'meaning': '耸肩'},
    'tilted': {'word': 'tilt', 'pos': 'v.', 'meaning': '倾斜；歪（头）'},
    'secrets': {'word': 'secret', 'pos': 'n.', 'meaning': '秘密'},
    'squirrels': {'word': 'squirrel', 'pos': 'n.', 'meaning': '松鼠'},
    'tame': {'pos': 'adj.', 'meaning': '温驯的；驯服的'},
    'daylight': {'pos': 'n.', 'meaning': '日光；天光'},
    'crickets': {'word': 'cricket', 'pos': 'n.', 'meaning': '蟋蟀'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(19, OVERRIDES)
