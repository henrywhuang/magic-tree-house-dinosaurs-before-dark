#!/usr/bin/env python3
"""Book 9 titles, plot-aware page breaks, vocabulary and illustration briefs."""

TITLES = [
    'Master Librarians', 'The Reef', 'Mini-Sub', 'Fish City', 'Two Eyes',
    'C-R-A-C-K', 'Remain Calm', 'Swim for Your Life!', 'Ouch!', 'The True Pearl',
]

# Each pair starts scene 2 and scene 3. These are exact proofread story anchors.
SCENE_ANCHORS = [
    ('Jack and Annie ran up their quiet street to the Frog Creek woods.',
     'Yes, I sent them to you'),
    ('Jack threw his notebook and the ocean book into his pack.',
     'Annie turned the handle on the hatch of the mini-sub.'),
    ('Annie pressed a key with an arrow pointing right.',
     'Outside the glass was a strange world of bright moving color.'),
    ('What is that?',
     'Jack looked up. Two dolphins were peering in the window.'),
    ('Uh-oh. This doesn’t sound good',
     'Two eyes were staring out from behind a giant sea plant.'),
    ('He found a picture of an octopus and read aloud:',
     'Just then, Jack felt a drop hit his arm.'),
    ('Jack felt the water rising around his bare feet.',
     'I guess we’ll have to swim'),
    ('They both swam as fast, and as calmly, as they could.',
     'Float!'),
    ('I saw the shark when we were swimming',
     'Ouch!'),
    ('They walked through the woods, through leafy shadows and golden light.',
     'Don’t forget the dolphins'),
]

# Twelve grade-appropriate words or phrases per chapter. Every item occurs in
# the proofread story and feeds the shared read/meaning/phonics/spelling flow.
VOCABULARY = [
    (['dream', 'early', 'lovely', 'paper', 'library', 'research'],
     ['exclaimed', 'pale', 'robe', 'riddle', 'scroll', 'mysteriously']),
    (['pink', 'machine', 'seat', 'computer', 'reef', 'coral'],
     ['skeletons', 'oceanographers', 'submersibles', 'handle', 'hatch', 'panel']),
    (['row', 'screen', 'color', 'visit', 'arrow', 'command'],
     ['relief', 'steer', 'glued', 'planet', 'valleys', 'caves']),
    (['coral', 'sandy', 'clam', 'dolphins', 'smooth', 'riddle'],
     ['peeping', 'antlers', 'footstool', 'peering', 'slippery', 'flashed']),
    (['diary', 'crack', 'hull', 'broken', 'plant', 'rise'],
     ['defective', 'junkyard', 'helicopter', 'gasped', 'octopus', 'horror']),
    (['hugged', 'shy', 'impossible', 'breaks', 'breathed', 'enemies'],
     ['suckers', 'tentacles', 'drop', 'ceiling', 'shadowy', 'hammerhead']),
    (['suddenly', 'bottom', 'far', 'summer', 'distance', 'blank'],
     ['spurting', 'burst', 'bobbed', 'sparkled', 'bare', 'ankles']),
    (['life', 'distance', 'float', 'sink', 'fin', 'smoothly'],
     ['breast', 'zigzagging', 'struggling', 'slippery', 'hammerhead', 'clinging']),
    (['shallow', 'soaked', 'shell', 'oyster', 'pearl', 'treasure'],
     ['sparkled', 'flippers', 'resist', 'chattered', 'gracefully', 'ridges']),
    (['ancient', 'soaked', 'patch', 'shadows', 'chased', 'grinned'],
     ['slanted', 'tucked', 'leafy', 'along', 'squeezed', 'true']),
]

SCENES = [
    [
        ('共同的清晨梦境', '天刚蒙蒙亮，戴圆眼镜的8岁杰克站在厨房窗边想着摩根；7岁的安妮冲进门，说他们做了同一个梦。'),
        ('树屋与摩根归来', '雨后清新的弗洛格溪树林里，兄妹跑到高大橡树下，白发摩根穿着红色天鹅绒长袍从魔法树屋窗口微笑。'),
        ('图书馆大师的第一道谜题', '树屋内，摩根展开古老卷轴并递出《Ocean Guide》，向杰克和安妮说明成为图书馆大师需要解开四道谜题。'),
    ],
    [
        ('粉红珊瑚礁上的谜语', '清晨海边，魔法树屋落在粉红珊瑚礁上，兄妹展开卷轴朗读关于粗糙灰色外表与内在美的谜语。'),
        ('发现白色迷你潜艇', '赤脚的杰克和安妮走过浅水与珊瑚，发现一艘半停在水中的白色泡泡状迷你潜艇，杰克翻书研究。'),
        ('潜艇意外潜入深海', '狭小的迷你潜艇驾驶舱里，安妮误触电脑控制面板，潜艇从珊瑚礁滑落并潜入深蓝海水，杰克惊慌抓住舱门。'),
    ],
    [
        ('研究潜艇控制面板', '白色迷你潜艇内，杰克和安妮面对带星鱼、箭头和地图图标的控制屏，试着找出返回珊瑚礁的方法。'),
        ('安妮学会转向', '安妮按下向右箭头，潜艇转过方向；杰克扶着圆眼镜露出如释重负的表情，屏幕地图显示粉红珊瑚礁。'),
        ('窗外的彩色海底星球', '兄妹贴近宽大舷窗，惊叹红黄蓝珊瑚、海底山谷洞穴和五彩鱼群，像进入另一个明亮星球。'),
    ],
    [
        ('珊瑚礁鱼城', '迷你潜艇穿过温暖的热带珊瑚礁，海草、星鱼、水母、海马和成群彩鱼环绕窗外，杰克在本子上记录。'),
        ('巨型蛤蜊与黄貂鱼', '安妮指向长尾黄貂鱼和脚凳大小的巨型蛤蜊，杰克一手拿《Ocean Guide》一手写下观察结果。'),
        ('苏琪和山姆来访', '两只笑脸海豚用鼻子轻碰潜艇窗，安妮隔着玻璃亲吻苏琪，杰克在旁边忍不住笑，蓝色海水充满阳光。'),
    ],
    [
        ('电脑日志中的危险警告', '潜艇驾驶舱里，兄妹阅读屏幕上的船舶日志，发现艇壳裂缝、返航和报废警告，神情逐渐紧张。'),
        ('破损潜艇开始上浮', '安妮按下波浪图标，迷你潜艇穿过鱼群和摇摆海草慢慢上升，杰克紧盯屏幕寻找回礁路线。'),
        ('巨型章鱼露出两只眼睛', '巨大海草后先露出两只高尔夫球般的眼睛，随后八条长腕伸向潜艇，杰克和安妮隔着舷窗惊恐凝视。'),
    ],
    [
        ('章鱼抱住迷你潜艇', '巨型橙红章鱼用布满吸盘的八条腕紧紧包住白色潜艇，宽大舷窗后能看见杰克和安妮紧张的脸。'),
        ('翻书了解温和的章鱼', '驾驶舱内，杰克颤抖着翻《Ocean Guide》研究章鱼，安妮隔窗友好挥手，章鱼用巨大眼睛好奇回望。'),
        ('裂缝开始漏水', '一滴海水落在杰克手臂上，天花板裂缝分叉并滴水；安妮朝窗外章鱼恳求放手，气氛紧迫但适合儿童阅读。'),
    ],
    [
        ('漏水潜艇冲出海面', '白色迷你潜艇像软木塞般冲出闪亮海面，驾驶舱地板已经进水，兄妹短暂庆幸却发现危险未结束。'),
        ('控制屏熄灭', '海水升到兄妹膝盖，电脑屏幕突然变黑，远处粉红珊瑚礁清晰可见，杰克和安妮意识到必须游过去。'),
        ('保持冷静下水', '杰克把圆眼镜和海洋书装进背包，安妮打开舱门先滑入海水；两人以蛙泳姿势冷静离开正在下沉的潜艇。'),
    ],
    [
        ('鲨鱼鳍悄悄逼近', '杰克和安妮在深蓝海面安静蛙泳，远处黑色锤头鲨背鳍曲折靠近，杰克看见后努力保持冷静。'),
        ('筋疲力尽漂浮休息', '遥远粉红珊瑚礁前，兄妹仰躺海面漂浮，手脚沉重、神情疲惫，阳光在水波上闪烁。'),
        ('海豚及时救援', '两只友善灰海豚苏琪和山姆浮出水面，兄妹分别抓住背鳍，被平稳拉向珊瑚礁，危险转为喜悦。'),
    ],
    [
        ('拥抱海豚告别', '浅水珊瑚礁边，安妮拥抱苏琪，杰克也亲吻山姆；两只海豚随后跃出闪亮海面，兄妹挥手道谢。'),
        ('他们都在保护对方', '兄妹坐在温暖浅水中，浑身湿透地说出都看见鲨鱼却没有告诉对方，明白彼此一直在勇敢保护对方。'),
        ('灰色牡蛎解开谜题', '安妮踩到粗糙灰色牡蛎，杰克用湿漉漉的海洋书研究珍珠形成；回到树屋后，卷轴上浮现银色单词 OYSTER。'),
    ],
    [
        ('晨光中整理第一道答案', '清晨金色光线斜照进树屋，杰克卷起古老卷轴，安妮把湿海洋书摊在阳光里晾干。'),
        ('穿过金色树林回家', '戴圆眼镜的杰克和马尾辫安妮走过雨后树林的金色树影，谈论章鱼、鲨鱼和让一切值得的两只海豚。'),
        ('真正的珍珠', '兄妹走回温暖的家门，杰克微笑想念山姆，安妮打趣他；远方晨光中的海豚意象象征“牡蛎里真正的珍珠”。'),
    ],
]
