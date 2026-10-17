#!/usr/bin/env python3
"""Author and append the Book 20 (Dingoes at Dinnertime) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-19.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 20's text is proofread from the audiobook transcript
(book20_source.txt); its chapter text is reconstructed here exactly as
``rebuild_docx_book`` builds it (book20_text + rebuild_book20 FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book20_text as bt
import rebuild_book20 as rb
import rebuild_docx_book as rdb

TARGET = ROOT / 'data' / 'questions.json'

# Balanced, non-repeating answer positions (one five-question row per chapter).
# Totals across the book: A 12, B 13, C 12, D 13.
ANSWER_PATTERNS = ('DBADC', 'ACBDA', 'CDACB', 'BADBC', 'CBDAB',
                   'DCADB', 'ABCAD', 'BDCBA', 'CADCB', 'DABDC')

META = {
    'DETAIL': ('RL.5.1', 'Explicit comprehension', 1, '基础'),
    'SEQUENCE': ('RL.5.3', 'Sequence', 2, '进阶'),
    'PLOT RELATION': ('RL.5.3', 'Character/event relationship', 2, '进阶'),
    'VOCABULARY IN CONTEXT': ('RL.5.4', 'Vocabulary in context', 1, '基础'),
    'SUMMARY': ('RL.5.2', 'Summary', 2, '进阶'),
    'INFERENCE': ('RL.5.1', 'Evidence-based inference', 2, '进阶'),
    'CAUSE / PURPOSE / RESULT': ('RL.5.3', 'Cause / purpose / result', 2, '进阶'),
}


def rationale_for(tag, correct):
    if tag == 'VOCABULARY IN CONTEXT':
        return f'结合原句语境，这个词在这里最接近“{correct}”。'
    if tag == 'SEQUENCE':
        return f'按照本章事件先后顺序，最先/最后发生的是：{correct}'
    if tag == 'SUMMARY':
        return f'这个选项同时保留了本章开端与后续的关键事件：{correct}'
    if tag == 'INFERENCE':
        return f'原文细节支持这一推断：{correct}'
    if tag == 'PLOT RELATION':
        return f'结合人物与事件的关系，正确的是：{correct}'
    if tag == 'CAUSE / PURPOSE / RESULT':
        return f'结合事件的原因、目的或结果，正确关系是：{correct}'
    return f'原文直接写到：{correct}'


CH = {
    1: [
        ('DETAIL', 'Which gifts from Jack and Annie’s first three trips are sitting beside Morgan’s note?',
         {'A': 'A pocket watch from the Titanic, an eagle’s feather from the prairie skies, and a lotus flower from India.',
          'B': 'A seashell from the ocean, a buffalo horn from the prairie, and a tiger’s tooth from India.',
          'C': 'A gold coin from a sunken ship, an eagle’s egg from the mountains, and a mango from India.',
          'D': 'A pocket watch from the Titanic, a piece of painted bark, and a kangaroo’s tooth.'}, 'A',
         ['Two, an eagle’s feather from the prairie skies.',
          'Three, a lotus flower from a forest in India.']),
        ('VOCABULARY IN CONTEXT', 'Jack “knew the note by heart now.” To know something “by heart” means to ___.',
         {'A': '能完整地背出来；牢牢记住', 'B': '打心底里喜欢', 'C': '心里感到害怕', 'D': '刚刚第一次读到'}, 'A',
         ['He knew the note by heart now:']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack say, “We must be going to Australia”?',
         {'A': 'They still need a gift from a kangaroo, and Australia is where kangaroos live.',
          'B': 'Morgan’s note says that the last gift is hidden somewhere in Australia.',
          'C': 'Annie heard a kangaroo calling to them from the Frog Creek woods.',
          'D': 'The lotus flower they brought home from India first came from Australia.'}, 'A',
         ['We just need to get a gift from a kangaroo,',
          '“We must be going to Australia,” said Jack. “That’s where kangaroos live.”']),
        ('INFERENCE', 'After Teddy scratches at a book, Jack picks it up and says, “What’d I tell you?” before showing Annie the cover. Why does he say this?',
         {'A': 'The title, Adventure in Australia, proves that his guess about the trip was right.',
          'B': 'He is upset that Teddy scratched and damaged the cover of the book.',
          'C': 'He had told Annie that their next trip would take them back to India.',
          'D': 'He had told Annie that Teddy knew how to read the titles of books.'}, 'A',
         ['“What’d I tell you?” he said. He showed the cover to Annie.',
          'The title was Adventure in Australia.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Annie hears Teddy barking from the Frog Creek woods.',
          'B': 'Jack and Annie hug Teddy inside the tree house.',
          'C': 'Teddy scratches at a book lying in the corner.',
          'D': 'Jack points at a picture of a forest and makes a wish.'}, 'A',
         ['“Teddy’s calling us,” said Annie.',
          'A faint bark came from the distance: Arf! Arf!']),
    ],
    2: [
        ('DETAIL', 'According to Jack’s book, what does the name “koala” mean?',
         {'A': 'No drink.', 'B': 'Big foot.', 'C': 'Sleepy bear.', 'D': 'Gum-tree eater.'}, 'A',
         ['The name koala means “no drink,” because koalas rarely drink water.']),
        ('VOCABULARY IN CONTEXT', '“The emus gave the little dog a haughty look. Then they turned and walked proudly away.” Here “haughty” means ___.',
         {'A': '傲慢的；高傲的', 'B': '害怕的；胆小的', 'C': '友好的；亲切的', 'D': '饥饿的；贪吃的'}, 'A',
         ['The emus gave the little dog a haughty look. Then they turned and walked proudly away.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why are wildfires a threat to koalas?',
         {'A': 'Koalas are slow-moving and can’t escape the smoke and flames.',
          'B': 'Koalas are afraid of loud noises and run straight into the fire.',
          'C': 'Koalas drink only from streams, and the streams dry up in a fire.',
          'D': 'Koalas sleep in caves, and the smoke quickly fills up the caves.'}, 'A',
         ['Wildfires are also a threat. Koalas are slow-moving and can’t escape the smoke and flames.']),
        ('INFERENCE', 'Annie asks the sleeping koala, “Don’t you feel well?” Why does Jack tell her not to worry?',
         {'A': 'His book says koalas sleep during the hot day, so the koala is just sleepy, not sick.',
          'B': 'His book says koalas are not really bears, so they can never get sick.',
          'C': 'He can tell that the koala is only pretending to be asleep.',
          'D': 'He knows that someone who takes care of koalas lives nearby.'}, 'A',
         ['“Don’t worry,” said Jack. “Listen to this.”',
          'Koalas, like kangaroos, are active at night and sleep during the day when the sun is hot.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie land in a dry Australian forest, smell smoke they think comes from campers, and meet emus and a sleepy koala while they look for water.',
          'B': 'Jack and Annie land in a rainy forest, swim in a cool stream, and meet a mother kangaroo and her baby in the tall grass.',
          'C': 'Jack and Annie land beside a busy campsite, eat dinner with the campers, and watch the emus race each other.',
          'D': 'Jack and Annie land in a burning forest, run into a dark cave, and hide from the flames with a koala.'}, 'A',
         ['The tree house had landed in a scrubby forest filled with droopy plants and dry brown trees.',
          '“Maybe people are camping over there,” Jack said.']),
    ],
    3: [
        ('DETAIL', 'According to Jack’s book, what does “macropod,” the scientists’ name for the kangaroo, mean?',
         {'A': 'Big foot.', 'B': 'No drink.', 'C': 'Laughing donkey.', 'D': 'Baby in a pouch.'}, 'A',
         ['Scientists call the kangaroo a macropod, which means “big foot.”']),
        ('VOCABULARY IN CONTEXT', '“Jack couldn’t believe how graceful the kangaroo was. She seemed to fly through the air, then land as softly as a butterfly.” “Graceful” means ___.',
         {'A': '优美的；动作轻盈优雅的', 'B': '笨重的；动作缓慢的', 'C': '凶猛的；样子吓人的', 'D': '感激的；心怀感谢的'}, 'A',
         ['Jack couldn’t believe how graceful the kangaroo was.',
          'She seemed to fly through the air, then land as softly as a butterfly.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why is the kookaburra also called the “laughing donkey”?',
         {'A': 'The strange sound it makes reminds people of a braying donkey.',
          'B': 'It has a long face and big ears just like a donkey.',
          'C': 'It likes to ride on the backs of donkeys and laugh.',
          'D': 'It carries heavy loads of sticks back to its nest.'}, 'A',
         ['This is because the strange sound it makes reminds people of a braying donkey.']),
        ('INFERENCE', 'The kangaroo starts stamping her feet, then she freezes, and Teddy growls from Jack’s backpack. What do these clues suggest?',
         {'A': 'They sense danger nearby—wild dogs are creeping toward the clearing.',
          'B': 'The kangaroo wants Annie to start another hopping contest.',
          'C': 'Teddy is hungry and wants to eat the kangaroo’s grass.',
          'D': 'A big thunderstorm is about to roll into the dry forest.'}, 'A',
         ['Grrr. Teddy growled from Jack’s backpack.',
          'A moment later, three dogs crept silently into the clearing.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The wild dogs race after the kangaroo and her baby.',
          'B': 'Annie and the kangaroo hop around each other.',
          'C': 'Jack reads about the laughing kookaburra.',
          'D': 'The kangaroo wakes up and glares at Jack and Annie.'}, 'A',
         ['Howling, the wild dogs raced after the kangaroo and her baby.']),
    ],
    4: [
        ('DETAIL', 'According to Jack’s book, what is the biggest enemy of the kangaroo?',
         {'A': 'The dingo, the wild dog of Australia.',
          'B': 'The emu, the large bird that doesn’t fly.',
          'C': 'The kookaburra, the laughing bird.',
          'D': 'The koala, which lives in gum trees.'}, 'A',
         ['The biggest enemy of the kangaroo is the dingo, the wild dog of Australia.']),
        ('VOCABULARY IN CONTEXT', 'When Jack sees the big black cloud of smoke, “A feeling of dread came over Jack.” “Dread” means ___.',
         {'A': '恐惧；担心坏事就要发生', 'B': '兴奋；非常期待', 'C': '困倦；很想睡觉', 'D': '饥饿；很想吃东西'}, 'A',
         ['A feeling of dread came over Jack.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why might a mother kangaroo throw her joey out of her pouch when dingoes chase her?',
         {'A': 'Without the extra weight, she can leap faster and farther and lead the dingoes away from her baby.',
          'B': 'She is angry that Jack and Annie woke her up, so she no longer wants to carry him.',
          'C': 'Her joey has grown too big and too heavy to ride in her pouch ever again.',
          'D': 'She wants Jack and Annie to keep her baby and take him back home with them.'}, 'A',
         ['Without the extra weight in her pouch, she can leap faster and farther.',
          'She then leads the dingoes away from her baby.']),
        ('INFERENCE', 'When Annie says Jack looks “just like a mother kangaroo,” Jack says, “Oh, brother.” But then he pats the baby’s soft fur. This shows that Jack ___.',
         {'A': 'feels a little silly but still cares about Joey',
          'B': 'is angry at Annie and wants to give Joey back',
          'C': 'is afraid that Joey will bite his fingers',
          'D': 'does not like animals with soft fur'}, 'A',
         ['“There,” Annie said. “You look just like a mother kangaroo.”',
          '“Oh, brother,” said Jack. But he patted the baby’s soft fur.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie find the baby kangaroo his mother left behind, carry him in Jack’s pack, and then realize the smoke is coming from a wildfire.',
          'B': 'Jack and Annie chase the dingoes away, bring the joey back to his mother, and receive a special gift from her.',
          'C': 'Jack and Annie find the campers cooking dinner, share their water, and fall asleep beside the warm bonfire.',
          'D': 'Jack and Annie lose the joey in the tall grass, look for him all afternoon, and then hurry back to the tree house.'}, 'A',
         ['Beside her in the grass was the baby kangaroo.',
          '“We’re looking at a wildfire!” he said.']),
    ],
    5: [
        ('DETAIL', 'As the fire spreads, which animals fly or race past Jack and Annie?',
         {'A': 'The kookaburra and the emus.', 'B': 'The koala and the dingoes.',
          'C': 'The mother kangaroo and her joey.', 'D': 'A flock of blackbirds and the emus.'}, 'A',
         ['Just then the kookaburra flew through the sky, cackling. The emus raced by at top speed.']),
        ('VOCABULARY IN CONTEXT', '“Branches cracked and fell from the trees. Smoke billowed everywhere.” Here “billowed” means ___.',
         {'A': '（烟雾）大团大团地翻滚涌出', 'B': '慢慢地消散不见', 'C': '被大雨浇灭了', 'D': '静静地飘落到地上'}, 'A',
         ['Branches cracked and fell from the trees. Smoke billowed everywhere.']),
        ('PLOT RELATION', 'Annie says, “I have to get something!” and runs off. Later she comes back through the smoke carrying the koala. How does this connect to what Jack read about koalas earlier?',
         {'A': 'Koalas are slow-moving and can’t escape fires, so Annie went back to save the koala.',
          'B': 'Koalas can lead people out of the smoke, so Annie went to find a guide.',
          'C': 'Koalas are the gift Morgan asked for, so Annie wanted to bring one home.',
          'D': 'Koalas know where the tree house is, so Annie asked the koala for help.'}, 'A',
         ['“I’ll catch up!” said Annie. “I have to get something!”',
          'She was carrying the koala.']),
        ('CAUSE / PURPOSE / RESULT', 'Smoke hides the treetops, and Jack stumbles blindly through the brush. How does he find his way?',
         {'A': 'He follows the sound of Teddy’s barking.',
          'B': 'He follows a map in the Australia book.',
          'C': 'He follows the running emus to safety.',
          'D': 'He follows the sound of Annie’s singing.'}, 'A',
         ['All he could do was follow the sound of Teddy’s barking.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Teddy barks and vanishes inside a cave.',
          'B': 'Annie dashes off in the other direction.',
          'C': 'The emus race by at top speed.',
          'D': 'Annie appears through the smoke carrying the koala.'}, 'A',
         ['Teddy barked again and vanished inside the cave.']),
    ],
    6: [
        ('DETAIL', 'When Teddy howls in the dark cave, what begins to glow?',
         {'A': 'A white line that grows into a giant snake, with handprints below it.',
          'B': 'A pair of yellow eyes belonging to a dingo hiding in the dark.',
          'C': 'A painting of a mother kangaroo carrying her joey in her pouch.',
          'D': 'A small fire that the campers left burning on the cave floor.'}, 'A',
         ['The glowing line grew until it looked like a giant snake.',
          'Then glowing handprints appeared below the snake.']),
        ('VOCABULARY IN CONTEXT', '“Suddenly Jack felt something thump against his leg. He stopped and gasped.” To “gasp” means to ___.',
         {'A': '（因吃惊或害怕）倒抽一口气', 'B': '哈哈大笑', 'C': '打一个大哈欠', 'D': '轻轻地哼歌'}, 'A',
         ['Suddenly Jack felt something thump against his leg. He stopped and gasped.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie hold hands as they walk into the cave?',
         {'A': 'It is too dark to see, so they stay together and follow Teddy’s bark.',
          'B': 'They are dancing the same way Annie danced with the kangaroo.',
          'C': 'Morgan’s note told them to hold hands inside every cave.',
          'D': 'The cave floor is slippery with water from the rain.'}, 'A',
         ['“I can’t see anything,” said Jack.',
          '“I guess we’ll have to follow Teddy’s bark,” said Annie. “Let’s hold hands.”']),
        ('INFERENCE', 'Right after Jack and Annie put their hands inside the painted handprints, they hear a loud boom, and soon they step out into a pouring rain. What does this hint?',
         {'A': 'Touching the painting seemed to bring a storm, as if the painting had some kind of magic.',
          'B': 'The booming sound came from the walls of the cave falling down behind them.',
          'C': 'The fire had reached the cave and was cracking the rocks into pieces.',
          'D': 'Teddy was making the booming noise to scare the dingoes away.'}, 'A',
         ['She let go of Jack and put her hand inside one of the painted handprints.',
          '“It sounded like thunder,” said Annie.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie hold hands and follow Teddy into a dark cave, put their hands on a glowing snake painting, and come out into a thunderstorm.',
          'B': 'Jack and Annie hide in a cave all night until the fire burns out, and then they find the tree house in the morning.',
          'C': 'Jack and Annie find the mother kangaroo hiding deep in a cave and give her baby back to her.',
          'D': 'Jack and Annie get lost in a dark cave after Teddy runs away, and they call for Morgan to help them.'}, 'A',
         ['Jack and Annie climbed onto the rock ledge and stepped into the cave.',
          'Annie pulled Jack toward the mouth of the cave and out into a pouring rain.']),
    ],
    7: [
        ('DETAIL', 'Where does Annie put the koala after the rain begins?',
         {'A': 'In the fork of two branches of an unburned gum tree.',
          'B': 'Inside Jack’s backpack, right next to Joey.',
          'C': 'On the rock ledge at the mouth of the cave.',
          'D': 'Back inside the magic tree house.'}, 'A',
         ['They walked over to the unburned gum tree. Annie placed the koala in the fork of two branches.']),
        ('VOCABULARY IN CONTEXT', 'When Jack looks back at the woods, “misty steam was rising from the charred ground and burning bushes.” Here “charred” means ___.',
         {'A': '烧焦的；烧黑的', 'B': '长满青苔的', 'C': '冻得硬邦邦的', 'D': '刚翻过土的'}, 'A',
         ['misty steam was rising from the charred ground and burning bushes.',
          'The heavy rain was putting out the wildfire.']),
        ('INFERENCE', 'Annie says the storm “wasn’t just luck. It was magic,” but Jack answers, “That doesn’t make sense.” What does this show about Jack and Annie?',
         {'A': 'Annie believes the glowing painting brought the storm, while Jack looks for a sensible explanation.',
          'B': 'Jack believes in magic much more than Annie does.',
          'C': 'Both of them think the storm came only by luck.',
          'D': 'Annie thinks the koala brought the storm, and Jack agrees with her.'}, 'A',
         ['“Yeah, the glowing hands and the snake,” said Annie. “Somehow they brought the storm.”',
          '“That doesn’t make sense,” said Jack.']),
        ('PLOT RELATION', 'Teddy leads Jack and Annie to the Australia book lying on the wet ground. Why does finding the book tell them they are in the right spot?',
         {'A': 'Jack had left the book on the ground in the spot where they found Joey.',
          'B': 'Morgan had placed the book there to mark the way to the tree house.',
          'C': 'The mother kangaroo had carried the book there in her pouch.',
          'D': 'The wind from the storm had blown the book out of the cave.'}, 'A',
         ['He stood over the Australia book. It was wet but not burned.',
          'I left our book in the spot where we found Joey.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'They hear the squishy sound of big feet slapping through mud.',
          'B': 'Annie places the koala in an unburned gum tree.',
          'C': 'Teddy finds the wet Australia book.',
          'D': 'The heavy rain turns into a drizzle.'}, 'A',
         ['It was the sound of big feet slapping through mud.']),
    ],
    8: [
        ('DETAIL', 'What gift does the mother kangaroo give Jack and Annie?',
         {'A': 'A small piece of bark with a tiny painting of the snake on it.',
          'B': 'A soft tuft of brown fur from her baby joey.',
          'C': 'A smooth stone from the floor of the painted cave.',
          'D': 'A gum leaf she picked from the koala’s tree.'}, 'A',
         ['Then she bent over and used a front paw to pick up a small piece of bark from the wet grass.',
          'There was a tiny painting on it. It was just like the snake painting in the cave.']),
        ('VOCABULARY IN CONTEXT', 'Jack’s book says, “In special ceremonies, they sometimes honor the Rainbow Serpent by painting their handprints on the magic snake.” A “ceremony” is ___.',
         {'A': '仪式；典礼', 'B': '比赛；竞赛', 'C': '课堂；学校', 'D': '集市；市场'}, 'A',
         ['In special ceremonies, they sometimes honor the Rainbow Serpent by painting their handprints on the magic snake.']),
        ('CAUSE / PURPOSE / RESULT', 'After hearing what Jack reads, why does Annie think the Rainbow Serpent sent the rain?',
         {'A': 'In Dreamtime the Rainbow Serpent sends life-giving rain, and putting their hands on its painting was like a special ceremony.',
          'B': 'The mother kangaroo showed Annie that the Rainbow Serpent lives up in the rain clouds.',
          'C': 'Jack’s book says that the Rainbow Serpent puts out every wildfire in Australia.',
          'D': 'Teddy barked at the sky to tell Annie that the snake was on its way.'}, 'A',
         ['In Dreamtime, there is a Rainbow Serpent who sends life-giving rain.',
          'It was like a special ceremony.']),
        ('INFERENCE', 'Jack says the Rainbow Serpent is “in Dreamtime, not real time.” Then Annie points to a rainbow in the sky, and Jack shivers even though the air is warm. What does his shiver suggest?',
         {'A': 'He is beginning to feel that something mysterious and magical really happened.',
          'B': 'He is cold because a chilly wind has started to blow through the forest.',
          'C': 'He is afraid the mother kangaroo will come back and stamp at them.',
          'D': 'He is getting sick from breathing in smoke from the wildfire.'}, 'A',
         ['A rainbow curved across the blue Australian sky.',
          'Though the air was warm again, he shivered.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Joey’s mother returns, gives Jack and Annie a bark painting of the Rainbow Serpent as a thank-you, and the children head home with all four gifts.',
          'B': 'Joey’s mother never returns, so Jack and Annie decide to take Joey home with them to Frog Creek.',
          'C': 'The dingoes come back and chase the mother kangaroo away, and Teddy fights them off in the rain.',
          'D': 'Jack and Annie paint their own handprints on a piece of bark and give it to the mother kangaroo as a gift.'}, 'A',
         ['The mother kangaroo bounded out of the trees.',
          '“Hey, we have all four gifts now,” said Annie.']),
    ],
    9: [
        ('DETAIL', 'According to Morgan, what does the eagle’s feather teach the boy?',
         {'A': 'That a small creature can be one of the bravest.',
          'B': 'That time is very precious and must be used wisely.',
          'C': 'That nature holds many wonders.',
          'D': 'That there is wisdom in the traditions of ancient peoples.'}, 'A',
         ['The eagle’s feather teaches him that a small creature can be one of the bravest.']),
        ('VOCABULARY IN CONTEXT', 'Morgan says the watch “teaches him that time is very precious. It must be used wisely.” Here “precious” means ___.',
         {'A': '宝贵的；珍贵的', 'B': '无聊的；没意思的', 'C': '飞快的；匆忙的', 'D': '免费的；不要钱的'}, 'A',
         ['This watch teaches him that time is very precious. It must be used wisely.']),
        ('PLOT RELATION', 'Morgan says, “Sometimes the boy didn’t want to study other times and places.” Which gift teaches him the lesson he needed for this?',
         {'A': 'The bark painting of the Rainbow Serpent.',
          'B': 'The lotus flower from the forest in India.',
          'C': 'The pocket watch from the Titanic.',
          'D': 'The eagle’s feather from the Lakota Indians.'}, 'A',
         ['Sometimes the boy didn’t want to study other times and places,',
          'This painting teaches him there is mystery, magic, and wisdom in the traditions of ancient peoples.']),
        ('INFERENCE', 'Morgan keeps talking about “the boy,” and Jack asks, “What boy?” Based on the end of the chapter, who was the boy Morgan meant?',
         {'A': 'Teddy—the little dog under the spell was really a boy.',
          'B': 'Jack, because he sometimes wastes time and feels afraid.',
          'C': 'A boy from Camelot whom Jack and Annie have never met.',
          'D': 'One of the children Jack and Annie met on the Titanic.'}, 'A',
         ['He was no longer a dog.',
          'He was a boy.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Annie shows Morgan the piece of painted bark.',
          'B': 'Morgan explains what the lotus flower teaches.',
          'C': 'Jack asks Morgan, “What boy?”',
          'D': 'Teddy changes from a dog into a boy.'}, 'A',
         ['She reached into Jack’s pack and pulled out the piece of painted bark.']),
    ],
    10: [
        ('DETAIL', 'According to Morgan, what is Ted training to do?',
         {'A': 'To work in Morgan’s library at Camelot.',
          'B': 'To become a brave knight of Camelot.',
          'C': 'To be a sailor on great ships at sea.',
          'D': 'To teach school in the town of Frog Creek.'}, 'A',
         ['“Ted is training to work in my library at Camelot,” said Morgan.']),
        ('VOCABULARY IN CONTEXT', 'After Morgan tells him to ask before trying her spells, “The boy grinned sheepishly.” “Sheepishly” means ___.',
         {'A': '不好意思地；有点难为情地', 'B': '得意洋洋地', 'C': '气呼呼地', 'D': '吓得发抖地'}, 'A',
         ['The boy grinned sheepishly.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan tell the boy, “I hope next time you’ll ask before trying the spells in my spell book”?',
         {'A': 'He had tried her spells without asking and accidentally changed himself into a dog.',
          'B': 'He had lost her spell book somewhere on the Titanic.',
          'C': 'He had used a spell to make the tree house spin too fast.',
          'D': 'He had turned Jack and Annie into kangaroos by mistake.'}, 'A',
         ['And I hope next time you’ll ask before trying the spells in my spell book,',
          '“I accidentally changed myself into a dog,” he said.']),
        ('INFERENCE', 'At the end, Annie says their adventures with Teddy were “Like living in Dreamtime,” and Jack agrees. What does she mean?',
         {'A': 'Their adventures felt magical and full of mystery, like the old stories of Dreamtime.',
          'B': 'They slept through all four adventures and only dreamed about them.',
          'C': 'Their adventures were quiet and boring, like lying in bed at night.',
          'D': 'They want to move to Australia and live there forever.'}, 'A',
         ['“Like living in Dreamtime,” said Annie.',
          'That was exactly what it was like.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to Australia, care for a baby kangaroo and escape a wildfire, receive a bark painting of the Rainbow Serpent as the fourth gift, and break the spell so Teddy turns back into a boy.',
          'B': 'Jack and Annie travel to a forest in India, escape a python and a tiger, free a trapped tiger, and receive a lotus flower as the third gift to help free Teddy.',
          'C': 'Jack and Annie travel to the Great Plains, live with the Lakota Indians, and receive an eagle’s feather as the second gift to help free Teddy.',
          'D': 'Jack and Annie travel to Australia, catch a sleepy koala for Morgan’s library, and decide to keep Teddy as their own pet dog in Frog Creek.'}, 'A',
         ['You helped break the spell.',
          '“Meet my young helper from Camelot,” said Morgan.']),
    ],
}

BOOK_TITLE = 'Dingoes at Dinnertime'
BOOK_TITLE_CN = '澳洲大火'
CHAPTER_TITLES = ['The Last Gift', 'Sleepyhead', 'Big Foot', 'Joey', 'Wildfire',
                  'Hand to Hand', 'Rain, Rain, Rain', 'The Rainbow Serpent', 'What Boy?', 'Dreamtime']


def chapter_text(chapter_index):
    """Rebuild Book 20 chapter text exactly as rebuild_docx_book does."""
    text = bt.chapter_text(chapter_index)
    for old, new in rb.FIXES.get(chapter_index, []):
        if old in text:
            text = text.replace(old, new)
    return rdb._cleanup(text).strip()


def build_book():
    texts = {c: chapter_text(c - 1) for c in range(1, 11)}
    chapters, problems = [], []
    for chapter_number in range(1, 11):
        norm_text = re.sub(r'[“”"\']', '', texts[chapter_number])
        questions = []
        for question_number, (tag, stem, options, answer, evidence) in enumerate(CH[chapter_number], start=1):
            standard, skill, dok, difficulty = META[tag]
            for piece in evidence:
                if re.sub(r'[“”"\']', '', piece) not in norm_text:
                    problems.append(f'ch{chapter_number} Q{question_number}: evidence not found: {piece!r}')
            # Source declarations keep the correct choice first for easy review.
            # Rotate it deterministically in the emitted quiz so learners cannot
            # infer the answer position; distribute A/B/C/D evenly across Book 20.
            labels = 'ABCD'
            correct_text = options[answer]
            distractors = [options[label] for label in labels if label != answer]
            emitted_answer = ANSWER_PATTERNS[chapter_number - 1][question_number - 1]
            emitted_options, distractor_index = {}, 0
            for label in labels:
                if label == emitted_answer:
                    emitted_options[label] = correct_text
                else:
                    emitted_options[label] = distractors[distractor_index]
                    distractor_index += 1
            questions.append({
                'number': question_number, 'standard': standard, 'skill': skill, 'dok': dok,
                'stem': stem, 'options': emitted_options, 'answer': emitted_answer, 'evidence': evidence,
                'rationale': rationale_for(tag, correct_text),
                'id': f'B20C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 20, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 20, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 20] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 20 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
