#!/usr/bin/env python3
"""Book 14 (Day of the Dragon King / 龙王焚书之日) titles, scene anchors,
illustration briefs and per-chapter key vocabulary.

Jack & Annie travel to ancient China ~2000 years ago to save an ancient legend
from the Dragon King (the first emperor), who burns every book in the land.
Character design stays consistent with earlier books — Jack: 深色蓬松短发、戴圆
眼镜；Annie: 棕色马尾 — here dressed in ancient Chinese clothes (宽松布衣、草鞋、
圆帽).  Source text has no bilingual word lists, so the standard/extension lists
are curated from the story (grade-5 appropriate, each word verified to occur in
its chapter).
"""

TITLES = [
    'The Bamboo Book', 'The Cowherd', 'The Silk Weaver', 'The Great Wall', 'The Scholar',
    'The Dragon King', 'The Burning of the Books', 'The Tomb', 'The Silk Path', 'The Ancient Legend',
]

# First paragraph of reader page 2 and page 3 — verbatim substrings from the chapter text.
SCENE_ANCHORS = [
    ('Outside, the sun shone brightly.',
     'She held up a long, thin strip of wood.'),
    ('Next to the writing was a picture.',
     'The man tending the cows was shouting and waving.'),
    ('Annie ran to the silk weaver.',
     'He dropped the ball of silk into his sack.'),
    ('Jack and Annie peeked over the bags.',
     'He reached into his sack and pulled out the China book.'),
    ('Annie gasped.',
     'He bowed to show his respect.'),
    ('Then it passed a large market square filled with stalls and shoppers.',
     'He looked over his shoulder at the burial grounds.'),
    ('But she had already snatched up the bundle of bamboo strips and was charging back to them.',
     'They were in a long hall lit with oil lamps.'),
    ('In the flickering lamplight, they wandered down the rows of soldiers.',
     'Jack tried not to panic.'),
    ('They walked and walked and walked down the lamp-lit passage.',
     'They charged across the bridge and kept running up the dirt road, past the farmhouse, and through the field.'),
    ('Jack and Annie gazed up at the bright summer sky.',
     'As they got to the edge of the woods, Annie stopped.'),
]

SCENES = [
    [
        ('出发去中国', '卧室里，棕色马尾的 Annie 探头问深色蓬松短发、戴圆眼镜的 Jack 准备好没；Jack 把薄薄的木质图书卡塞进背包，带上笔记本和铅笔。'),
        ('树屋见摩根', '阳光洒进 Frog Creek 树林，两人爬上绳梯，白发女巫摩根举起一根刻着神秘汉字的细长竹片，说这次要去两千年前的古代中国。'),
        ('竹简与研究书', '树屋里摩根递给 Jack 一本《第一位皇帝的时代》研究书，叮嘱最黑暗时刻唯有古老传说能相救；Jack 推推眼镜许愿，树屋飞速旋转。'),
    ],
    [
        ('变身古装', 'Jack 睁开眼，两人衣服已变成宽松布衣、草鞋和圆帽；窗外阳光下牛群吃草，一个年轻人守望着，远处是一座城墙环绕的城池。'),
        ('龙王画像', '戴圆眼镜的 Jack 翻开中国研究书，指着画中身穿华丽宽袖长袍、戴珠帘高冠的皇帝——被称作“龙王”的第一位皇帝，两人商量去城里皇宫。'),
        ('牛郎的托付', '守牛的英俊年轻人跑来，恳请 Jack 和棕色马尾的 Annie 替他给织女捎话——黄昏田边相见，临别还低声警告：当心龙王。'),
    ],
    [
        ('田间农忙', 'Jack 和 Annie 压低圆帽穿过农庄，牛拉着干草车，农夫锄地、妇人推着满载谷物的独轮车；远处廊下一位年轻女子正在织机前织布。'),
        ('织女赠丝', '棕色马尾的 Annie 跑到织女跟前捎口信，织女含羞而笑，递上一团黄色蚕丝道谢，轻声说蚕丝取自蚕茧，是中国最宝贵的秘密。'),
        ('被人发现', 'Jack 刚把丝线塞进布袋，织女急忙低语“你们被人看见了”；一个男人指着他们大喊，两人撒腿就往外跑。'),
    ],
    [
        ('藏进谷车', '追喊声中，Jack 和 Annie 绕到农舍后，纵身跳进装满谷袋的木牛车，埋进袋子中间；忽然车子猛地一颠，有人赶着车拉走了他们。'),
        ('筑墙的队伍', '两人从谷袋后探头，看见赶车人稳稳驾着牛车驶向城池；车子停下，一长队扛着斧头、铁锹的民夫在卫兵押送下穿过大路。'),
        ('万里长城', '戴圆眼镜的 Jack 翻开纸书，读到龙王驱使百姓修筑长城；赶车人一把抓住他们，却盯着那本纸书惊得张大嘴，缓缓伸手去摸。'),
    ],
    [
        ('他是书生', 'Jack 说这纸书来自他们的国家，赶车人热泪盈眶——他热爱读书，原来他假扮农夫，其实是位学者，在中国世代最受人尊敬。'),
        ('焚书之危', '听说龙王畏惧书本与学问、随时可能下令烧毁所有藏书，Annie 倒吸一口凉气；两人亮出闪光的秘密图书卡，证明身份。'),
        ('结伴前往', '学者躬身行礼，敬佩这么年轻的图书管理大师，答应带他们去皇家藏书楼；一同登上牛车，他听说异国处处有图书馆，感叹如同天堂。'),
    ],
    [
        ('牛车进城', '牛车吱呀驶过护城河上的木桥、穿过巨大城门；街边是茅草顶的泥屋和翘角屋顶的木宅——学者说弯翘的屋檐能挡住只走直线的恶灵。'),
        ('集市与皇陵', '车过热闹集市，鱼、丝绸、玉器琳琅，还有笼中当宠物的蟋蟀；随后到了龙王皇宫，园中隆起座座土丘，是三十万工匠为龙王修的陵墓。'),
        ('宫中起火', 'Jack 回望皇陵，忽见宫廷院落腾起滚滚黑烟——起火了！院里满是士兵与巨大篝火，一位身穿华袍高冠的男子走出殿门，正是龙王。'),
    ],
    [
        ('焚书烈焰', '龙王注视冲天篝火，士兵把一捆捆竹简投入火中，竹片噼啪炸响；Annie 高喊“住手”却淹没在火吼里，学者指着掉落的一捆竹简——正是要找的传说。'),
        ('抢书逃亡', 'Annie 抢起那捆竹简冲回来塞进布袋；龙王怒吼“抓住他们”，学者叫他们逃进皇陵——士兵怕祖先亡灵不敢追；箭矢呼啸，两人翻墙钻进土丘门洞。'),
        ('陵中长廊', '土丘里是一条油灯照亮的长廊，尽头是陡峭石阶；Jack 和 Annie 屏息一级级走下，到了底部，眼前竟是挤满成千上万士兵的大厅。'),
    ],
    [
        ('陶土大军', '满屋士兵竟是泥塑陶俑！Annie 捏了捏陶俑的鼻子，Jack 摸到坚硬彩绘的脸；研究书说龙王烧制七千尊真人大小陶俑，好在死后护卫自己。'),
        ('迷失俑阵', '摇曳灯影中，两人穿行俑阵，张张面孔各不相同，还有跪射弓手、青铜兵器和木战车骏马；Jack 忙着记笔记，却发现分不清来路，一望无尽。'),
        ('丝线指路', 'Jack 强忍慌乱，空气越来越闷、灯光越来越暗；他举起竹简书求救却毫无动静，忽然那团黄色蚕丝从布袋滚出，一路留下丝线自己滚动起来。'),
    ],
    [
        ('追随丝线', 'Jack 和 Annie 跟着自动滚动的黄色丝线在俑阵间穿行，直呼“这不科学”；丝线到头散尽，两人喘口气，正好看见前方一道向上的石阶。'),
        ('抢在闭城前', '沿着油灯长廊走到一扇门，推开竟是夕阳下的皇宫外；铜锣一响城门将闭，两人赤脚狂奔，穿过大街小巷，赶在巨大城门合拢前冲了出去。'),
        ('奔回树屋', '两人冲过木桥、沿土路穿过田野奔回大树爬进树屋；回望田边，织女与牛郎终于团聚相拥；Jack 许愿回家，树屋飞快旋转，一切归于寂静。'),
    ],
    [
        ('传说揭晓', '换回原衣的两人把中国研究书和竹简书交给摩根；摩根说这传说叫《织女与牛郎》，讲两位天界神仙下凡相爱，正是他们帮过的那对恋人。'),
        ('银河相隔', '摩根说天帝天后后来用银河把二人分开，每年只能在喜鹊搭成的桥上相会一次；Jack 和 Annie 仰望明亮的夏夜星空，随后爬下绳梯告别。'),
        ('蟋蟀讲古', '走到林边，Annie 停下听蟋蟀鸣叫，说它们的祖先活在龙王时代，正把传说讲给小蟋蟀听；Jack 微笑着，妈妈的呼唤传来，两人跑回了家。'),
    ],
]

# Curated key vocabulary: (standard, extension) per chapter — each occurs in text.
VOCABULARY = [
    (['library', 'notebook', 'whisper', 'wonder', 'adventure', 'ladder'], ['ancient', 'legend']),
    (['pocket', 'field', 'peaceful', 'message', 'handsome', 'shoulder'], ['twilight', 'grateful']),
    (['silk', 'thread', 'secret', 'smooth', 'hurry'], ['loom', 'cocoon']),
    (['grain', 'breath', 'driver', 'guard', 'wall', 'protect'], ['lurch', 'invader']),
    (['country', 'learn', 'danger', 'honor', 'power', 'respect'], ['scholar', 'paradise']),
    (['bridge', 'market', 'palace', 'spirit', 'soldier', 'tomb'], ['moat', 'ancestor']),
    (['bonfire', 'soldier', 'crowd', 'burial', 'arrow', 'duck'], ['blaze', 'snatch']),
    (['soldier', 'real', 'army', 'clay', 'tomb', 'lost'], ['armor', 'panic']),
    (['thread', 'stairs', 'passage', 'gate', 'bridge'], ['relief', 'barefoot', 'embrace']),
    (['legend', 'famous', 'together', 'tale', 'summer', 'ancestor'], ['heavenly', 'separate']),
]
