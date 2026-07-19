#!/usr/bin/env python3
"""Book 7 titles, plot-aware page breaks, vocabulary and illustration briefs."""

TITLES = [
    "The 'M' Things", 'Bones', 'Brrr!', 'Cave Kids', 'Snow Tracks',
    'Song on the Wind', "The Sorcerer's Gift", 'The Great Parade',
    'Master of the Animals', 'This Age',
]

# Each pair starts scene 2 and scene 3. These are exact proofread story anchors.
SCENE_ANCHORS = [
    ('Squeak. A mouse sat', 'They walked over to the open book.'),
    ('Jack saw them, too:', 'Jack pulled on his pack'),
    ('A booming snore shattered', 'Under a cliff was a wide ledge.'),
    ('Ta-da!', 'He and Annie carried their stone lamps'),
    ('It showed a figure with human arms', 'Jack looked into his pack.'),
    ('Suddenly Jack heard a crack.', '"I hear music."'),
    ('Annie was sitting on a woolly mammoth.', 'Then the sorcerer reached into a pouch.'),
    ('But just then the mammoth let out a cry.', 'But the tiger had circled around the trees.'),
    ('Jack kept blowing until he ran out of breath.', 'After they disappeared into the tree house'),
    ('He held up the mammoth bone.', 'Jack and Annie ran through the Frog Creek woods'),
]

# Grade-5 useful words that actually occur in each chapter. The second list is
# recognition vocabulary; the generator chooses up to ten challenging core words.
VOCABULARY = [
    (['prepare', 'journey', 'special', 'silent', 'shadow'],
     ['dart', 'sigh', 'patch', 'clearing', 'carve', 'stack', 'corner', 'spin']),
    (['plain', 'cliff', 'mission', 'modern', 'enemy'],
     ['grove', 'chatter', 'huddle', 'caption', 'spear', 'trap', 'hurl', 'ancestor', 'fierce']),
    (['answer', 'strong', 'panic', 'bare', 'safe'],
     ['blackness', 'gasp', 'moan', 'booming', 'shatter', 'jagged', 'footprint', 'ledge', 'cozy']),
    (['plant', 'stone', 'clothes', 'borrow', 'careful'],
     ['hollow', 'braid', 'fiber', 'mammoth', 'flint', 'needle', 'wick', 'moss', 'cavern', 'prehistoric']),
    (['power', 'human', 'mask', 'friend', 'track'],
     ['gallery', 'painting', 'beast', 'antler', 'sorcerer', 'owl', 'flute', 'shadow', 'peer']),
    (['freeze', 'cover', 'distance', 'ground', 'sound'],
     ['swirl', 'footprint', 'vanish', 'sabertooth', 'fang', 'cave in', 'heap', 'pit', 'haunting', 'eyehole']),
    (['tight', 'burn', 'kindness', 'smooth', 'speed'],
     ['tug', 'socket', 'puzzle', 'robe', 'woolly', 'tusk', 'kneel', 'pouch', 'hollow', 'plod', 'squint']),
    (['distance', 'join', 'closer', 'sunlight', 'wildly'],
     ['herd', 'elk', 'reindeer', 'prance', 'bison', 'escort', 'sparkle', 'bound', 'slink', 'plunge', 'glint']),
    (['horror', 'breath', 'world', 'positive', 'direction'],
     ['glare', 'growl', 'stomp', 'snarl', 'lumber', 'stroke', 'prehistoric', 'raise', 'spear', 'absolutely']),
    (['soft', 'secret', 'free', 'pause', 'safe'],
     ['spell', 'gather', 'glance', 'rosy', 'age', 'hunt', 'trap', 'starve', 'sidewalk', 'mammoth bone']),
]

SCENES = [
    [
        ('放学路过弗洛格溪', '温暖的傍晚，杰克和安妮刚上完游泳课，披着浴巾路过弗洛格溪树林；安妮跑向魔法树屋，戴圆眼镜的杰克无奈跟上。'),
        ('M 字上的两件宝物', '树屋内，棕白小老鼠花生米蹲在窗沿；兄妹俯看地板上的大字母 M，月光石和芒果放在上面，两人发现它们都以 M 开头。'),
        ('穿着泳衣飞向冰河时代', '杰克和安妮打开画着岩石与飞雪的书，安妮指向雪地；杰克刚意识到他们只穿泳衣，树屋已在狂风和书页中旋转。'),
    ],
    [
        ('雪原上的树屋', '灰色天空下飞雪纷纷，树屋落在光秃高树上，远处是白色平原和高大岩崖；裹着浴巾的兄妹冷得发抖，花生米躲进背包。'),
        ('岩崖上的克鲁马农人', '杰克拿着《冰河时代生活》望向岩崖，四个穿皮毛的克鲁马农人手持长矛站在风雪中，安妮又好奇又紧张。'),
        ('闯入洞熊的洞穴', '兄妹戴着游泳护目镜、顶着浴巾跑进阴暗山洞，地面散落着大量古老骨头；杰克在洞口读到这是巨型洞熊的家。'),
    ],
    [
        ('黑暗中的呼噜声', '漆黑山洞里满地是骨头，杰克摸索着寻找安妮；深处传来低沉呼噜，一只巨大洞熊的模糊轮廓在黑暗中熟睡。'),
        ('逃出洞熊的家', '洞熊的呼噜震动空气，杰克和安妮惊跳着跨过骨头奔出山洞，沿着飞雪中的崎岖岩壁快速逃离。'),
        ('金色火光的山洞', '风雪中，兄妹发现另一个岩棚下的洞口，温暖金色火光从里面照出，与外面蓝灰色冰雪形成安全温馨的对比。'),
    ],
    [
        ('克鲁马农人的家', '洞穴火堆旁摆着石刀、石斧、编织绳和骨笛，杰克读书记笔记，安妮好奇观察堆叠整齐的驯鹿皮。'),
        ('变成洞穴小孩', '安妮穿上带兜帽的长毛皮外套向杰克展示，杰克也套上柔软皮衣；两人把浴巾和护目镜留下当谢礼，花生米从背包探头。'),
        ('灯火照亮洞穴壁画', '穿毛皮外套的兄妹双手捧着石灯穿过狭小隧道，在高大洞穴中照亮红黑黄色的熊、狮、猛犸象和毛犀壁画。'),
    ],
    [
        ('两万五千年前的画', '石灯闪烁，杰克翻书解释壁画，安妮仰望墙上奔跑的麋鹿、野牛、毛犀与猛犸象，古老动物仿佛在火光中活过来。'),
        ('动物大师的形象', '墙上出现长着人类四肢、鹿角和猫头鹰面孔、手持骨笛的神秘形象，安妮惊喜地相信他是摩根的朋友。'),
        ('花生米留下雪地足迹', '兄妹回到火堆旁发现背包里的花生米不见了，他们焦急地搜寻；洞口新雪上一串小鼠脚印通向白色荒原。'),
    ],
    [
        ('足迹在风雪中消失', '穿驯鹿皮外套的杰克和安妮追随小脚印走进雪原，狂风卷起细雪逐渐覆盖痕迹，远处岩崖上一只剑齿虎静静俯视。'),
        ('掉进雪下的陷阱', '兄妹向光秃树林奔跑时，藏在雪下的树枝忽然塌陷，两人跌入深坑，四周是无法攀爬的雪壁。'),
        ('风中的骨笛歌声', '深坑上方传来神秘音乐，戴鹿角与猫头鹰面具的高大巫师出现在雪光中，花生米从他身边探头，兄妹惊讶仰望。'),
    ],
    [
        ('神秘绳索救援', '巫师将粗绳抛入陷坑，安妮双手紧握、脚蹬土壁缓缓上升，杰克在坑底观察，好奇是谁在另一端拉绳。'),
        ('拉绳的猛犸象露露', '杰克被拉上雪地后，看见安妮和花生米坐在毛发蓬松、长着巨大弯牙的毛猛犸象上，绳索另一端绕在它的脖子上。'),
        ('巫师赠送猛犸象骨笛', '巫师从皮袋里取出带六个孔的光滑白色骨笛送给杰克，眼神温和；随后兄妹骑着露露穿过阳光闪耀的雪原。'),
    ],
    [
        ('冰原上的动物大游行', '杰克、安妮和花生米骑着露露前行，麋鹿、驯鹿、毛犀和野牛在远处优雅同行，阳光把雪地照得闪闪发光。'),
        ('剑齿虎从后方追来', '露露突然惊叫狂奔，其他动物四散而去；剑齿虎贴着阳光下的雪面从后方追赶，兄妹紧抱猛犸象长毛。'),
        ('树屋前被虎拦住', '露露奔到高树林时，剑齿虎已绕到魔法树屋与猛犸象之间，低头逼近；长白獠牙在阳光中闪亮，但画面无血腥。'),
    ],
    [
        ('骨笛让剑齿虎停下', '骑在露露背上的杰克双手发抖地吹响骨笛，安妮鼓励他；剑齿虎在奇异音乐中暂停，猛犸象守护性地踏地。'),
        ('远古乐声送走剑齿虎', '杰克闭眼深呼吸，继续吹奏来自另一个世界般的音乐，剑齿虎转身走向岩崖，安妮欣喜指着它离开。'),
        ('归还皮衣告别冰河时代', '夕阳下，露露走向远方，兄妹在树屋前放下驯鹿皮外套；远处四个克鲁马农人穿过雪原，树屋在道别声中旋转。'),
    ],
    [
        ('回到温暖的傍晚', '魔法树屋回到夏日弗洛格溪，鸟儿歌唱、空气柔和；穿回日常探险服的杰克推推圆眼镜，安妮轻抚花生米。'),
        ('第三件 M 宝物', '杰克把白色猛犸象骨笛放在地板大字母 M 上，与芒果和月光石排在一起，兄妹知道再找一件就能解开摩根的魔咒。'),
        ('安全回家吃晚餐', '玫瑰色夕阳中，杰克和安妮穿过树林和街道跑向温暖的家，笑着想象父母从超市“猎获”了意大利面、肉丸和披萨。'),
    ],
]
