#!/usr/bin/env python3
"""Book 18 (Buffalo Before Breakfast / 早餐前的野牛) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text has no bilingual word lists, so the standard/extension lists are
curated from the story (grade-5 appropriate, each word verified to occur in its
chapter).  Character design stays consistent with earlier books — Jack: 深色蓬松
短发、戴圆眼镜；Annie: 棕色马尾 — here they trade their modern jeans and T-shirts
for Lakota buckskin (Jack in a buckskin shirt/pants and coonskin cap, Annie in a
fringed buckskin dress) on the 1800s Great Plains.
"""

TITLES = [
    "Teddy's Back!", 'Ocean of Grass', 'Black Hawk', 'Good Manners', 'Sunlight and Midnight',
    'Stampede!', 'White Buffalo Woman', 'Sacred Circle', 'Lakota School', 'Good Medicine',
]

# A narrative sentence from reader page 2 (~1/3) and page 3 (~2/3) — verbatim
# substrings, quotes ignored.
SCENE_ANCHORS = [
    ('The small dog wagged his tail joyfully.',
     'Jack and Annie stared at the watch.'),
    ('The tree house sat in a lone tree in a vast golden prairie.',
     'The wind blew gently as Jack hurried after her.'),
    ('He galloped toward them, grabbing his bow.',
     'Black Hawk nudged his pony forward again.'),
    ('Then Jack took off his coonskin cap.',
     'Women and girls pounded meat and sewed clothes.'),
    ('Black Hawk handed his wolf skin to Grandmother.',
     'Jack took a deep breath.'),
    ('He began creeping on all fours toward the buffalo.',
     'A ripple went through the herd as other shaggy animals looked up.'),
    ('Annie turned to Jack and Black Hawk as they rode up to her.',
     'The little dog came bounding out of the grass toward them.'),
    ('The evening shadows spread over the camp.',
     'She put the feather on the ground in front of Jack and Annie.'),
    ('Black Hawk laughed again.',
     'Grandmother, Black Hawk, and the rest of the tribe were watching.'),
    ('Teddy tilted his head and gave Jack a wise look.',
     'But when they turned around, the little dog was gone.'),
]

SCENES = [
    [
        ('小狗回来了', '清晨卧室里，深色蓬松短发、戴圆眼镜的 Jack 系好运动鞋，抬头透过窗户，看见晨光中一只垂着耳朵、棕色乱毛的小狗 Teddy 站在门外，惊喜地喊出它的名字。'),
        ('树屋新任务', 'Frog Creek 树林最高的橡树上，树屋里棕色马尾的 Annie 念出摩根留下的字条——解救 Teddy 需要四件礼物，Jack 拿起第一件：泰坦尼克号的银怀表。'),
        ('许愿去草原', 'Jack 从角落翻出封面画着辽阔草原的《大平原》，指着封面许愿要去那里，风声骤起，树屋越转越快，然后一切归于绝对的寂静。'),
    ],
    [
        ('神奇鹿皮衣', '牛仔裤和 T 恤神奇地变了样：深色蓬松短发、戴圆眼镜的 Jack 穿上鹿皮衬衫长裤、戴起浣熊皮帽，棕色马尾的 Annie 换上一条带流苏的鹿皮裙。'),
        ('无边的草海', '树屋孤零零落在金黄辽阔的大草原上，朝阳初升，风吹过高高的黄草沙沙作响，Jack 和 Annie 望着窗外惊叹：这简直是一片草的海洋。'),
        ('草浪中前行', '棕色马尾的 Annie 抱着小狗 Teddy 在没到胸口的草浪里穿行，戴圆眼镜的 Jack 打着喷嚏跟在后头，走上小坡顶时忽然愣住——前方有惊喜。'),
    ],
    [
        ('草原上的营地', '深色蓬松短发、戴圆眼镜的 Jack 和棕色马尾的 Annie 蹲在草丛里，望着前方一圈鹿皮蒂皮帐篷，马匹在旁吃草，一名背着弓箭的骑手迎着阳光疾驰而来。'),
        ('少年黑鹰', '骑手勒马停住，原来是个十岁上下、骑着小马的拉科塔少年黑鹰 Black Hawk，他放下弓静静打量着微笑的 Annie，答应带他俩去见自己的族人。'),
        ('两指表示朋友', '走近营地时所有人都停下手里的活计盯着他们，戴圆眼镜的 Jack 想起书里的规矩，赶紧和 Annie 一起竖起两根手指，表示我们是朋友。'),
    ],
    [
        ('拜见老祖母', '黑鹰领 Jack 和 Annie 走进一顶画满野牛图案的蒂皮帐篷，中央火塘燃烧着，一位老祖母坐在兽皮上往鹿皮软鞋上缝珠子，抬头望向两位客人。'),
        ('献上皮帽', '深色蓬松短发的 Jack 摘下浣熊皮帽送给老祖母，祖母戴上帽子笑了起来，Jack 和 Annie 也跟着笑，觉得她慈祥得像自己的外婆。'),
        ('帐中钻出狼', '营地里人们忙着刻弓、捶肉、缝衣，忽然小狗 Teddy 冲着帐篷低吼狂吠，一头睁着黄眼睛的巨狼从祖母的帐篷里钻了出来，两人吓得倒吸一口凉气。'),
    ],
    [
        ('披狼皮的黑鹰', '那头“巨狼”竟是披着狼皮的黑鹰，脑袋从狼颈的开口探出，他笑着对 Jack 和 Annie 说：披上狼皮，就能感到狼——野牛最强猎手的力量。'),
        ('午夜与阳光', '黑鹰赶来一黑一黄两匹小马，棕色马尾的 Annie 摸着它们的鼻子叫它们午夜 Midnight 和阳光 Sunlight，教 Jack 抓住鬃毛、夹紧双腿骑上光背马。'),
        ('驰马见牛群', '云影像展翅的黑色巨鸟掠过草原，三人纵马穿行在高高的草丛间，黑鹰的小马在草坡顶停下——山下是成千上万头正在低头吃草的野牛。'),
    ],
    [
        ('潜近野牛群', '不顾祖母告诫、也没披狼皮，黑鹰四肢着地朝野牛群匍匐潜行，戴圆眼镜的 Jack 翻着资料书，紧张地读到：受惊的野牛会掀起可怕的踩踏狂奔。'),
        ('喷嚏惹牛群狂奔', '黑鹰突然“阿嚏”打了个喷嚏，最近的野牛猛地抬头低吼、挺角冲来，成群毛茸茸的野牛被惊动，小狗 Teddy 也跳下来朝牛群狂吠奔去。'),
        ('策马救黑鹰', 'Jack 深吸一口气，夹马冲下山坡在狂奔的野牛间穿行救回黑鹰；山顶另一头，棕色马尾的 Annie 被野牛围住轻声安抚，牛群竟渐渐停下重新吃草。'),
    ],
    [
        ('白野牛女传说', '骑马回到 Annie 身边，棕色马尾的 Annie 满脸惊异地讲述：她被野牛围困、举手大喊“停”，忽然一位身穿白鹿皮裙的美丽女子现身相助，随即消失不见。'),
        ('那是精灵', '黑鹰瞪大了眼睛低声说，那位白衣女子并非人间之人，Annie 见到的是白野牛女的精灵；戴圆眼镜的 Jack 追问：你是说……像鬼魂一样吗？'),
        ('小狗归来', '小狗 Teddy 从草丛里蹦跳着奔回，Annie 一把把它抱起，它舔遍她的脸；黑鹰说必须赶回去把这件事告诉祖母，身后的野牛安然吃着草。'),
    ],
    [
        ('夕阳下营地', '夕阳把一圈蒂皮帐篷映得通红，人们围坐在大火旁；深色蓬松短发的 Jack 和棕色马尾的 Annie 随黑鹰下马走近火堆，老祖母起身迎接他们。'),
        ('万物皆关联', '祖母神情严肃地教导低头认错的黑鹰：骄傲让你逞能，逞能惊了野牛，一环扣一环——万物皆相关联；随后为两人取了拉科塔名字。'),
        ('神圣的圆环', '篝火旁，一位老人把长长的圣烟斗举向天空、指向四方，再在圆环中依次传递；祖母把一根鹰羽放到 Jack 和 Annie 面前，作为奖励勇气的礼物。'),
    ],
    [
        ('拔营追野牛', '黎明微光中，全族人拆下蒂皮帐篷，捆到两根木杆拖成的木架上让马拉着；棕色马尾的 Annie 把野牛肉塞进生牛皮袋，祖母说该跟着野牛迁徙了。'),
        ('处处是学校', '戴圆眼镜的 Jack 问起土地和上学，黑鹰笑着说土地属于大神、无人能占有，学习也不止一处——营地、草原、天空处处都能学到本领与勇气。'),
        ('许愿回家', '与祖母、黑鹰互竖两指道别后，Jack 和 Annie 跑回树屋，望着金色的草海，Jack 举起宾州小书指着 Frog Creek 许愿回家，风起，树屋飞快旋转。'),
    ],
    [
        ('回到家中', '明亮的阳光洒满树屋，Jack 和 Annie 变回牛仔裤和 T 恤，小狗 Teddy 舔着他们的脸；棕色马尾的 Annie 把鹰羽放到摩根字条上，紧挨着泰坦尼克号的银怀表。'),
        ('好药力之谜', 'Annie 猜测 Teddy 和白野牛女有关——它一消失，白衣女子就出现，女子一消失，它又跑回来；戴圆眼镜的 Jack 望着小狗说，也许 Teddy 真有好药力。'),
        ('小狗又消失', '门廊上妈妈和外婆在呼唤，两人想把 Teddy 装进背包带回家，一转身小狗却又无影无踪；风掠过树林，鸟儿飞向蓝天，Jack 心想：万物皆相关联。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['spell', 'mission', 'prairie', 'ladder', 'wag', 'sigh'], ['scruffy', 'floppy', 'swoop']),
    (['vast', 'whisper', 'ocean', 'tickle', 'sneeze', 'slope'], ['buckskin', 'fringe', 'ripple']),
    (['tribe', 'warrior', 'graze', 'gallop', 'halt', 'arrow'], ['quiver', 'rustle', 'admire']),
    (['brave', 'glance', 'carve', 'pound', 'claw', 'strength'], ['bead', 'moccasin', 'gasp']),
    (['fierce', 'hide', 'mane', 'grip', 'whoop', 'shadow'], ['snarl', 'slit', 'powerful']),
    (['bison', 'herd', 'creep', 'charge', 'stampede', 'moan'], ['alarm', 'dodge', 'shaggy']),
    (['medicine', 'spirit', 'escape', 'disappear', 'ghost', 'scoop'], ['bound', 'lick', 'peaceful']),
    (['sacred', 'pride', 'frighten', 'courage', 'drum', 'ceremony'], ['sternly', 'twilight', 'messenger']),
    (['platform', 'pole', 'stuff', 'belong', 'journey', 'vanish'], ['strap', 'rawhide', 'dawn']),
    (['flood', 'feather', 'porch', 'tilt', 'branch', 'wave'], ['gust', 'relate', 'distance']),
]
