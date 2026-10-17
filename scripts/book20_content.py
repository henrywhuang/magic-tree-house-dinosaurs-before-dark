#!/usr/bin/env python3
"""Book 20 (Dingoes at Dinnertime / 澳洲大火) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text is proofread from the audiobook transcript (book20_source.txt) and
has no bilingual word lists, so the standard/extension lists are curated from
the story (grade-5 appropriate, each word verified to occur in its chapter).
Character design stays consistent with earlier books — Jack: 深色蓬松短发、戴圆
眼镜；Annie: 棕色马尾；Teddy: 棕黄色小狗 — here in modern clothes and sun hats
in the dry Australian bush (eucalyptus/gum-tree forest), through a wildfire and
the rainstorm that puts it out.
"""

TITLES = [
    'The Last Gift', 'Sleepyhead', 'Big Foot', 'Joey', 'Wildfire',
    'Hand to Hand', 'Rain, Rain, Rain', 'The Rainbow Serpent', 'What Boy?', 'Dreamtime',
]

# Verbatim narrative substrings at roughly 1/3 and 2/3 of each chapter — quotes ignored.
SCENE_ANCHORS = [
    ('Annie grabbed the rope ladder and started climbing.',
     'Beside the note were the gifts from their first three trips:'),
    ('They started walking across a sun-baked clearing.',
     'Annie ran to a tree at the edge of the clearing.'),
    ('The lump was an animal lying on its back.',
     'Jack couldn’t believe how graceful the kangaroo was.'),
    ('Jack opened the Australia book and found a picture of a baby kangaroo.',
     'Jack put his Australia book on the ground.'),
    ('Jack and Teddy turned to go.',
     'Suddenly Jack heard Annie calling him.'),
    ('Suddenly Jack felt something thump against his leg.',
     'She let go of Jack and put her hand inside one of the painted handprints.'),
    ('Joey stirred in his pack.',
     'He picked up the Australia book.'),
    ('The rain stopped as Jack studied the piece of bark.',
     'The rain clouds were gone.'),
    ('She picked up their first gift.',
     'Morgan picked up the piece of bark with the painting of the Rainbow Serpent.'),
    ('Jack just nodded.',
     'When they got to the ground, they looked up.'),
]

SCENES = [
    [
        ('门廊听见狗叫', '午后，棕色马尾的 Annie 坐在家门前的台阶上望向青蛙溪树林，深色蓬松短发、戴圆眼镜的 Jack 在她身旁看书，远处隐约传来小狗“汪汪”的叫声，两人相视一笑。'),
        ('树屋里的小狗', '两人跑进树林，最高的橡树上，一只黑鼻子从树屋窗口探出来；爬进树屋，棕黄色小狗 Teddy 正坐在一圈午后阳光里摇着尾巴，地板上还留着摩根的字条。'),
        ('许愿去澳洲', '字条旁摆着怀表、鹰羽和莲花三件礼物，Teddy 用爪子扒出角落里的《澳洲探险》，Jack 指着书中一大片森林的图画许愿，风起了，树屋越转越快。'),
    ],
    [
        ('干旱的灌木林', '炽热的阳光照进树屋，Jack 和 Annie 头上多了遮阳帽；窗外是植物低垂、树木枯黄的澳洲灌木林，远处树梢上飘起一缕轻烟，空气里有股野餐烧烤般的味道。'),
        ('高傲的鸸鹋', '烈日下龟裂的空地上蜥蜴乱窜，两只比 Jack 还高、身子圆胖、腿和脖子都又细又长的鸸鹋从灌木后走出，冲着汪汪叫的小狗 Teddy 傲慢地瞥了一眼，昂首走开。'),
        ('树杈上的考拉', '空地边的桉树杈上，一只圆耳朵、黑鼻子、毛茸茸的考拉正在酣睡，棕色马尾的 Annie 轻抚它的软毛叫它“小瞌睡虫”，戴圆眼镜的 Jack 捧着书念起考拉的知识。'),
    ],
    [
        ('怪笑的翠鸟', '干燥的桉树上，一只棕色羽毛、大脑袋、长嘴巴的笑翠鸟俯视着 Jack 和 Annie，发出驴叫般的怪笑；Annie 笑着唱起歌来，Jack 在笔记本上记下它的名字。'),
        ('袋鼠妈妈醒来', '浅浅的尘土坑里，一只蓝褐色的大袋鼠仰面躺着，育儿袋里探出一个小脑袋；被说话声吵醒后，它一跃而起，瞪着戴遮阳帽的 Jack 和 Annie，不满地跺了跺脚。'),
        ('野狗追袋鼠', 'Annie 学着袋鼠在空地上蹦跳，像在共舞；忽然三只沙黄色、凶相毕露的野狗从灌木中悄悄钻出，袋鼠妈妈腾空而起，左躲右闪地逃开，野狗嚎叫着紧追不舍。'),
    ],
    [
        ('草丛里的小袋鼠', '棕色马尾的 Annie 追到草丛边跪下，一只瑟瑟发抖的小袋鼠缩在草里；戴圆眼镜的 Jack 赶到，翻开《澳洲探险》读到野狗是袋鼠的天敌，小狗 Teddy 乖乖坐在一旁。'),
        ('钻进背包里', '柔软的棕色小袋鼠 Joey 一个大跳，头朝下钻进 Jack 的背包，只露出一双大脚，随后翻过身探出脑袋；Annie 帮 Jack 把背包反背在胸前，活像一位袋鼠妈妈。'),
        ('远处燃起大火', 'Annie 抓了一把青草喂 Joey，Joey 一边嚼一边睁大眼睛望着她；远方那缕轻烟已变成滚滚黑云，焦糊味越来越浓，一棵树突然燃起熊熊火焰，Jack 心头一紧。'),
    ],
    [
        ('动物四散奔逃', '林火蔓延，浓烟越来越重，笑翠鸟怪叫着飞过天空，鸸鹋全速狂奔而过；戴圆眼镜的 Jack 胸前背着小袋鼠 Joey，焦急地辨认树屋的方向，眼睛被烟熏得刺痛。'),
        ('烟火中奔跑', '枝干噼啪断裂坠落，浓烟翻滚，Annie 冲往另一个方向不见了；戴遮阳帽的 Jack 一边咳嗽一边揉眼，托着沉甸甸的背包，循着 Teddy 的叫声在灌木丛中跌跌撞撞地奔跑。'),
        ('抱着考拉归来', '炽热的烟雾中，棕色马尾的 Annie 抱着那只考拉现身，泪流满面；两人跟着 Teddy 的叫声来到一块巨石前，棕黄色的 Teddy 站在岩架上，身后是黑黝黝的洞口。'),
    ],
    [
        ('手牵手进山洞', '凉爽漆黑的山洞里，Jack 和 Annie 手牵着手，Jack 另一只手摸着岩壁慢慢前行，胸前背包里的小袋鼠动了动，前方黑暗中传来 Teddy 一声声引路的叫声。'),
        ('发光的巨蛇', 'Teddy 一声长嚎，黑暗中一道白线亮了起来，渐渐变成一条发光的巨蛇，蛇身下方浮现出一排发光的手印；戴圆眼镜的 Jack 和棕色马尾的 Annie 惊讶地紧握彼此的手。'),
        ('手印与雷声', '两人把手按进岩壁上发光的手印里，石壁光滑清凉，仿佛在呼吸；随即一阵幽灵般的呼啸和隆隆雷声传来，他们跟着 Teddy 冲出洞口，闪电划破天空，大雨倾盆。'),
    ],
    [
        ('雨中送考拉', '倾盆大雨浇灭了林火，焦黑的土地上升起白茫茫的水汽；棕色马尾的 Annie 把考拉放回一棵没被烧着的桉树枝杈间，轻声让它接着睡，考拉仿佛冲他们微微一笑。'),
        ('泥地里找书', '小狗 Teddy 一声不吭地在湿漉漉的泥地上领路，胸前背着 Joey 的 Jack 和 Annie 紧随其后，终于找到那本淋湿却没烧坏的《澳洲探险》——正是发现 Joey 的地方。'),
        ('细雨中等待', '大雨转成细雨，又变成零星小雨，Jack、Annie、Teddy 和 Joey 站在灰蒙蒙的林中苦苦等待，Jack 越来越难过；忽然远处传来啪嗒啪嗒、大脚踩过泥水的声音。'),
    ],
    [
        ('母子重逢', '袋鼠妈妈从林中跃出，小袋鼠 Joey 跳出 Jack 的背包，一头扎进妈妈的育儿袋，又翻身探出脑袋；Jack 和 Annie 欢笑鼓掌，袋鼠妈妈温柔地递来一小块树皮。'),
        ('树皮上的彩虹蛇', '雨停了，戴圆眼镜的 Jack 端详树皮上那幅小小的蛇形图画，和山洞壁画一模一样；他翻开湿漉漉的书，读到澳洲原住民关于“梦幻时光”和降下生命之雨的彩虹蛇的传说。'),
        ('彩虹横跨天空', '雨云散去，一道彩虹横跨澳洲湛蓝的天空；他们穿过湿润、冒着热气的森林，回到安然无恙的树屋，Teddy 用爪子拍着家乡的书，棕色马尾的 Annie 喊着“飞越彩虹”。'),
    ],
    [
        ('重见摩根', '树屋回到青蛙溪树林，温柔美丽的摩根·勒菲在屋里等着他们；棕色马尾的 Annie 扑上前抱住这位女魔法师，Jack 也跳起来拥抱她，小狗 Teddy 在一旁开心地汪汪叫。'),
        ('四件礼物的意义', '摩根依次拿起泰坦尼克号的怀表、拉科塔人的鹰羽和印度森林的莲花，讲述一个男孩从中学到的道理：时间宝贵、弱小者也能勇敢、大自然充满奇迹，Jack 和 Annie 听得入神。'),
        ('小狗变成男孩', '摩根拿起彩虹蛇树皮画，感谢他们帮那个男孩解除魔咒；Teddy 汪汪叫了三声，转眼间，在时光的颤动与旋风的飞旋中，棕黄色小狗不见了，地上出现了一个男孩。'),
    ],
    [
        ('卡米洛少年','树屋里，一个男孩趴跪在地上抬起头：他长着友善的雀斑脸和闪亮的深色眼睛，头发和 Teddy 的毛色一模一样，看上去比 Jack 大一点；他开心地跳起来拥抱摩根。'),
        ('带回新故事', '男孩 Ted 不好意思地笑着，原来他误用魔法书把自己变成了小狗；他说要把泰坦尼克号、白水牛女、受伤老虎和彩虹蛇的故事写进卡米洛图书馆，Jack 仍惊得说不出话。'),
        ('暮色中回家', '摩根和 Ted 站在树屋窗口，沐浴着傍晚的光芒挥手告别，树屋随旋风消失；Jack 和 Annie 默默穿过青蛙溪树林回家，一群黑鸟飞过银粉色的晚霞天空。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['faint', 'grab', 'scratch', 'special', 'spin', 'absolutely'], ['kangaroo', 'eagle', 'oak']),
    (['drought', 'sniff', 'threat', 'moisture', 'thirsty', 'harsh'], ['koala', 'emu', 'marsupial']),
    (['terrible', 'beak', 'stomach', 'stamp', 'copy', 'contest'], ['kookaburra', 'pouch', 'zigzag']),
    (['enemy', 'chase', 'weight', 'shy', 'backward', 'burst'], ['dingo', 'joey', 'wildfire']),
    (['choice', 'spread', 'dash', 'choke', 'cough', 'stumble'], ['haze', 'smoky', 'sting']),
    (['thump', 'howl', 'amazing', 'despite', 'breathe', 'pour'], ['handprint', 'boom', 'whistle']),
    (['steam', 'pretend', 'disturb', 'stir', 'lucky', 'slap'], ['charred', 'drizzle', 'sprinkle']),
    (['nod', 'study', 'explain', 'wiggle', 'artist', 'frown'], ['myth', 'ceremony', 'steamy']),
    (['lovely', 'waste', 'precious', 'mystery', 'tradition', 'lesson'], ['whirlwind', 'flutter', 'wisely']),
    (['helper', 'rare', 'shock', 'exciting', 'search', 'exactly'], ['sheepishly', 'flock', 'silvery']),
]
