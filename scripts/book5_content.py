#!/usr/bin/env python3
"""Shared Book 5 metadata and the three plot scenes used by data and art builds."""

TITLES = [
    'Back into the Woods', 'The Open Book', 'E-hy!', 'Captured',
    'Flames in the Mist', 'Shadow Warrior', 'To the East', 'Dragon Water',
    'Mouse-walk', "'Night, Peanut",
]

# The two anchors start scene 2 and scene 3. They deliberately follow story beats,
# rather than splitting a chapter into three equal word counts.
SCENE_ANCHORS = [
    ('"Come on up!"', 'Jack looked around again.'),
    ('“Look!” Annie pointed', '“Let\'s go!” said Annie.'),
    ('Jack pushed his glasses into place.', '"Jack," whispered Annie.'),
    ('The short ninja darted down', 'The ninjas stopped near the rushing water'),
    ('Suddenly the ninjas froze.', 'Finally the ninjas came to a stop.'),
    ('“Perhaps I can help you,”', '"Can\'t we go with you?"'),
    ('All the trees looked the same.', 'Soon they were out of the pine woods'),
    ('“East!” he said.', 'Peanut climbed out of Annie\'s sweatshirt pouch'),
    ('Jack pushed his glasses into place and stood up.', '“And take this—" said the master.'),
    ('He put the moonstone in his pocket.', 'She put Peanut gently down on the glowing M.'),
]

# Proofread against the chapter vocabulary panels in the supplied OCR source.
VOCABULARY = [
    (['walk', 'library', 'week', 'hard', 'cute', 'old'], ['nor', 'kid', 'cricket', 'scattered', 'plain']),
    (['piece', 'thin', 'maybe', 'only', 'now', 'trouble', 'minute'], ['spine', 'rushing', 'ninja', 'scoop', 'sweatshirt']),
    (['pants', 'shirt', 'scarves', 'enemy', 'Japan', 'neither'], ['pouch', 'grove', 'sword', 'trunk', 'huddle']),
    (['iron', 'note', 'us', 'spider', 'game', 'always'], ['capture', 'spike', 'claw', 'nod', 'web', 'stream']),
    (['full', 'sky', 'mountain', 'sneaker', 'cave'], ['flame', 'pant', 'pine', 'master']),
    (['floor', 'why', 'Japanese', 'family', 'alone', 'practice'], ['warrior', 'mat', 'samurai', 'fighter', 'mercy']),
    (['east', 'nature', 'more', 'stick', 'space', 'direction'], ['stuff', 'moonlight', 'head', 'way', 'bamboo']),
    (['against', 'right', 'left', 'quiet'], ['press', 'swirl', 'weed', 'drown', 'hood']),
    (['mouse', 'cross', 'second', 'fast', 'own'], ['teeny', 'light', 'squeak', 'moonlit', 'helper', 'kiss']),
    (['smooth', 'dinner', 'again', 'pocket', 'bed', 'sleep'], ['night', 'moonstone', 'glow', 'goodnight', 'bump']),
]

SCENES = [
    [
        ('树屋终于回来了', '黄昏里，安妮跑进弗洛格溪树林，杰克追着她来到最高的橡树下，惊喜地发现消失数周的魔法树屋重新出现。'),
        ('发光的 M 与花生米', '树屋里书本散落，地板上的字母 M 微微发光；安妮温柔地摸着一只棕白色小老鼠，杰克在旁观察。'),
        ('摩根的求救纸条', '杰克从木地板上捡起写着求救信息的纸条，神情骤然紧张；安妮抱着小老鼠凑近查看。'),
    ],
    [
        ('残缺的魔法信息', '杰克和安妮在树屋窗口的暮光中研究摩根留下的残缺纸条，试图读懂“解除魔咒、寻找四样东西”的线索。'),
        ('白花山谷里的忍者', '杰克举起一本敞开的书，书页画着开满白花的山林、湍急溪流和两名蒙面忍者，兄妹俩又惊讶又警觉。'),
        ('带着花生米出发', '安妮把小老鼠放进橘红连帽衫的口袋并指向忍者图画，树屋在狂风和飞舞书页中开始旋转。'),
    ],
    [
        ('抵达古代日本', '月光下的树屋落在开满白花的山树上，山谷溪流奔腾；杰克和安妮从窗口偷偷观察岩石旁的两名黑衣忍者。'),
        ('了解影子武士', '杰克蹲在树屋内翻读忍者书并在笔记本记录，安妮和口袋里的花生米安静听着，窗外是古代日本山林。'),
        ('忍者爬上树屋', '两名蒙面忍者戴着带爪铁环像猫一样迅速攀上树干，杰克和安妮匆忙拉起绳梯并缩在树屋角落。'),
    ],
    [
        ('无声的俘虏', '树屋内，两名忍者取下带爪铁环，接过摩根纸条默默对视；勇敢的安妮上前说明来意，杰克紧张站在后方。'),
        ('跟随忍者下山', '暮色染红山谷，杰克和安妮跟随一高一矮两名忍者穿过山路，安妮口袋里的小老鼠探出脑袋。'),
        ('穿越冰冷溪流', '湍急冰冷的山溪中，高个忍者肩扛杰克、矮个女忍者肩扛安妮，稳稳涉水而过，白色浪花环绕他们。'),
    ],
    [
        ('雾中的火把', '满月升起，两名忍者带兄妹攀登岩石山坡；谷底雾中出现一队武士的火把，忍者瞬间警觉。'),
        ('寻找隐秘山洞', '松林月影里忍者突然消失，杰克翻开书查找线索，发现忍者会在隐蔽山洞中秘密集会。'),
        ('洞口的召唤', '两名忍者从树影中返回，向杰克和安妮招手，带他们走向岩壁间被松枝遮掩、透出烛光的黑暗洞口。'),
    ],
    [
        ('烛光中的忍者大师', '幽深山洞里几十支蜡烛照亮草席上的忍者大师；杰克和安妮坐在石地上，花生米从口袋探头。'),
        ('女忍者与战争警报', '忍者大师揭示矮个忍者是女性并拿着摩根纸条；高个忍者突然示警，远处武士火光正逼近山洞。'),
        ('自然法则', '洞外月光下，忍者大师郑重告诉兄妹“利用自然、成为自然、跟随自然”，随后忍者们隐入黑暗，只剩两个孩子。'),
    ],
    [
        ('两个小忍者向东', '杰克和安妮拉紧连帽衫帽绳，像两个小忍者一样在月光松林中悄悄向东行进。'),
        ('用月影辨方向', '林间空地上，安妮把树枝插进泥土，杰克根据月光投下的长影判断东方，两人露出找到办法的喜悦。'),
        ('武士逼近', '岩石山坡上，兄妹躲在巨石后；一名穿竹甲、佩双刀的古代武士从月光中逼近，山下还有成片火把。'),
    ],
    [
        ('像岩石一样安静', '武士从巨石旁搜寻，杰克和安妮紧贴岩面闭眼屏息，想象自己像岩石一样坚固、安静，成功没有被发现。'),
        ('冰水中的险情', '杰克试图涉过狂暴冰冷的溪流却被水流冲倒，紧抓岸边水草；安妮奋力拉住他的双臂。'),
        ('跟随花生米', '小老鼠花生米沿溪岸跑向一根横跨窄河道的月光树枝，杰克和安妮追上来，发现这座天然小桥。'),
    ],
    [
        ('小老鼠式过桥', '杰克和安妮张开双臂、像轻快小老鼠一样快速走过横跨急流的细树枝，到达对岸后倒在草地上大笑。'),
        ('树屋里的忍者大师', '月光白花包围的树屋内，忍者大师抱着花生米等待兄妹，远处武士火把正在山林中逼近。'),
        ('得到月光石', '忍者大师把一枚清澈圆润、微微发光的月光石交给杰克，安妮抱着花生米，三人在旋转前郑重告别。'),
    ],
    [
        ('带着月光石回家', '树屋回到暮色中的弗洛格溪，杰克在掌心凝视发光月光石，安妮和花生米望向远处亮灯的家与呼唤他们的父亲。'),
        ('给花生米做小床', '安妮脱下一只条纹袜，把花生米温柔放进袜子做成的小床；杰克背着背包，露出无奈又温暖的笑。'),
        ('影子武士回家', '安妮把花生米留在发光的 M 和摩根纸条旁，兄妹牵手穿过凉爽黑暗的树林，像两名安静敏捷的影子武士走向家。'),
    ],
]
