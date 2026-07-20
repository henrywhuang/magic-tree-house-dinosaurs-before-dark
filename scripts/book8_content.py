#!/usr/bin/env python3
"""Book 8 titles, plot-aware page breaks, vocabulary and illustration briefs."""

TITLES = [
    'By Moonlight', 'Space Motel', 'Open Sesame!', 'Moon Rabbits', 'Hang On!',
    'High Jump', 'The Moon Man', 'One Star to Another', 'Morgan', 'Earth Life',
]

# Each pair starts scene 2 and scene 3. These are exact proofread story anchors.
SCENE_ANCHORS = [
    ('Soon they left their street.', 'Squeak.'),
    ('Squeak, squeak!', 'Jack looked up. Annie was gone.'),
    ('Bulky white suits hung from hangers.', '“Ready?” said Annie.'),
    ('“Look!” Annie cried, laughing.', '“Oh, wow! Look!” said Annie.'),
    ('Only giant gray rocks and craters—and an American flag.', '“Oh, wow. A moon man!” said Annie.'),
    ('A giant rock had fallen into the narrow pass.', '“One, two, three—go!” she shouted'),
    ('Jack pulled out his notebook and pencil.', 'Finally he gave the notebook back to Jack.'),
    ('Jack and Annie crawled through the tree house window.', '“I’ve got an idea,” said Jack.'),
    ('Morgan shrugged.', '“But who turned you into a mouse?” said Annie.'),
    ('Jack opened his eyes. The ladder was gone.', 'The midnight air felt cool and moist.'),
]

# Proofread against the supplied OCR vocabulary panels and limited to words that
# occur in each chapter. The generator marks them in the story and selects up to
# ten challenging core words for the confirmed vocabulary-learning flow.
VOCABULARY = [
    (['clock', 'meet', 'day', 'night'], ['midnight', 'stream', 'dim', 'squint', 'equipment', 'shadowy', 'structure']),
    (['space', 'round', 'light', 'scientist', 'future'], ['motel', 'dome', 'base', 'diagram', 'chamber', 'airlock', 'period']),
    (['hour', 'glove', 'snowman'], ['sesame', 'button', 'spacesuit', 'two-way', 'airlock', 'visor', 'bulky', 'clumsily']),
    (['rabbit', 'everywhere', 'surprise', 'earth', 'half'], ['dust', 'feather', 'crater', 'off-balance', 'goof off', 'buggy', 'gravity', 'naturally']),
    (['drove', 'American', 'message', 'children', 'forever'], ['bump', 'hollow', 'buck', 'bronco', 'brake', 'telescope', 'barren', 'mankind', 'dizzy']),
    (['friendly', 'driver', 'step', 'radio', 'really'], ['tank', 'pass', 'crash', 'meteorite', 'relieved', 'tremble', 'tip over', 'bulky']),
    (['peace', 'mark', 'star', 'mean'], ['spaceman', 'refrigerator', 'jet', 'hand', 'visor', 'mini-spaceship', 'carefully']),
    (['hurry', 'toward', 'soon', 'miss', 'heart'], ['underwater', 'unlock', 'bulky', 'constellation', 'chant', 'whirling', 'blinding', 'scurry']),
    (['smile', 'yours', 'understand', 'page', 'trick'], ['certain', 'frown', 'sniff', 'shyly', 'absolutely', 'moment', 'magician', 'creature']),
    (['after', 'knowledge', 'alien', 'wrong'], ['breeze', 'universe', 'wonder', 'galaxy', 'rustle', 'moist', 'proof', 'scoff']),
]

SCENES = [
    [
        ('午夜唤醒杰克', '月光照进卧室，戴圆眼镜的8岁杰克刚惊醒，7岁的安妮穿着牛仔裤和连帽衫轻声催他出发。'),
        ('银色月光下的树屋', '兄妹沿着被满月染成银色的弗洛格溪树林前行，树影深处的魔法树屋在高大橡树上发光。'),
        ('第四件 M 宝物的线索', '树屋内，棕白小老鼠花生米坐在打开的月球图书上；杰克和安妮查看发光的 M、月光石、芒果和猛犸象骨。'),
    ],
    [
        ('2031 年的月球基地', '魔法树屋落在一间明亮的白色圆形大厅内，兄妹惊奇地打量曲面墙、登陆舱和未来设备。'),
        ('花生米的不安警告', '小老鼠花生米围着地板上的 M 焦急跑圈，安妮蹲下安慰它，杰克对照《Hello, Moon》研究基地地图。'),
        ('窗外真正的月球', '安妮在气闸巨门的窗边招手，杰克赶来后望见灰色环形山、高山、耀眼阳光和墨黑天空。'),
    ],
    [
        ('门外没有空气', '安妮正要按下气闸的开门按钮，杰克赶紧抓住她的手，指着月球书解释高温和无空气的危险。'),
        ('穿上白色宇航服', '储藏室里整齐挂着宇航服，兄妹互相扣好氧气罐和头盔，套上手套与大靴子，像两个笨拙的雪人。'),
        ('芝麻开门踏上月面', '透明面罩后的杰克和安妮并肩站在气闸中，安妮按下按钮，巨门滑开，灰白月面与黑色天空出现在眼前。'),
    ],
    [
        ('亿万年不消失的足迹', '杰克站在细粉般的月尘上翻书，周围是清晰足迹，远方蓝白地球在漆黑天空中发光。'),
        ('低重力月兔跳', '穿宇航服的安妮像月兔般高高跃过杰克，杰克也笨拙地弹跳，月尘在靴底下优美扬起。'),
        ('环形山里的月球车', '杰克跌在浅环形山边无法起身，安妮把他拉起；两人随即发现坑底停着四个巨轮的月球车。'),
    ],
    [
        ('月球车翻越灰色山口', '安妮驾驶四轮月球车在岩石和凹地间剧烈颠簸，杰克紧抓仪表台，车后扬起大片灰色月尘。'),
        ('人类首次登月地', '兄妹在星条旗、望远镜和登月纪念牌前迈着巨大慢步，杰克在笔记本上认真抄写和平留言。'),
        ('远方飞行的月球人', '安妮从月面望远镜中望见一个背着巨大喷气背包的神秘宇航员正在远处灰色地平线上方飞行。'),
    ],
    [
        ('急驶返回月球基地', '杰克驾驶月球车绕过环形山和乱石逃向基地，安妮坐在旁边提醒他减速，远方月球人逐渐靠近。'),
        ('陨石封住山口', '一块比安妮高两倍的巨大陨石卡在狭窄山口，月球车停在尘云前，兄妹翻书判断该如何脱困。'),
        ('跳过陨石后的身影', '兄妹利用低重力跃过陨石后都跌倒在月尘中，透过圆面罩仰望时，一位高大的神秘月球人出现在安妮上方。'),
    ],
    [
        ('神秘月球人伸手相助', '巨大白色宇航员背着如冰箱般的喷气背包，安妮先向他致意，然后走到跌倒的杰克身边把他拉起。'),
        ('笔记本上的无声交流', '杰克把写着和平问候的小笔记本与铅笔递到月球人戴着厚手套的巨大手中，安妮在一旁期待观看。'),
        ('星星组成的神秘地图', '月球人将画满星点的笔记本还给兄妹，杰克与安妮低头研究；远处月球人已靠喷气背包飞过黑暗山脊。'),
    ],
    [
        ('氧气将尽赶回白色圆顶', '兄妹在漆黑天空下用漂浮长步走向月球基地，杰克尽量屏住呼吸，白色圆顶与气闸就在前方。'),
        ('回到树屋放上星图', '脱下笨重宇航服的兄妹爬回树屋，安妮抱着花生米，杰克把星图放在 M 和三件宝物旁。'),
        ('星连成老鼠解除魔咒', '杰克用铅笔连起星点画出老鼠，兄妹咏唱四件 M 宝物；树屋被旋转的明亮魔法光芒充满。'),
    ],
    [
        ('花生米变回摩根', '耀眼光芒消散后，长白发、温柔神秘的摩根站在树屋内，杰克和安妮惊喜地明白她就是花生米。'),
        ('各次冒险的助手', '摩根微笑解释，她曾以小老鼠的尖声提醒忍者大师、雨林猴子和冰河巫师，兄妹回想起一路获得的帮助。'),
        ('摩根致谢并送他们回家', '摩根向勇敢的兄妹真诚致谢，把宾夕法尼亚图书递给安妮；三人在月球树屋内做好回归准备。'),
    ],
    [
        ('月光树屋里的告别', '树屋回到弗洛格溪的午夜，白发摩根在月光下告别，轻抚杰克的脸并拉拉安妮的马尾辫。'),
        ('魔法树屋消失', '兄妹站在巨大橡树下仰望，绳梯和树屋已经消失，树叶间只剩柔和月光，两人依依不舍。'),
        ('仰望月球想象宇宙', '兄妹沿安静街道走回温暖的家，安妮指向远处的满月，杰克思考神秘月球人是否来自另一个星系。'),
    ],
]
