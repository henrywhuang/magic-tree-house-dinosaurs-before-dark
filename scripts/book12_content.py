#!/usr/bin/env python3
"""Book 12 (Polar Bears Past Bedtime / 雪原上的北极熊) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text has no bilingual word lists, so the standard/extension lists are
curated from the story (grade-5 appropriate, each word verified to occur in its
chapter).  Character design stays consistent with earlier books — Jack: 深色蓬松
短发、戴圆眼镜；Annie: 棕色马尾 — here both bundled in sealskin fur parkas over
pajamas for the Arctic.
"""

TITLES = [
    'Are You Serious?', 'The Howling', 'Mush!', 'Snow House', "You're It!",
    'Flying Bears', 'Spirit Lights', 'Riddle Solved', 'Oh, No, One More!', 'Master Librarians',
]

# First paragraph of reader page 2 and page 3 — verbatim substrings, quotes ignored.
SCENE_ANCHORS = [
    ('Jack and Annie stepped between the trees.',
     'Morgan pulled a fourth scroll from the folds of her robe.'),
    ('Jack took out his notebook.',
     'The howling grew louder.'),
    ('The seal hunter was giving Annie a pair of fur pants.',
     'The seal hunter was standing beside a dogsled.'),
    ('The seal hunter looked up.',
     'The hunter just laughed, then turned back to his cooking.'),
    ('They ran over the white tundra until they came to the frozen sea.',
     'Jack rolled onto his side and tried to stand.'),
    ('Then the polar bear stretched out her four legs and lay on the ice.',
     'He lay on his stomach. He spread out his arms and legs.'),
    ('Jack scrambled to his feet.',
     'At that moment, the sky exploded.'),
    ('Howling filled the night as the dogsled came into view.',
     'Jack pulled the bear masks out of his backpack.'),
    ('Annie grabbed the Pennsylvania book that always took them home.',
     'They began unrolling the scrolls.'),
    ('The wooden card was as thin and smooth as an ordinary library card.',
     'Jack and Annie climbed down the rope ladder.'),
]

SCENES = [
    [
        ('窗外的雪鸮', '深夜卧室里，深色蓬松短发、戴圆眼镜的 Jack 打着手电，望向窗外树枝上一只睁着大黄眼睛、不停“呼呼”叫的白色雪鸮。'),
        ('树林里见摩根', '月光下的 Frog Creek 树林，Jack 和棕色马尾的 Annie 爬上绳梯，白发飘飘的女巫摩根微笑递来一卷古老卷轴和一本《北极历险》。'),
        ('许愿去北极', 'Jack 和 Annie 盯着《北极历险》封面上的冰雪世界，Annie 指着封面许愿，起风了，树屋越转越快，一切归于绝对的寂静。'),
    ],
    [
        ('冰天雪地的树屋', '灰暗天空下，树屋落在一望无际的冰原上，穿着睡衣的 Jack 和 Annie 冻得瑟瑟发抖、牙齿打颤，一起念着卷轴上的谜语。'),
        ('研究海豹猎人', '戴圆眼镜的 Jack 翻开《北极历险》，指着书里穿海豹皮连帽大衣的猎人插图给 Annie 看，两人搓着手取暖。'),
        ('狼嚎与猎人现身', '风雪弥漫中一阵狼嚎由远及近，Jack 和 Annie 缩在树屋角落，一张被毛皮兜帽围住的脸忽然出现在树屋窗口——正是海豹猎人。'),
    ],
    [
        ('猎人送来毛皮衣', '树屋窗口，海豹猎人递进海豹皮连帽大衣，深色蓬松短发的 Jack 和棕色马尾的 Annie 高兴地套上暖和的皮袄。'),
        ('雪橇犬队', '雪地里，海豹猎人站在一架狗拉雪橇旁，一群西伯利亚哈士奇汪汪叫着，Annie 已经站上雪橇后方招手。'),
        ('“驾！”飞驰而去', '猎人甩响长鞭大喊“驾”，哈士奇拉着雪橇在扬起的雪雾中飞奔，雪鸮在他们头顶盘旋。'),
    ],
    [
        ('月下的圆顶冰屋', '月光照亮冻原上一座小小的圆顶冰屋，狗拉雪橇缓缓停下，戴圆眼镜的 Jack 和棕色马尾的 Annie 跟着海豹猎人走近冰屋。'),
        ('冰屋里煮海豹肉', '冰屋里胖胖的蜡烛跳动着影子，Jack 和 Annie 坐在铺着毛皮的台子上，看海豹猎人在小炉子上化雪、煮肉。'),
        ('北极熊面具', '海豹猎人从毛皮台子下取出两张北极熊木雕面具，钝钝的鼻子、圆圆的耳朵；Jack 和 Annie 好奇地凑近端详。'),
    ],
    [
        ('两只北极熊宝宝', '月光下的雪原上，两只圆滚滚的北极熊幼崽打着滚玩耍，棕色马尾、穿毛皮袄的 Annie 笑着朝它们跑去，哈士奇在一旁狂吠。'),
        ('和熊宝宝玩“你来追”', '雪白的冻原上，Jack、Annie 和两只熊宝宝互相追逐嬉戏，又一起顺着雪坡滑到结冰的海面上。'),
        ('冰面裂开', '结冰的海面上响起“咔嚓”裂纹声，Jack 和 Annie 吓得趴在冰上不敢动，两只熊宝宝紧紧挨过来，一头巨大的北极熊正低吼着走来。'),
    ],
    [
        ('熊妈妈的绝技', '月夜结冰的海边，巨大的北极熊妈妈把四条腿摊开、贴着冰面缓缓爬行分散重量，戴熊面具的 Jack 和 Annie 屏息看着。'),
        ('戴上熊面具', 'Jack 摘下圆眼镜戴上北极熊木面具，Annie 也戴上，两人透过面具的眼孔望着熊妈妈把幼崽驮上背、贴冰滑走。'),
        ('像熊一样“飞”', 'Jack 趴在冰上摊开手脚，学着熊妈妈的样子一推一滑，月光洒在雪原上，他觉得自己像一只在飞翔的北极熊。'),
    ],
    [
        ('感谢北极熊之灵', '安全的冻原上，戴着北极熊面具的 Jack 和 Annie 朝坐在不远处守望的熊妈妈鞠躬，双臂张开旋转，郑重道谢。'),
        ('北极光爆发', '夜空骤然炸开一片红、绿、紫的绚烂极光，如巨大的漩涡在雪原上流动闪烁，Jack 和 Annie 仰头看得屏住了呼吸。'),
        ('寻找科学解释', '在极光的绿光里，戴圆眼镜的 Jack 从背包里翻出《北极历险》，指着书里北极光的插图对 Annie 说这是有科学道理的。'),
    ],
    [
        ('雪橇归来', '月光冻原上狼嚎般的犬吠由远及近，海豹猎人跟着雪橇跑来，Jack 和 Annie 挥手大喊朝雪橇奔去。'),
        ('猜出谜底“面具”', 'Jack 掏出笔记本大声念摩根的谜语，忽然和 Annie 一起喊出答案——“面具”！海豹猎人微笑点头。'),
        ('还面具、坐雪橇回家', 'Jack 把两张北极熊面具还给海豹猎人，猎人把面具收进皮袄，三人登上雪橇，喊着“驾”朝黑暗的冰面出发。'),
    ],
    [
        ('暴风雪中的树屋', '狂风暴雪拍打着落在冰原上的树屋，Jack 和 Annie 脱下海豹皮衣从窗口递还给雪地里的海豹猎人，冻得直发抖。'),
        ('许愿却没反应', 'Annie 举着带他们回家的宾州小书指着封面许愿，可树屋一动不动，冰冷的风雪灌进树屋，两人急得团团转。'),
        ('拼出谜底“HOME”', 'Jack 和 Annie 摊开四卷卷轴：OYSTER、ECHO、HONEY、MASK，盯着首字母 O-E-H-M，忽然重组成 HOME——他们最爱的地方！'),
    ],
    [
        ('成为图书管理大师', '温暖的树屋里，白发女巫摩根现身，把两张薄薄光滑的木质魔法图书卡分别递给深色蓬松短发的 Jack 和棕色马尾的 Annie。'),
        ('魔法图书卡', 'Jack 和 Annie 捧着刻着神秘字样的木卡惊叹不已，摩根叮嘱他们把卡带上未来的旅程，只交给真正需要帮助的人。'),
        ('回到温暖的家', 'Jack 和 Annie 爬下绳梯，穿过不再阴森的树林，望见远处亮着门廊灯、洒满月光的家，轻声说“到家了”。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['owl', 'flashlight', 'wondered', 'whispered', 'ancient', 'scroll'], ['enchantress', 'Arctic']),
    (['crisp', 'shivered', 'chattering', 'courage', 'hunter'], ['sealskin', 'howling']),
    (['puzzled', 'parka', 'mittens', 'dogsled', 'whip'], ['huskies', 'drifting']),
    (['tundra', 'igloo', 'temperature', 'candle', 'ceremony', 'spirit'], ['platform', 'blunt']),
    (['cub', 'wrestling', 'snowbank', 'crack', 'snorting'], ['panting', 'tundra']),
    (['whimpered', 'growled', 'paced', 'incredible', 'protect'], ['moan', 'crept']),
    (['awe', 'bowing', 'exploded', 'dazzling', 'shimmered', 'scientific'], ['twirled', 'hushed']),
    (['vast', 'familiar', 'mask', 'brave', 'discover'], ['sighed', 'shrugged']),
    (['blizzard', 'snowstorm', 'shimmering', 'scroll', 'battered'], ['unscramble', 'gaze']),
    (['succeeded', 'quest', 'soothing', 'ordinary', 'mission'], ['tingly', 'cozy']),
]
