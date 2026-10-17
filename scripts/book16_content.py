#!/usr/bin/env python3
"""Book 16 (Hour of the Olympics / 古奥林匹克竞技会) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text has no bilingual word lists, so the standard/extension lists are
curated from the story (grade-5 appropriate, each word verified to occur in its
chapter).  Character design stays consistent with earlier books — Jack: 深色蓬松
短发、戴圆眼镜；Annie: 棕色马尾 — here both wear ancient Greek tunics (chiton);
in this book Annie disguises herself as a boy, tucking her braids under a
soldier's helmet so she can sneak into the men-only Olympic games.
"""

TITLES = [
    'Just One More', 'Any Girls Here?', 'The Secret Poet', 'Not Fair!', 'Hi, Zeus',
    'Mystery Man', 'Go! Go! Go!', 'Save Annie!', 'Fly Away Home', "They're All Here",
]

# First paragraph of reader page 2 and page 3 — verbatim substrings, quotes ignored.
SCENE_ANCHORS = [
    ('They followed the beam of light across their yard and up the street.',
     'Jack heard a rustling sound.'),
    ('She started down the rope ladder.',
     'The woman and the soldier were waving their arms and talking loudly to each other.'),
    ('He reached into his bag and took out the secret library cards.',
     'Plato stopped at the door of a sand-colored house with a brick roof.'),
    ('Annie looked back at the woman.',
     'Plato shook his head.'),
    ('As they moved along, Plato pointed to a beautiful tree nearby.',
     'In front of them loomed the biggest statue he had ever seen.'),
    ('Musicians playing pipes were at the front.',
     'The soldier was dressed like the actor from the outdoor theater.'),
    ('Jack saw the dozens of chariots lined up on the race track.',
     'He shoved his notebook into his pack.'),
    ('Finally, Jack reached Annie and the guards.',
     'He held the story up to the sky.'),
    ('The white horse had grown giant feathery wings and was pulling their chariot into the sky.',
     'Annie sniffled but started walking.'),
    ('Annie turned on the flashlight and used it to find her way down the rope ladder.',
     'Jack thought he saw the stars move as if Pegasus was rearing back in the sky.'),
]

SCENES = [
    [
        ('摸黑出发', '天没亮的卧室里，深色蓬松短发、戴圆眼镜的 Jack 一骨碌爬起，棕色马尾的 Annie 打开手电，两人踮脚溜出家门，沿着光束奔向 Frog Creek 树林。'),
        ('树屋见摩根', '漆黑树屋里，白发女巫摩根坐在窗边，请 Annie 关掉刺眼的手电，递上写着希腊文的纸条和研究书《古希腊的一天》，郑重交代最后一个任务。'),
        ('许愿去希腊', 'Jack 激动地指着书封，许愿去古希腊，Annie 也盼着以后更多冒险；风声骤起，树屋越转越快，最后一切归于绝对的寂静。'),
    ],
    [
        ('落在橄榄树上', '暖阳洒进树屋，Jack 和 Annie 换上古希腊短袍与凉鞋，探出窗口望见橄榄树林外白色帐篷连片、红砖石柱与如潮人群——他们来到了古代奥运会。'),
        ('集市不见女孩', '穿过橄榄林走进帐篷集市，笛声悠扬、烤肉飘香，戴圆眼镜的 Jack 和 Annie 却发现四周全是男人和男孩，一个女孩也看不见。'),
        ('露天剧场的戏', '露天剧场舞台上，一位“黄发紫袍女子”正和披红缨头盔的士兵挥臂对白；那女子摘下假发竟是个男孩，一位白胡子老者朝 Annie 走来。'),
    ],
    [
        ('哲学家柏拉图', '白胡子老者柏拉图微笑自称“智慧的爱好者”，惊讶地打量勇敢穿行奥林匹亚的 Annie；棕色马尾的她大方回问，戴圆眼镜的 Jack 在一旁点头。'),
        ('亮出图书卡', 'Jack 从皮袋里掏出两张秘密图书卡，卡上代表“图书管理大师”的 M、L 闪着微光；柏拉图惊叹不已，答应带他们去见写下故事的诗人朋友。'),
        ('庭院见诗人', '柏拉图领两人走进一座沙色砖顶房子的空庭院，Jack 翻书才知希腊女孩不能上学；片刻后柏拉图带回一位手持卷轴、长袍镶边的年轻女子——秘密诗人。'),
    ],
    [
        ('无名的诗人', '年轻女诗人把自学写成的卷轴交到 Jack 手中，却不肯留名，只说署名“无名氏”；棕色马尾的 Annie 皱起眉头，觉得这实在太不公平。'),
        ('女孩的心愿', '女诗人盼着有朝一日女子也能像男子一样写书，Jack 郑重承诺“一定会的”；她躬身道谢匆匆离去，Annie 抱怨女孩连戏都不许演。'),
        ('分头行动', '柏拉图摇头说女孩不许进赛场，希腊的自由眼下只属于男人；Annie 叹气决定回剧场，让戴圆眼镜的 Jack 独自去看奥运会、替她记笔记。'),
    ],
    [
        ('战车赛之日', '柏拉图带 Jack 走向赛道，说今天是奥运会头一天——战车赛日；路过高大的体育馆，运动员正在里面练习跑步、掷标枪和铁饼。'),
        ('圣树与胜利女神', '柏拉图指着一棵神圣的橄榄树，说冠军将戴上它枝叶编成的桂冠；不远处立着一尊生着双翼的胜利女神 Nike 雕像，Jack 忙掏出笔记本记下。'),
        ('宙斯神庙巨像', '走进巨柱神庙，Jack 倒吸一口气——两层楼高的宙斯坐在宝座上俯视众人；他觉得自己好渺小，怯生生说了句“你好，宙斯”，庙外号角骤响。'),
    ],
    [
        ('观礼台看游行', '柏拉图把 Jack 领到裁判席旁的看台，视野极佳；奥运游行已经开始，吹排笛的乐师走在最前，身后是全希腊最出色的运动员绕场行进。'),
        ('拳手与摔跤手', '队伍里跑者之后是戴青铜头盔、缠着特制护套的拳手，再后面是摔跤手；戴圆眼镜的 Jack 一条条记进笔记本，想着 Annie 一定会喜欢。'),
        ('矮个神秘士兵', '看台下一个披斗篷、戴红缨头盔的士兵格外矮小，直盯着 Jack；忽然斗篷里伸出一只小手轻轻一挥——那竟是把辫子藏进头盔、女扮男装的 Annie！'),
    ],
    [
        ('急得直摇头', '认出女扮男装的 Annie，戴圆眼镜的 Jack 在看台上又摇头又挥拳，示意她快走；Annie 却只顾冲他挥手，随后扭头继续看比赛。'),
        ('战车飞驰', '号角一响，几十辆四马战车在赛道上疾冲，尘土滚滚，人群疯狂呐喊跺脚；假扮士兵的 Annie 蹦跳着尖声高喊“加油！加油！”，引来旁人侧目。'),
        ('头盔掉了', 'Jack 再也坐不住，飞奔下台阶；只见 Annie 扯掉头盔，棕色辫子甩了出来，斗篷滑落，人群纷纷高喊叫卫兵——两名大个卫兵抢先一步抓住了她。'),
    ],
    [
        ('卫兵拖走她', '两名卫兵拽着挣扎的 Annie 往外拖，她又惊又怒大喊“放开我”；Jack 冲下看台，拼命挤过人群，一遍遍高喊“别碰她”。'),
        ('最黑暗时刻', 'Jack 好不容易挤到近前却被卫兵拦住，越来越多卫兵围上来，人群齐声喊“抓住她”；Annie 急喊“故事！”——Jack 猛然想起诗人的卷轴。'),
        ('白马破尘而出', 'Jack 把卷轴高高举向天空大喊“救救 Annie”；喊声淹没在赛马轰鸣里，人群却忽然静了——一匹雪白骏马拉着空战车破尘而出，径直朝 Jack 奔来。'),
    ],
    [
        ('跳上战车逃走', '雪白骏马在矮墙边停下，Annie 挣脱卫兵奔向 Jack，两人翻墙跳进空战车；骏马腾空前蹄，柏拉图含笑挥手，白马拉着战车与奥运赛马并肩飞奔。'),
        ('飞马腾空', '忽然雪白骏马长出巨大的羽翼，拉着战车升上蓝天；Jack 死死抓住栏杆，只见飞马掠过宙斯神庙、胜利女神像、圣橄榄树与体育馆，飞越整座奥林匹亚。'),
        ('告别飞马', '飞马滑落橄榄林边，Annie 泪汪汪抚着它的脖子道谢；白马用鼻子轻触她额头、推她走向树屋，随后展翅飞入奥林匹斯蓝天，消失在云后。'),
    ],
    [
        ('回到树屋', '树屋重归黑暗，Jack 换回 T 恤牛仔裤；白发摩根问起旅程，Annie 说自己坐过飞马拉的战车；Jack 把卷轴交给摩根——那正是飞马 Pegasus 的故事。'),
        ('它们都在这儿', 'Annie 打着手电爬下绳梯四处找 Pegasus，摩根却让她关灯抬头：救过他们的英雄——Hercules、织女、巨蛇 Sarph 和飞马——今夜全都在这里。'),
        ('星空里的伙伴', '摩根挥手，夜空中一颗颗星连成 Hercules、织女、巨蛇与展翅的飞马星座；Annie 轻声说“我爱你，Pegasus”；老故事永远伴随他们，众人道别摸黑回家。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['flashlight', 'ancient', 'mission', 'brave', 'research', 'journey'], ['shiver', 'rustle']),
    (['tunic', 'olive', 'theater', 'stage', 'helmet', 'crowd'], ['cape', 'wig']),
    (['poet', 'scroll', 'courtyard', 'puzzled', 'secret', 'wisdom'], ['philosopher', 'brilliant']),
    (['trouble', 'promise', 'freedom', 'sigh', 'bow'], ['democracy', 'citizen', 'grumble']),
    (['chariot', 'athlete', 'statue', 'temple', 'sacred', 'victory'], ['gymnasium', 'throne']),
    (['parade', 'cheer', 'boxer', 'wrestler', 'armor', 'soldier'], ['bronze', 'judge']),
    (['trumpet', 'chariot', 'horror', 'dust', 'guard', 'costume'], ['glare', 'pigtail']),
    (['scroll', 'gallop', 'silent', 'wonder', 'angry', 'murmur'], ['arrest', 'roar']),
    (['chariot', 'wing', 'wobbly', 'stroke', 'disappear', 'tear'], ['feathery', 'rear']),
    (['serpent', 'shimmer', 'relief', 'trust', 'glow', 'vanish'], ['mythology', 'constellation']),
]
