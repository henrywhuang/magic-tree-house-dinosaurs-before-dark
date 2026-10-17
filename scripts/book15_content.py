#!/usr/bin/env python3
"""Book 15 (Viking Ships at Sunrise / 日出时的维京战船) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text has no bilingual word lists, so the standard/extension lists are
curated from the story (grade-5 appropriate, each word verified to occur in its
chapter).  Character design stays consistent with earlier books — Jack: 深色蓬松
短发、戴圆眼镜；Annie: 棕色马尾 — here both dressed in simple medieval hooded
robes/cloaks in a seaside Irish monastery, where Viking raiders attack at dawn.
"""

TITLES = [
    'Before Dawn', 'The Steep Climb', 'Brother Patrick', 'Books of Wonder', 'Warships on the Waves',
    'The Vikings Are Coming!', 'Fogbound', 'Lost at Sea', 'Sea Monster!', 'Sunrise',
]

# First paragraph of reader page 2 and page 3 — verbatim substrings, quotes ignored.
SCENE_ANCHORS = [
    ('Just then something fell in front of them.',
     'Morgan pulled a book from her robe.'),
    ('Jack read more in the Ireland book.',
     'Just then something fell from above.'),
    ('The man smiled again.',
     'Jack looked at the misty gray sea.'),
    ('The hut was warm and peaceful, yet very alive. It glowed with the golden light of many candles.',
     'The old monk looked up at Jack and Annie.'),
    ('No one spoke as the great, fiery ball rose slowly over the ocean.',
     'Jack hurried out the gate. Before he went further, he stopped and pulled out his notebook.'),
    ('The fog blanketed the whole island. Jack and Annie could barely see the path to the monastery.',
     'The monks ran into the library. Brother Patrick turned to Jack and Annie.'),
    ('Jack and Annie crept closer to the ships.',
     'He pushed himself up and onto the ship’s deck.'),
    ('She grabbed one of the oars. She could barely lift it.',
     'Jack smiled. He didn’t know how Annie could be braver than she already was.'),
    ('Jack turned. The great serpent was pressing its long neck against the back of the ship, pushing it toward the shore.',
     'The Vikings shouted and started down the steep stairs.'),
    ('Morgan smiled.',
     'The sky was turning pink and gold.'),
]

SCENES = [
    [
        ('黎明前醒来', '天还没亮，5点的灰蓝微光透进窗，深色蓬松短发、戴圆眼镜的 Jack 从床上坐起，想着今天要去一千多年前维京海盗横行的古爱尔兰，棕色马尾的 Annie 已在门口穿戴整齐。'),
        ('雾林登树屋', '浓雾缠绕着 Frog Creek 黑黢黢的树林，一架绳梯忽然从雾中的魔法树屋垂落，Jack 和 Annie 抓住绳梯，穿过湿冷的空气爬进树屋。'),
        ('摩根的谜题', '树屋角落坐着白发女巫摩根，脚边放着罗马卷轴与中国竹简，她递来写着神秘拉丁文的纸条和《古爱尔兰》，Annie 指着封面许愿，树屋越转越快，归于寂静。'),
    ],
    [
        ('换上中世纪衣裳', '树屋里光线灰暗，棕色马尾的 Annie 低头发现自己穿上了长及脚踝的粗布长裙、腰间挂着小钱袋，戴圆眼镜的 Jack 则一身厚羊毛衣裤、背着皮袋，翻着《古爱尔兰》。'),
        ('悬崖与大海', '树屋竟落在爱尔兰海边的悬崖上，二十英尺下是嶙峋礁石，海浪拍打，海鸥在灰蒙蒙的海面上盘旋，崖壁上凿着一道陡峭的石阶通向浓雾。'),
        ('陡阶垂下绳索', 'Annie 提着裙子踩上湿滑的石阶，险些被裙摆绊倒，一根粗绳忽然从崖顶垂下，她抓住绳子慢慢向上爬，Jack 在下面紧张地叮嘱她一定小心。'),
    ],
    [
        ('遇见帕特里克修士', '崖顶上站着一位身穿棕色长袍的修士，红润的圆脸、光头只剩一圈头发，蓝眼睛闪着笑意，把刚爬上来的 Jack 逗称作“又一个小入侵者”，Jack 连忙解释他们并无恶意。'),
        ('亮出图书卡', '灰白晨光里，Jack 和 Annie 掏出刻着 M 和 L 的秘密图书卡给帕特里克看，修士低头行礼，郑重地说“欢迎你们，我的朋友”，两人也连声道谢。'),
        ('维京海盗的警告', '帕特里克望着迷雾笼罩的灰色大海，讲起船头雕着蛇形怪首的维京战船，一旦看见就必须躲藏，否则会被掳为奴隶；远处教堂尖顶下低沉的钟声响起。'),
    ],
    [
        ('蜂窝石屋修道院', '石墙环绕的修道院里，有挂着钟的小教堂、菜园和六座像巨大蜂窝的圆顶石屋，帕特里克领着 Jack 和 Annie 走到面包房门口，修士正从低矮石炉里取出烤好的扁面包。'),
        ('烛光里的图书室', '最大的蜂窝石屋温暖静谧、被无数烛火映成金色，修士们围着木桌读书、下棋、写字绘画，Annie 惊喜地小声说“这就是文明”，戴圆眼镜的 Jack 也爱上了这里。'),
        ('迈克尔的手抄本', '老修士迈克尔用鹅毛笔在羊皮纸上绘着蓝色花边，书封镶着红蓝宝石，页页是华丽的字体和精致彩绘；他指着页顶那行拉丁文——正是 Jack 他们要找的故事。'),
    ],
    [
        ('故事尚未完成', '迈克尔修士的手抄本还没画完，帕特里克说他们必须改日再来取，Jack 和 Annie 一脸失望，又担心没有故事就回不了家；院里教堂钟声响起，唤修士们去做日出祷告。'),
        ('海上日出', '帕特里克领着两人走进菜园，地平线泛起粉紫的霞光，火红的太阳缓缓从大海尽头升起，修士轻声祷告“太阳的光啊，照耀这充满奇迹的一天”，Annie 看得入迷。'),
        ('地平线上的战船', '顺着绳子爬下悬崖时，海鸥凄厉地盘旋鸣叫像在示警；Jack 回望地平线，心脏几乎停跳——一艘、又两艘扬着风帆的维京龙头战船，蛇形船首在朝阳中闪着寒光。'),
    ],
    [
        ('冲上崖顶报信', '浓云遮住太阳，大雾渐渐吞没海上的龙头战船，Jack 顾不上用绳子，双手攀着陡峭石阶飞快向上爬，要去给修士们报信，Annie 也从树屋跟着爬了上来。'),
        ('敲响警钟', '白雾笼罩整座小岛，Jack 和 Annie 冲到修道院门口，Annie 用力拉响钟绳“当！当！”，修士们从教堂涌出，帕特里克红润的脸瞬间煞白：“快！把书都藏起来！”'),
        ('迈克尔托付手抄本', '帕特里克指点他们走两块大石之间的小路下到海边、别走会被海盗攀爬的石阶；颤巍巍的迈克尔修士捧着镶宝石的爱尔兰故事集追来塞给他们，Jack 小心地收进皮袋。'),
    ],
    [
        ('迷雾中下崖', '海鸥在浓雾里刺耳地尖叫，Jack 和 Annie 一步一挪地摸下陡峭崖径，Annie 脚下一滑撞到 Jack，碎石哗啦滚落崖下，两人终于踩上海边一片平坦的卵石滩。'),
        ('维京战士', '雾中浮现三艘拴在嶙峋礁石上的龙头战船，风帆落下、空无一人随浪轻晃；忽然一群黄发维京战士出现，铁盔下垂着长发，握着圆木盾、长剑和斧头，正仰望着崖顶。'),
        ('藏进战船漂向海', '两人决定躲进船舷最低的小战船，Jack 蹚过冰冷浅水爬上甲板，船却猛地一晃；Annie 蹚水时长裙太重沉了下去，抓住船绳一手一手挪来，Jack 拉她上船，绳子一松，战船滑向大海。'),
    ],
    [
        ('漂进茫茫大海', 'Annie 摔在船板上，小战船已驶入白茫茫的大海，怎么也看不见小岛；戴圆眼镜的 Jack 翻开研究书，指着维京战船的插图，念着船桨、划手和储物箱的说明。'),
        ('戴上维京头盔', 'Annie 不肯放弃，两人各拖着沉重的长桨坐到相对的储物箱上；她从箱里翻出两顶小小的维京头盔，一人一顶戴上，觉得自己勇敢了许多，准备划船。'),
        ('风暴中的海怪', '狂风骤起，湍急的水流把长桨从 Jack 手中卷走，暴雨倾盆、电闪雷鸣，海水灌进船舷；巨浪扑来之际，Jack 高举镶宝石的手抄本大喊“故事救救我们”，一条巨大海蛇从浪中升起。'),
    ],
    [
        ('巨大的海蛇', '海蛇的头越升越高，脖子有两层楼那么高，碧绿的鳞片沾满海藻黏液；Jack 吓得大喊“走开”，Annie 却喊“别走，救救我们”，海蛇滑近战船，Jack 连忙低头躲闪。'),
        ('海蛇推船靠岸', '巨蛇把长长的脖子抵住船尾，一路把战船推向岸边；风渐渐平息，乌云散开，海面在阳光下闪着金光，Jack 望见崖边礁石上的魔法树屋，心里重新燃起希望。'),
        ('逃回树屋', '海蛇最后一推把船搁上沙洲，它扬起脖子、粉绿鳞片闪光，朝 Annie 点了点头潜入海中；两个维京人却出现在崖顶追下石阶，Jack 和 Annie 爬进树屋许愿回家，树屋飞速旋转起来。'),
    ],
    [
        ('带回失落之书', '回到 Frog Creek 的树屋，重新穿上牛仔裤的 Jack 把迈克尔修士镶宝石的手抄本递给摩根，白发女巫轻抚闪亮的书封感叹“真是伟大的艺术”，把它放在罗马卷轴和中国竹简旁。'),
        ('怪物也能是英雄', '摩根讲起这是古爱尔兰巨蛇萨尔夫的传说，说怪物和维京人有时也能成为英雄，修道院的图书室曾是黑暗时代的一束光；她感谢 Jack 和 Annie 的勇气，称他们也是英雄。'),
        ('又一个日出', '摩根让他们回家歇息，并约定两周后再去古希腊寻找另一本失落的书；粉金色的天空下，Jack 和 Annie 穿过树林奔回家，Jack 望着红日升起，轻声念“太阳的光啊，照耀这充满奇迹的一天”。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['ancient', 'whisper', 'damp', 'scroll', 'robe'], ['mysterious', 'research', 'dangle']),
    (['steep', 'cliff', 'leather', 'monk', 'notebook'], ['slippery', 'vanish', 'glide']),
    (['invader', 'serpent', 'island', 'coast', 'fierce', 'monastery'], ['stammer', 'prow']),
    (['bakery', 'oven', 'library', 'candle', 'myth', 'jewel'], ['gleam', 'quill']),
    (['horizon', 'fiery', 'ocean', 'voyage', 'gull', 'ledge'], ['clutch', 'blaze']),
    (['warn', 'scramble', 'fog', 'gather', 'cave', 'haste'], ['yank', 'hobble']),
    (['screech', 'warrior', 'helmet', 'shield', 'shallow', 'pebble'], ['creep', 'jagged']),
    (['deck', 'oar', 'row', 'crew', 'thunder', 'lightning'], ['current', 'crawl']),
    (['scale', 'slime', 'glitter', 'monster', 'duck', 'gasp'], ['rear', 'dive']),
    (['courage', 'hero', 'civilization', 'sparkle', 'sigh', 'porch'], ['enchantress', 'thrill']),
]
