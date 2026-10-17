#!/usr/bin/env python3
"""Book 17 (Tonight on the Titanic / 泰坦尼克号上的一夜) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Source text (docx) has no bilingual word lists, so the standard/extension lists
are curated from the story (grade-5 appropriate, each word verified to occur in
its chapter).  Character design stays consistent with earlier books — Jack: 深色
蓬松短发、戴圆眼镜；Annie: 棕色马尾 — but from chapter 2 on the tree house's magic
dresses them in 1912 clothes (Jack: 呢子大衣、及膝短裤；Annie: 水手裙、羊毛斗篷)
over their pajamas and rain ponchos.
"""

TITLES = [
    'A New Mission', 'The Unsinkable Ship', 'SOS', 'Put on Your Life Belts!',
    'William and Lucy', 'Women and Children First', 'The Gift', 'Every Man for Himself',
    'Time Stops', 'A Touch of Magic',
]

# First paragraph of reader page 2 and page 3 — verbatim substrings, quotes ignored.
SCENE_ANCHORS = [
    ('Wind blew through the trees, shaking water to the ground.',
     'Jack’s gaze fell on a piece of paper lying on the floor.'),
    ('Then Jack looked straight ahead and saw a box high in the air, near the front of the ship.',
     'The scraping sound stopped. The ship slid past the iceberg until they lost sight of it.'),
    ('The little dog scampered after them.',
     'The captain stepped out onto the deck.'),
    ('Men and women stumbled out of their rooms.',
     'At the bottom of the stairs, they rounded a corner, and they both gasped.'),
    ('Lucy looked confused.',
     'Annie slipped the little dog into the leather knapsack on Jack’s back.'),
    ('The men smiled at her again.',
     'On the top deck, the Titanic was as bright as a Christmas tree.'),
    ('He gently pushed Lucy and William forward.',
     'Jack and Annie watched as a big man picked Lucy up and swung her into the little boat.'),
    ('They ran up the slanting deck.',
     'Suddenly, the front of the ship dipped down into the sea.'),
    ('There was more frantic barking.',
     'The back of the Titanic was rising out of the ocean.'),
    ('The watch had stopped. The hands were at 2:20.',
     'She started down the rope ladder. Jack looked around the tree house one last time.'),
]

SCENES = [
    [
        ('雨夜的召唤', '暴雨敲打窗玻璃的深夜，棕色马尾的 Annie 披着雨披、举着手电站在门口，叫醒戴圆眼镜的 Jack，说雨声在喊“快来”，树屋有大事要发生。'),
        ('树屋里的小狗', '手电光扫过漆黑的树屋，深色蓬松短发的 Jack 和 Annie 惊讶地发现墙角蜷着一只毛色浅棕、脏兮兮的小狗，他们叫它 Teddy，小狗怯生生地摇着尾巴。'),
        ('摩根的四件礼物', 'Jack 捡起地上摩根留下的字条：要解开小狗身上的魔咒，必须集齐四件礼物，第一件来自沉入大海的船。Teddy 用鼻子拱开一本《不沉之船》。'),
    ],
    [
        ('换上旧时装', '寒风里 Jack 低头发现自己换上了呢子大衣和及膝短裤，Annie 也穿上水手裙和羊毛斗篷，树屋正落在巨轮两根冒着黑烟的大烟囱之间。'),
        ('不沉的巨轮', '戴圆眼镜的 Jack 借着手电翻开书，念到 1912 年 4 月 14 日深夜，这艘四个街区长、载着两千多名乘客的英国邮轮正驶向纽约，人人都说它永不沉没。'),
        ('冰山就在前方', '瞭望台传来“前方有冰山”的喊声，Jack 和 Annie 扑到窗边，只见一座黑黢黢的巨大冰山逼近，船身擦过冰山发出刺耳的摩擦声。'),
    ],
    [
        ('泰坦尼克号', '船舷救生圈上“R.M.S. TITANIC”的黑字让 Jack 脸色发白，他轻声告诉棕色马尾的 Annie：这就是撞上冰山沉没的泰坦尼克号，可他们改变不了历史。'),
        ('无线电求救', '圆窗里，戴耳机的报务员敲击着电键，白胡子船长下令向附近所有船只发出国际求救信号 SOS，Jack 和 Annie 屏息偷看。'),
        ('救生艇不够', 'Jack 就着手电念书：船上只有二十艘救生艇，还不够坐一半的人。他和 Annie 盯着船体地图，决定沿大楼梯下到三等舱，去帮人找到救生艇。'),
    ],
    [
        ('华丽大楼梯', '深色蓬松短发的 Jack 和 Annie 推门来到空荡荡的大楼梯口，深色亮木的台阶、头顶发光的大穹顶，楼梯顶端的华丽挂钟指着十二点二十分。'),
        ('穿上救生衣', '白制服船员挨个敲门大喊“快穿好救生衣上甲板”，穿着绸缎睡袍和天鹅绒长袍的绅士淑女睡眼惺忪地走出房间，却没人当回事。'),
        ('倾斜的走廊', 'Jack 抱起 Teddy，和 Annie 冲下更低的楼梯，拐角处地板明显向下倾斜，走廊尽头海水已在晃荡——小狗突然朝一扇紧闭的舱门狂吠。'),
    ],
    [
        ('门后的小男孩', '狂吠声中舱门打开，一个穿睡袍、红头发带雀斑的四岁小男孩 William 探出头，一眼看见 Teddy 就笑着扑上去搂住小狗的脖子。'),
        ('姐姐露西', '穿白色长睡裙的姐姐 Lucy 走出来，同样红发雀斑、又高又瘦。Annie 急忙告诉她泰坦尼克号撞了冰山正在下沉，要带他们去救生艇。'),
        ('把小狗装进背包', 'Annie 把 Teddy 塞进 Jack 的皮背包，只露出前爪和脑袋。就在这时冰冷的海水漫过 Jack 的鞋面，绿色海水正顺着走廊涌来，Annie 大喊“快跑”。'),
    ],
    [
        ('海水追上楼梯', '一行人沿楼梯往上逃，戴圆眼镜的 Jack 回头，看见冰冷海水正一级一级爬上台阶，Teddy 发出一声惊叫，Annie 催促大家快跑。'),
        ('执迷的牌手', '烟雾缭绕的房间里四个男人还在打牌，Annie 大喊“快上救生艇”，他们却笑着说船就算沉也得一整夜，有的是时间，让她别担心。'),
        ('甲板像圣诞树', '顶层甲板灯火通明亮如圣诞树，乐队奏着欢快的曲子，一枚火箭嘶地窜上夜空炸成彩色光球，William 冻得发抖却拍手笑喊“放烟花啦”。'),
    ],
    [
        ('不敢上救生艇', '救生艇在船舷缆索上摇晃，下方海水漆黑。Lucy 直摇头说宁可留在明亮的大船上，Jack 和 Annie 恳求她为了弟弟一定要勇敢。'),
        ('把姐弟送上艇', '船员喊“妇女儿童先上”，Jack 轻轻把 Lucy 和 William 推向前。大个子男人一把抱起 Lucy 荡进小艇，又把 William 放进她怀里。'),
        ('银表的礼物', 'Lucy 从口袋掏出父亲的银怀表挂到 Annie 脖子上，说姐弟俩今晚全靠他们。表针指着一点五十分——离沉船只剩三十分钟了。'),
    ],
    [
        ('拉安妮回大船', '救生艇正往下放，一位裹着皮草的贵妇扑到栏杆边求救。小艇被重新吊回，Jack 一把抓住 Annie 的手，把她从下沉的大船边拉了回来。'),
        ('目送姐弟远去', 'Jack 和 Annie 趴在倾斜的栏杆上，望着 Lucy 和 William 的小艇缓缓降到漆黑海面，漂进茫茫夜色，Annie 挥手喊“谢谢你们的礼物”。'),
        ('各自逃命', '船头猛地扎进海里，桌椅顺着甲板滑下，船长大喊“现在各自逃命”。Jack 和 Annie 躲开滑动的家具，奋力冲向通往大烟囱的楼梯。'),
    ],
    [
        ('树屋不见了', '爬到大烟囱旁，Jack 和 Annie 却发现魔法树屋不见了。泰坦尼克号船头越沉越深，两人死死抓住栏杆，海水轰鸣着漫过下层甲板。'),
        ('小狗的呼唤', '一片漆黑中传来 Teddy 拼命的吠叫，Annie 循声摸下陡斜的甲板，戴圆眼镜的 Jack 吓得直喊，生怕她掉进冰冷的大海里。'),
        ('找到侧翻的树屋', '船灯全灭，Jack 滑倒撞上烟囱，借着微光看见侧翻卡在栏杆间的树屋。他爬过去，Annie 一把将他拉进树屋，Teddy 舔他的脸。'),
    ],
    [
        ('回到树屋', '一切归于寂静，Jack 睁眼发现自己又穿回睡衣雨披躺在树屋地板上。想起沉入冰海的泰坦尼克号，深色蓬松短发的他和 Annie 都红了眼眶。'),
        ('停摆的怀表', 'Annie 打开手电照向脖子上的银怀表，表针停在两点二十分——正是巨轮沉没的时刻。她把怀表放到摩根字条上：第一件来自沉船的礼物到手了。'),
        ('道别泰坦尼克', '小狗 Teddy 又神秘消失，Jack 和 Annie 爬下绳梯回到星空下的家。Jack 轻声说：时间为泰坦尼克停住，但书和记忆让它永远活着。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['flashlight', 'poncho', 'shiver', 'whisper', 'spell', 'mission'], ['terrier', 'scruffy', 'gaze']),
    (['overcoat', 'voyage', 'passenger', 'iceberg', 'smokestack', 'unsinkable'], ['cloak', 'glitter', 'jolt']),
    (['engine', 'captain', 'uniform', 'distress', 'signal', 'operator'], ['gush', 'scamper', 'shrug']),
    (['stairway', 'elegant', 'velvet', 'stateroom', 'hallway', 'slant'], ['glossy', 'robe', 'cheerful']),
    (['freckle', 'emergency', 'nightgown', 'confuse', 'knapsack', 'freeze'], ['nightshirt', 'sleepily', 'kiss']),
    (['staircase', 'rescue', 'soothing', 'crowd', 'rocket', 'firework'], ['yelp', 'streak', 'lively']),
    (['lifeboat', 'cable', 'uniformed', 'straighten', 'silver', 'danger'], ['brightly', 'toss', 'jerk']),
    (['railing', 'peer', 'glassy', 'panic', 'crew', 'tilt'], ['hymn', 'dodge', 'crawl']),
    (['roar', 'imagine', 'furniture', 'frantic', 'steep', 'smokestack'], ['corridor', 'crash', 'barely']),
    (['cheek', 'furry', 'stroke', 'silent', 'myth', 'memory'], ['whine', 'shudder', 'cozy']),
]
