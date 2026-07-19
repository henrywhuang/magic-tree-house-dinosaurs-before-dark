#!/usr/bin/env python3
"""Shared Book 6 metadata, vocabulary, plot scenes and art descriptions."""

TITLES = [
    "Where's Peanut?", 'Big Bugs', 'Yikes!', 'Millions of Them!',
    'Pretty Fish', 'Monkey Trouble', 'Freeze!', 'Vampire Bats?',
    'The Thing', 'Halfway There',
]

# Each pair starts scene 2 and scene 3. Boundaries follow story beats rather than
# equal word counts so each illustration explains one coherent event.
SCENE_ANCHORS = [
    ('Squeak!', '"We have to find three more things'),
    ('"I don\'t get it,"', '"Okay, then, let\'s go,"'),
    ('“Wait!” Jack grabbed', '“We have to use the ladder,”'),
    ('Annie stopped. "Wait—what\'s that?"', '“Run to the tree house!”'),
    ('"Jack, look at those pretty fish', '“Well...” Jack looked'),
    ('“Uh-oh,” said Annie.', 'Screeching split the air again.'),
    ('Soon he found the monkey.', 'GRRR!'),
    ('“But what about our mission?”', 'Suddenly Jack stopped.'),
    ('Something came flying through', 'Before Annie could answer'),
    ('Squeak. Peanut was looking', 'Jack put the rain forest book'),
]

# Proofread against the supplied OCR vocabulary panels, then filtered for useful
# Grade 5 reading words. Chapter 10 is curated from its story because the source
# switches to a cumulative glossary after the final chapter.
VOCABULARY = [
    (['afternoon', 'said', 'thing', 'she', 'her'], ['stack', 'shimmer', 'lump', 'clue', 'look around']),
    (['forest', 'know', 'bug'], ['creepy', 'neat', 'screech', 'buzz', 'afraid', 'frown', 'shiver']),
    (['air', 'land', 'different'], ['steamy', 'layer', 'canopy', 'understory', 'emergent', 'damp', 'vegetation', 'treetop']),
    (['million', 'army', 'ant'], ['ray', 'gloom', 'vine', 'moss', 'crackling', 'paddle', 'camouflage', 'surroundings']),
    (['pretty', 'river', 'mile', 'eat', 'snake'], ['canoe', 'Amazon', 'glance', 'belly', 'razor-sharp', 'scaly', 'wiggle']),
    (['monkey', 'fruit', 'bad'], ['poke', 'hurl', 'duck', 'rock', 'raindrop', 'thunder', 'spear']),
    (['find', 'umbrella', 'love'], ['freeze', 'beckon', 'thunder', 'kitten', 'jaguar', 'predator', 'growl']),
    (['forgot', 'look'], ['vampire', 'bat', 'mission', 'pat', 'leafy', 'streak', 'victim', 'rustle']),
    (['thanks', 'special', 'happy'], ['thud', 'cock', 'free', 'spell', 'clap', 'swing', 'vanish', 'tremble']),
    (['mango', 'taste', 'peach', 'mouse'], ['moonstone', 'halfway', 'proof', 'shudder', 'bother', 'shadow', 'golden', 'tag']),
]

SCENES = [
    [
        ('重返午后的树屋', '金色午后，安妮跑进弗洛格溪树林，杰克紧随其后；兄妹仰望最高橡树上重新出现的魔法树屋。'),
        ('袜子里的花生米', '树屋里，一只棕白小老鼠从红白条纹袜子小床中探出脑袋，安妮把它捧在掌心，杰克开心地笑。'),
        ('打开的雨林之书', '树屋阴影角落里敞开一本热带雨林图书，杰克和安妮带着花生米俯身查看，意识到新的线索已经出现。'),
    ],
    [
        ('神秘的热带雨林', '杰克举起封面画着高大密林的雨林书兴奋研究，安妮想到大虫子和蜘蛛，紧张地缩起肩膀。'),
        ('为了摩根鼓起勇气', '树屋午后光线中，杰克解释必须帮助摩根并保护正在消失的雨林，安妮深呼吸后坚定点头。'),
        ('旋转前往亚马孙', '杰克指向书中蓝天、绿叶和鲜花的图片，花生米钻进安妮口袋；狂风卷动书页，树屋开始旋转。'),
    ],
    [
        ('落在高高树冠上', '树屋停在明亮雨林树冠层的浓密绿叶间，彩蝶和热带鸟环绕；杰克、安妮与花生米从窗口向外张望。'),
        ('离地一百五十英尺', '杰克抓住正要爬出窗的安妮并指着书中雨林分层图，兄妹惊觉自己在离地极高的树顶层。'),
        ('爬向幽暗林下层', '兄妹沿绳梯穿过巨大枝叶向下攀爬，阳光渐暗，远处雨林地面深不可测，氛围神秘但适龄。'),
    ],
    [
        ('伪装的雨林生灵', '昏暗雨林地面上，兄妹站在巨树、藤蔓与苔藓之间看书，周围藏着与环境融为一体的青蛙、蜥蜴和昆虫。'),
        ('数不清的行军蚁', '落叶发出噼啪声，密集行军蚁像黑色河流穿过林地，鸟、蛙和蜥蜴纷纷逃开，兄妹惊讶后退。'),
        ('独木舟逃离蚁群', '杰克和安妮冲出树林来到棕色大河，把一根掏空原木当独木舟推离岸边，蚁群停在远处落叶间。'),
    ],
    [
        ('漂流亚马孙河', '兄妹坐在无桨独木舟上顺棕色亚马孙河漂流，头顶枝叶藤蔓交织，杰克翻书讲解四千英里长河。'),
        ('牙齿锋利的鱼与绿蛇', '安妮收回靠近蓝色红腹水虎鱼的手；杰克抓住垂下藤蔓却发现是一条温和逃开的长绿蛇，惊险而无伤。'),
        ('鳄鱼和小猴子', '漂浮树枝突然露出鳄鱼长嘴从独木舟旁游过，兄妹惊魂未定；树梢上一只小棕猴倒挂着好奇注视他们。'),
    ],
    [
        ('猴子投来红果子', '小棕猴在河岸树枝上把鲜红芒果丢向独木舟，杰克和安妮抱头躲闪，花生米从口袋探出头。'),
        ('暴雨困住独木舟', '雷雨突然笼罩亚马孙河，独木舟在风浪中摇摆，兄妹望着水中的水虎鱼与远处鳄鱼，急切寻找上岸办法。'),
        ('猴子伸出救援木棍', '小猴从岸边递出长木棍，安妮紧握另一端；猴子把独木舟稳稳拉回岸边，杰克露出惊喜感激。'),
    ],
    [
        ('跟着猴子躲进森林', '暴雨中小猴在树枝间摆荡并招手，安妮追进林中，杰克背着包随后赶来，巨大树冠像雨伞遮住雨水。'),
        ('安妮遇见美洲虎幼崽', '雨林地面上，安妮温柔陪一只金色黑斑美洲虎幼崽玩耍，小猴在上方观看，杰克翻书后露出担忧。'),
        ('母美洲虎逼近', '母美洲虎从巨树后保护性地走向幼崽，兄妹屏息不动；小猴轻拉它尾巴引开注意，让孩子安全逃走。'),
    ],
    [
        ('吸血蝙蝠的警告', '幽暗雨林中，杰克用书看到吸血蝙蝠夜间活动的插图，安妮和口袋里的花生米紧张环顾渐暗天空。'),
        ('迷路后让花生米带路', '兄妹在相反方向争论后把花生米放到落叶地面，小老鼠像白色闪光穿过浓密叶片，两人紧跟其后。'),
        ('终于找到树屋', '花生米沿绳索独自爬向高处树屋，杰克和安妮从巨树另一侧抬头发现它，松了一口气并开始攀爬。'),
    ],
    [
        ('回到树屋却没有回家书', '树屋内杰克写笔记，安妮翻找书堆却找不到宾夕法尼亚图书，窗外雨林天色渐暗，两人担心无法回家。'),
        ('猴子送来红色芒果', '小猴从窗口把红芒果递给安妮而不是投掷，安妮与它对视后恍然明白这是解除摩根魔咒所需之物。'),
        ('回家之书重新出现', '杰克惊喜指向重新显现的宾夕法尼亚图书，安妮捧着芒果，小猴挥手荡回森林，树屋随即在风中旋转。'),
    ],
    [
        ('芒果与月光石', '回到弗洛格溪的树屋中，安妮举起红熟芒果，杰克查书后把它放到发光字母 M 上、清澈月光石旁。'),
        ('完成一半任务', '兄妹对花生米温柔告别，芒果与月光石并排微微发光；他们明白已经找到四件物品中的两件。'),
        ('带着雨林领悟回家', '金色夕阳下，杰克和安妮跑出弗洛格溪树林、穿过街道冲向地面上的家，身后树影仿佛浮现猴子和美洲虎的回忆。'),
    ],
]
