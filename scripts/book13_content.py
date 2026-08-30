#!/usr/bin/env python3
"""Book 13 (Vacation Under the Volcano / 庞贝城最后一天) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text has no bilingual word lists, so the standard/extension lists are
curated from the story (grade-5 appropriate, each word verified to occur in its
chapter).  Character design stays consistent with earlier books — Jack: 深色蓬松
短发、戴圆眼镜；Annie: 棕色马尾 — in ordinary modern vacation T-shirts at Frog
Creek, and magically disguised in white Roman tunics + laced sandals once inside
A.D. 79 Pompeii on the day Mount Vesuvius erupts.
"""

TITLES = [
    'A Secret Code', 'The End Is Near', 'Gladiators!', 'Scary Things', 'Books? Books?',
    'The End Is Here', 'The Sky Is Falling', 'Nightmare at Noon', 'Save Us!', 'A Simple Explanation',
]

# First paragraph of reader page 2 and page 3 — verbatim narrative substrings, quotes ignored.
SCENE_ANCHORS = [
    ('They left the sidewalk and headed into the Frog Creek woods.',
     'Morgan handed Jack a book called Life in Roman Times.'),
    ('He threw his notebook and the Roman book into his leather bag.',
     'They kept walking, until they passed a bakery filled with freshly baked flat breads.'),
    ('To his surprise he found a picture of the old woman.',
     'They kept walking, until soon they came to a fancy building with large columns.'),
    ('The woman fixed her gaze on Jack.',
     'Jack took the piece of paper from his bag.'),
    ('Jack trailed behind her.',
     'She was in a garden off the dining room.'),
    ('He put the scroll in the leather bag.',
     'He saw something near the mermaid fountain.'),
    ('Glowing rocks were bursting through the sky above Mount Vesuvius.',
     'They ran from the scroll library into the garden.'),
    ('Jack followed her as they ran past the Temple of Jupiter.',
     'The closer they got to the volcano, the more the ground trembled.'),
    ('At the moment, Jack couldn’t remember anything.',
     'Jack and Annie didn’t stop to ask any questions.'),
    ('Jack reached into his pack.',
     'Jack and Annie started walking through the woods.'),
]

SCENES = [
    [
        ('抽屉里的魔法卡', '清晨卧室里，深色蓬松短发、戴圆眼镜、穿 T恤的 Jack 从抽屉取出薄薄的木质图书卡，指尖摩挲着卡面上闪着微光的“ML”两个字母。'),
        ('树屋里的秘密任务', '古橡树上的魔法树屋里，白发女巫摩根把一张写着神秘拉丁文的纸条递给 Jack 和棕色马尾的 Annie——那是他们要抢救的失落故事的书名。'),
        ('许愿飞往罗马', 'Jack 捧着摩根给的《罗马生活》一书，指着封面上身穿长袍的罗马人许愿，狂风骤起，树屋越转越快，最后一切归于绝对的寂静。'),
    ],
    [
        ('变身罗马孩子', '树屋落在橄榄林里，Jack 和 Annie 惊讶地发现 T恤运动鞋不见了，换成白色束腰长袍和系带凉鞋；林外一侧山峦平缓，另一侧庞贝城在阳光下闪光。'),
        ('走过庞贝街市', '戴圆眼镜的 Jack 和棕色马尾的 Annie 走过石板铺就的热闹街道，两旁店铺摆着大陶罐、挂着肉，酒馆里有人弹琴，热闹得像家乡的集市。'),
        ('女预言者的警告', '喧闹的集市广场上小贩叫卖蜂蜜糕，一个披黑斗篷、白发凌乱的老妇伸出瘦骨嶙峋的手指着 Jack 和 Annie，嘶哑地喊：“末日将至！”'),
    ],
    [
        ('躲在水果摊后', 'Jack 和 Annie 蹲在水果摊后探头张望，戴圆眼镜的 Jack 翻开《罗马生活》，书页上竟印着那个老妇的画像——原来她是能预见未来的预言者。'),
        ('穿过广场找图书馆', '棕色马尾的 Annie 拉着 Jack 穿过人来人往的集市广场，经过一座供人洗浴、游泳、聚会的公共浴场大楼，四处寻找传说中的图书馆。'),
        ('角斗士登场', '一条宽街上，一列肌肉虬结的高大武士戴着华丽头盔、扛着沉重盾牌走来，脚上却拴着锁链，卫兵押送在旁——Jack 低呼：“是角斗士！”'),
    ],
    [
        ('角斗场前受阻', '通往露天角斗场的入口人群欢呼，戴圆眼镜的 Jack 和 Annie 想跟进去，却被罗马卫兵横起长矛拦下；黑斗篷老预言者又出现，嘶声喊“快逃命”。'),
        ('预言者说怪事', '街角，白发老妇死死盯着 Jack，一件件说出可怕的怪象：溪水干涸、鸟群飞走、老鼠逃光、母牛哀鸣、海水滚烫、大地震颤又低语。'),
        ('奔向度假别墅', 'Jack 掏出写着拉丁书名的纸条，老妇瞥见 Annie 图书卡上的微光便明白了，指向街尾一座大别墅；Jack 和 Annie 拔腿朝别墅狂奔。'),
    ],
    [
        ('溜进空别墅', 'Jack 推开别墅大门，两人溜进空荡荡的中庭；戴圆眼镜的 Jack 望着天花板方口下接雨水的石池，Annie 却急着一间间探头喊：“书？书呢？”'),
        ('罗马人的餐厅', '戴圆眼镜的 Jack 挨个房间张望：卧室墙上绘着彩画、地面铺着彩色碎石；餐厅矮桌摆着银盘，三张斜榻堆满靠枕，罗马人竟是躺着进餐。'),
        ('卷轴就是图书馆', '穿过有美人鱼喷泉和棕榈的花园，尽头房间长木架上摆满一卷卷纸卷；Annie 以为没有书，戴圆眼镜的 Jack 却恍然大悟——莎草纸卷轴正是图书馆！'),
    ],
    [
        ('找到拉丁卷轴', '别墅藏书室里，Jack 和 Annie 手忙脚乱地一卷卷展开纸卷比对，终于找到卷首拉丁文与纸条相符的那一卷；Jack 顺手翻书，瞥见火山喷发的插图。'),
        ('今天就是末日', '戴圆眼镜的 Jack 惊恐地读到：维苏威火山将在公元79年8月24日正午喷发——正是今天！他结结巴巴冲棕色马尾的 Annie 大喊：“火山——正午！”'),
        ('日晷指向正午', '别墅花园里，Jack 和 Annie 蹲在美人鱼喷泉旁的日晷前，对照书上插图——正午时日晷几乎没有影子，正是此刻；紧接着一声惊天巨响炸开。'),
    ],
    [
        ('大地剧烈摇晃', '别墅石板露台剧烈震颤，花盆、植物、美人鱼喷泉纷纷砸落，池水泼溅到 Jack 和 Annie 身上；两人跌进藏书室，脚下石地裂开大缝。'),
        ('天空喷落火石', '透过窗口，Jack 和 Annie 看见炽热岩石冲上维苏威火山顶、山头被炸飞；戴圆眼镜的 Jack 读书才知那是轻飘飘的浮石与遮天蔽日的火山灰云。'),
        ('顶靠枕逃出别墅', '火山灰与浮石纷纷落下，Jack 和 Annie 从餐厅斜榻抓起靠枕，用腰带绑在头上当帽子，冲出大门时一股热浪扑面，两人奔进昏暗燃烧的街道。'),
    ],
    [
        ('逃出混乱集市', '维苏威火山喷出烈焰，火石与灰烬如雨落下；集市上购物者、士兵、角斗士、小贩四散奔逃，摊子倒塌、货车打滑，Jack 一时僵在原地。'),
        ('逆着人流奔向火山', 'Jack 和 Annie 跑过石柱倒塌的朱庇特神庙和塌顶的公共浴场；为回到橄榄林的树屋，两人竟迎着冒红云的维苏威火山、逆着逃难人群奔去。'),
        ('大桥不见了', '离火山越近，地面抖得越凶，天色越暗越呛；Jack 呛着臭味、泪眼模糊地跟着 Annie 跑到橄榄林旁干涸的溪边——可过溪的小桥竟消失不见了。'),
    ],
    [
        ('陷进浮石堆', '干涸的溪谷里，浮石像灰雪般堆成厚厚的堆；Jack 和 Annie 滑下河岸想蹚过去，浮石却越落越多，两人越陷越深、动弹不得。'),
        ('大力神显灵相救', '棕色马尾的 Annie 高举古卷向漆黑天空大喊“故事快救我们”，火光一闪，一个比角斗士还高大的巨人应声而现，一手一个把兄妹拎到对岸，低吼“快跑”。'),
        ('冲回魔法树屋', 'Jack 和 Annie 头也不回地穿过橄榄林，跳过断枝与地缝，爬上魔法树屋的绳梯；Annie 举起宾州小书许愿，树屋越转越快，终归于安宁的寂静。'),
    ],
    [
        ('平安回到家乡', '树屋里，累瘫的 Jack 摘下沾满灰的圆眼镜，发现背包和 T恤都回来了；白发女巫摩根在角落现身，微笑说很高兴看到他们平安归来，夸他们勇敢。'),
        ('归还卷轴领新任务', 'Jack 从背包取出蒙尘的古卷交给满怀感激的摩根；摩根许诺两周后送他们去古代中国，随后揭晓卷轴是大力神赫拉克勒斯的失落传说，与树屋一同消失。'),
        ('一个简单的解释', 'Jack 和 Annie 走过树林回家，Annie 说救他们的正是大力神——在相信他的罗马时代他便是真的；Jack 笑着抬头轻声道谢，爸爸在门廊喊他们出发度假。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['secret', 'library', 'whisper', 'wonder', 'nightmare', 'mission'], ['ancient', 'shimmer']),
    (['tunic', 'grove', 'shiver', 'bridge', 'stream', 'shop'], ['tavern', 'cloak']),
    (['fruit', 'peer', 'warn', 'temple', 'shield'], ['soothsayer', 'column', 'incredible']),
    (['strong', 'fight', 'guard', 'cheer', 'spear'], ['gaze', 'chill', 'spine']),
    (['empty', 'ceiling', 'garden', 'pillow', 'scroll'], ['fountain', 'patio', 'papyrus']),
    (['scroll', 'title', 'volcano', 'noon', 'shadow'], ['erupt', 'sundial', 'blast']),
    (['tremble', 'crash', 'roof', 'crack', 'window'], ['pumice', 'lava', 'plaster']),
    (['fire', 'ash', 'rush', 'shout', 'wall'], ['collapse', 'crumble', 'billow']),
    (['snow', 'save', 'story', 'voice', 'flash', 'trap'], ['drift', 'dazed']),
    (['brave', 'home', 'escape', 'famous', 'myth'], ['hoarse', 'grateful', 'mysterious']),
]
