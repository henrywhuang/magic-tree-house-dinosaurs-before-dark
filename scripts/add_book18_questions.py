#!/usr/bin/env python3
"""Author and append the Book 18 (Buffalo Before Breakfast) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-16.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 18 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book18_text + rebuild_book18
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book18_text as bt
import rebuild_book18 as rb
import rebuild_docx_book as rdb

TARGET = ROOT / 'data' / 'questions.json'

# Balanced, non-repeating answer positions (one five-question row per chapter).
# Totals across the book: A 13, B 13, C 12, D 12.
ANSWER_PATTERNS = ('CABDB', 'DBCAC', 'BDACD', 'ACDBA', 'DCBAB',
                   'BADCA', 'CDABD', 'ABCDC', 'DACBA', 'BCADB')

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
        ('VOCABULARY IN CONTEXT', 'Morgan’s note says, “This little dog is under a spell and needs your help.” Here a “spell” is ___.',
         {'A': '魔咒；魔法咒语', 'B': '拼写；拼单词', 'C': '一段时间', 'D': '一种疾病'}, 'A',
         ['This little dog is under a spell and needs your help.']),
        ('DETAIL', 'What is the title of the book Jack picks up in the corner of the tree house?',
         {'A': 'The Great Plains.', 'B': 'The Titanic Disaster.',
          'C': 'Mountain Men of America.', 'D': 'The Blue Prairie Sky.'}, 'A',
         ['The title was The Great Plains.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Morgan’s note, what must happen to free Teddy from the spell?',
         {'A': 'Jack and Annie must be given four special things.',
          'B': 'Jack and Annie must find Morgan in the woods.',
          'C': 'Teddy must spend a night alone in the tree house.',
          'D': 'Jack and Annie must read four books about dogs.'}, 'A',
         ['To free him, you must be given four special things:']),
        ('INFERENCE', 'Annie says they already have “the gift from a ship lost at sea.” Which object is she talking about?',
         {'A': 'The silver pocket watch on the tree house floor.',
          'B': 'The book with a wide prairie on its cover.',
          'C': 'The notebook and pencil in Jack’s backpack.',
          'D': 'The rope ladder hanging from the oak tree.'}, 'A',
         ['We’ve got the first special thing,” said Annie, “the gift from a ship lost at sea.',
          'He picked up the silver pocket watch.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Jack looks out his bedroom window and sees Teddy.',
          'B': 'Annie reads Morgan’s note aloud in the tree house.',
          'C': 'Jack finds a book called The Great Plains.',
          'D': 'Jack and Annie follow Teddy into the Frog Creek woods.'}, 'A',
         ['Then he looked out his bedroom window.', 'A small dog stood in the early sunlight.']),
    ],
    2: [
        ('DETAIL', 'What did Jack’s backpack magically turn into?',
         {'A': 'A leather bag.', 'B': 'A woven straw basket.',
          'C': 'A small wooden box.', 'D': 'A cloth sack.'}, 'A',
         ['Jack’s backpack was now a leather bag.']),
        ('INFERENCE', 'When Jack says they need “a gift from the prairie blue,” what does Annie think “the prairie blue” means?',
         {'A': 'The sky above the prairie.',
          'B': 'A blue river on the plains.',
          'C': 'A blue flower in the grass.',
          'D': 'A blue stone hidden in the grass.'}, 'A',
         ['I bet that means the sky,” said Annie, looking up.']),
        ('VOCABULARY IN CONTEXT', 'The tree house sat in a lone tree in a “vast” golden prairie. Here “vast” means ___.',
         {'A': '广阔的；巨大的', 'B': '狭小的', 'C': '干枯的', 'D': '危险的'}, 'A',
         ['The tree house sat in a lone tree in a vast golden prairie.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do some people call the Great Plains “an ocean of grass”?',
         {'A': 'The grass rolls in waves as far as the eye can see.',
          'B': 'The plains are flooded with water every spring.',
          'C': 'Sea animals once lived in the tall grass.',
          'D': 'The grass is blue-green like the sea.'}, 'A',
         ['Some called it “an ocean of grass.”', 'All he could see was rolling waves of grass.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie land in a lone tree on a vast prairie, learn they need a gift from the prairie blue, and walk through tall grass until they see something great.',
          'B': 'Jack and Annie land beside a wide river, build a small raft, and float across the plains all day long to look for Morgan.',
          'C': 'Jack and Annie land on a high mountain, meet a real mountain man, and trade their coonskin caps for a blue stone.',
          'D': 'Jack and Annie land in a thick forest, lose Teddy among the trees, and spend the whole day searching for him.'}, 'A',
         ['We need a gift from the prairie blue,” said Jack.', 'Wow, that is great,” he whispered.']),
    ],
    3: [
        ('DETAIL', 'According to the research book, which was the largest tribe on the Great Plains in the early 1800s?',
         {'A': 'The Lakota.', 'B': 'The Cherokee.', 'C': 'The Apache.', 'D': 'The Navajo.'}, 'A',
         ['The Lakota were the largest tribe.']),
        ('VOCABULARY IN CONTEXT', 'Jack sees the rider has “a bow and a quiver of arrows on his back.” Here a “quiver” is ___.',
         {'A': '箭筒；箭袋', 'B': '颤抖；发抖', 'C': '弓弦', 'D': '马鞍'}, 'A',
         ['Jack could only see the outline of a body with a bow and a quiver of arrows on his back.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie meet Black Hawk, a Lakota boy they first mistook for a warrior, read about Lakota manners, and greet his people with the sign for “friend.”',
          'B': 'Jack and Annie hide in the grass from Lakota warriors all day, then sneak back to the tree house before anyone in the camp can see them.',
          'C': 'Jack and Annie meet Black Hawk’s parents, who invite them into the camp and teach them how to hunt buffalo with bows and arrows.',
          'D': 'Jack and Annie are chased across the plains by soldiers until a grown-up Lakota warrior on a pony rides up and rescues them.'}, 'A',
         ['Now Jack saw that he was only a boy on a pony.', 'Jack quickly held up two fingers. Annie did the same.']),
        ('INFERENCE', 'Black Hawk “didn’t smile back. But he did lower his bow.” This suggests that Black Hawk ___.',
         {'A': 'was still careful but no longer saw them as a threat',
          'B': 'was angry and wanted them to leave right away',
          'C': 'was planning to hunt them with his arrows',
          'D': 'could not understand anything Annie said'}, 'A',
         ['The boy didn’t smile back. But he did lower his bow while he stared at Annie.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack flip through the research book before following Annie to the camp?',
         {'A': 'He wants information about how to act with the Lakota.',
          'B': 'He wants to find a map that shows the way home.',
          'C': 'He wants to look up what kind of pony Black Hawk rides.',
          'D': 'He wants to learn how to shoot a bow and arrow.'}, 'A',
         ['He wanted information about how to act with the Lakota.']),
    ],
    4: [
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack straighten his shoulders and lift his chin as he walks through the camp?',
         {'A': 'He is trying to appear brave, just as Annie does.',
          'B': 'He is trying to see over the tops of the tepees.',
          'C': 'He is stretching after the long walk through the grass.',
          'D': 'He is looking up at the smoke rising from a tepee.'}, 'A',
         ['Jack wondered how to appear brave.', 'Jack straightened his shoulders. He lifted his chin, and he felt braver.']),
        ('VOCABULARY IN CONTEXT', '“The pony headed for the grazing pasture.” A “pasture” is ___.',
         {'A': '牧场；放牧的草地', 'B': '马厩', 'C': '小河', 'D': '帐篷'}, 'A',
         ['The pony headed for the grazing pasture.']),
        ('DETAIL', 'What does Jack give to Grandmother as a gift?',
         {'A': 'His coonskin cap.', 'B': 'His notebook.', 'C': 'His leather bag.', 'D': 'His pencil.'}, 'A',
         ['Then Jack took off his coonskin cap. He gave it to Grandmother.']),
        ('PLOT RELATION', 'Grandmother’s words remind Annie of the seal hunter in the Arctic. How are the Lakota and the seal hunter alike?',
         {'A': 'Both use all the gifts from the animal’s body and waste nothing.',
          'B': 'Both live in round houses made of snow and ice.',
          'C': 'Both hunt only at night while the animals are asleep.',
          'D': 'Both keep the animals as pets instead of hunting them.'}, 'A',
         ['The buffalo gives our people many gifts,” said the old woman.',
          'He used all the gifts from the seal’s body. He didn’t waste a thing.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A huge wolf comes out of Grandmother’s tepee.',
          'B': 'Grandmother puts Jack’s cap on her head and laughs.',
          'C': 'Grandmother explains why a girl sews on bear claws.',
          'D': 'Jack lists the gifts the buffalo gives the Lakota.'}, 'A',
         ['Coming out of Grandmother’s tepee was a huge wolf!']),
    ],
    5: [
        ('VOCABULARY IN CONTEXT', 'The “fierce wolf” was really Black Hawk “wearing a wolf’s hide.” Here “hide” means ___.',
         {'A': '（动物的）兽皮', 'B': '躲藏；藏起来', 'C': '面具', 'D': '帽子'}, 'A',
         ['The fierce wolf was Black Hawk wearing a wolf’s hide!']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Grandmother let Black Hawk only show the buffalo, not hunt them?',
         {'A': 'They have enough meat, and the Lakota never take more buffalo than they need.',
          'B': 'Black Hawk is still too young to ride a pony anywhere near the buffalo herd.',
          'C': 'The buffalo herd has wandered much too far away from the camp today.',
          'D': 'Visitors like Jack and Annie are never allowed to watch a buffalo hunt.'}, 'A',
         ['Do not hunt. We have enough meat today.', 'Lakota never take more buffalo than we need,” she said.']),
        ('DETAIL', 'How does Annie say they can ride the ponies without saddles or reins?',
         {'A': 'Hold on to the ponies’ manes and grip with their legs.',
          'B': 'Tie ropes around the ponies’ necks to steer them.',
          'C': 'Sit behind Black Hawk and hold on to his shoulders.',
          'D': 'Walk beside the ponies and lead them by their tails.'}, 'A',
         ['Just hold on to their manes,', 'and grip with your legs.']),
        ('INFERENCE', 'Jack lets out a wild whoop after he sees Grandmother watching him. Why?',
         {'A': 'He remembers that the Lakota admire people who do not show fear, and he wants her to admire him.',
          'B': 'He is scared of the pony and is calling out loudly for Annie to come back and help him.',
          'C': 'He wants Grandmother to come over and take the pony away before it starts to run.',
          'D': 'He is trying to frighten the buffalo herd so that it will run far away from the camp.'}, 'A',
         ['Lakota people admire those who do not show fear, Jack remembered.',
          'He liked Grandmother. He wanted her to admire him.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'The “wolf” turns out to be Black Hawk in a wolf skin, Grandmother lets him show the buffalo but not hunt, and the children ride ponies to a huge herd.',
          'B': 'A real wolf chases Teddy out of the camp, and Black Hawk hunts it with his bow while Jack and Annie hide inside the tepee.',
          'C': 'Grandmother teaches Jack and Annie how to sew wolf skins, and they spend the whole afternoon working quietly inside the tepee.',
          'D': 'Jack falls off his pony, so Annie and Black Hawk ride off to see the buffalo while Jack waits alone back at the camp.'}, 'A',
         ['May I show them the buffalo now?” he said.', 'Before them were thousands and thousands of grazing buffalo.']),
    ],
    6: [
        ('DETAIL', 'According to the research book, how many bison were on the Great Plains at the beginning of the 1800s?',
         {'A': '40 million.', 'B': 'Less than 300.', 'C': '2 thousand.', 'D': '6 million.'}, 'A',
         ['At the beginning of the 1800s, there were 40 million bison on the Great Plains.']),
        ('INFERENCE', 'Looking at the huge herd, Jack “knew for certain” what time they had come to. What did he figure out?',
         {'A': 'They had come before the white settlers arrived and before the great herds ended.',
          'B': 'They had come after almost all of the buffalo had been killed by hunters.',
          'C': 'They had come to the very same year that the Titanic sank in the ocean.',
          'D': 'They had come to a time when the Lakota no longer lived on the plains.'}, 'A',
         ['As far as he could see, there was nothing but buffalo.',
          'Now Jack knew for certain they’d come to the time before the white settlers and soldiers had arrived, before the end of the great buffalo herds.']),
        ('VOCABULARY IN CONTEXT', 'The book warns that one alarmed buffalo might “set off a terrifying stampede.” A “stampede” is ___.',
         {'A': '（兽群）受惊狂奔', 'B': '一场暴风雨', 'C': '一次狩猎比赛', 'D': '一片草原'}, 'A',
         ['If one becomes alarmed by a hunter, he might start running and set off a terrifying stampede.']),
        ('CAUSE / PURPOSE / RESULT', 'What makes the huge buffalo charge at Black Hawk?',
         {'A': 'Black Hawk sneezes loudly right beside it.',
          'B': 'Teddy runs up and bites its back legs.',
          'C': 'Jack shouts “Come back!” from the slope.',
          'D': 'Black Hawk shoots an arrow toward it.'}, 'A',
         ['Ah-ah-CHOO!” Black Hawk sneezed.', 'The huge buffalo jerked its head up.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'All the buffalo stop running and begin grazing again.',
          'B': 'Teddy jumps out of Annie’s arms and runs toward the herd.',
          'C': 'Jack rides Sunlight down the slope to rescue Black Hawk.',
          'D': 'Black Hawk creeps on all fours toward the buffalo.'}, 'A',
         ['They began grazing again as if nothing had happened.']),
    ],
    7: [
        ('PLOT RELATION', 'Black Hawk and Jack explain Annie’s success with the buffalo in different ways. Which choice shows the difference?',
         {'A': 'Black Hawk says she has good medicine; Jack says she just has a way with animals.',
          'B': 'Black Hawk says she was only lucky; Jack says the buffalo were too tired to run.',
          'C': 'Black Hawk says Teddy scared the buffalo; Jack says the ponies calmed them down.',
          'D': 'Black Hawk says she used a magic spell; Jack says she read it in Morgan’s book.'}, 'A',
         ['She has good medicine,” said Black Hawk.', 'She just has a way with animals.']),
        ('VOCABULARY IN CONTEXT', '“On her face was a look of amazement.” Here “amazement” means ___.',
         {'A': '惊奇；惊讶', 'B': '愤怒；生气', 'C': '疲倦；劳累', 'D': '伤心；难过'}, 'A',
         ['On her face was a look of amazement.']),
        ('DETAIL', 'What was the beautiful lady who helped Annie wearing?',
         {'A': 'A white leather dress.', 'B': 'A fringed buckskin dress.',
          'C': 'A blue feathered robe.', 'D': 'A gray wolf-skin cape.'}, 'A',
         ['Then, out of nowhere, a beautiful lady in a white leather dress came to help me.']),
        ('INFERENCE', 'When Annie mentions the lady in white, Black Hawk’s “eyes had grown wide.” This suggests that Black Hawk ___.',
         {'A': 'understands that something very special and sacred has happened',
          'B': 'thinks Annie is making up a silly story to impress him',
          'C': 'is angry that Annie ran so close to the buffalo herd',
          'D': 'is worried that the buffalo will start running again'}, 'A',
         ['You saw a lady in white?” asked Black Hawk. His eyes had grown wide.',
          'That lady does not live on this earth,” Black Hawk said softly.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Annie tells how a lady in white helped stop the buffalo, Teddy returns, and Black Hawk says she saw White Buffalo Woman, so they ride back to tell Grandmother.',
          'B': 'Annie gets lost among the buffalo, Black Hawk finds her by following Teddy’s barking, and they all decide to hunt one buffalo for Grandmother.',
          'C': 'A lady in white rides into the Lakota camp, gives Annie a pony of her own, and tells the children it is time to go home to Frog Creek.',
          'D': 'Jack chases Teddy far across the plains, finds a white buffalo calf hiding in the grass, and brings it back to Black Hawk’s camp.'}, 'A',
         ['You saw the spirit of White Buffalo Woman,” he said.', 'We must tell Grandmother.']),
    ],
    8: [
        ('VOCABULARY IN CONTEXT', '“Let this be a lesson to you,” Grandmother said “sternly.” Here “sternly” means ___.',
         {'A': '严厉地', 'B': '温柔地', 'C': '开心地', 'D': '小声地'}, 'A',
         ['Let this be a lesson to you,” Grandmother said sternly.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Grandmother, how did Black Hawk’s pride lead to the stampede?',
         {'A': 'Pride made him show off, his foolishness frightened one buffalo, and that buffalo frightened the others.',
          'B': 'Pride made him forget his wolf suit, so the buffalo could easily see that he was only a boy.',
          'C': 'Pride made him ride his pony too fast, and its pounding hooves woke the whole sleeping herd.',
          'D': 'Pride made him shout at Jack and Annie, and their loud voices scared every buffalo nearby.'}, 'A',
         ['Your pride led you to show off.', 'Your foolishness frightened a buffalo. He frightened others.']),
        ('INFERENCE', 'Grandmother calls the children “Buffalo Girl” and “Rides-Like-Wind” and welcomes them to the family. This shows that she ___.',
         {'A': 'honors the courage they showed that day',
          'B': 'is still angry that they went to the buffalo',
          'C': 'has forgotten what their real names are',
          'D': 'wants them to stay and hunt with Black Hawk'}, 'A',
         ['Buffalo Girl and Rides-Like-Wind showed great courage today,” she said.',
          'We welcome you to our family,” said Grandmother.']),
        ('DETAIL', 'What gift does Grandmother give Jack and Annie, and why?',
         {'A': 'An eagle’s feather, for their courage.',
          'B': 'A buffalo robe, for the cold night.',
          'C': 'A beaded moccasin, for their journey.',
          'D': 'A sacred pipe, for their prayers.'}, 'A',
         ['This is a gift for you,” she said. “An eagle’s feather for your courage.']),
        ('PLOT RELATION', 'According to Grandmother, how is White Buffalo Woman connected to the Great Spirit?',
         {'A': 'She is his messenger, who brought the sacred pipe so prayers could rise to him.',
          'B': 'She is his daughter, who rules over all the wolves that live on the plains.',
          'C': 'She is his enemy, who once tried to drive all the buffalo off the plains.',
          'D': 'She is his helper, who teaches Lakota children how to ride their ponies.'}, 'A',
         ['She is a messenger of the Great Spirit,” said Grandmother.',
          'She brought the sacred pipe so that our prayers could rise to the Great Spirit.']),
    ],
    9: [
        ('DETAIL', 'How do the Lakota carry their tepees when they move camp?',
         {'A': 'On wooden platforms strapped to two poles and pulled by horses.',
          'B': 'In big rawhide bags carried on the people’s own backs.',
          'C': 'In wooden wagons with wheels that are pulled by buffalo.',
          'D': 'Rolled up tightly and floated down the river on rafts.'}, 'A',
         ['They were loading them onto wooden platforms strapped to two poles. The poles were pulled by horses.']),
        ('INFERENCE', 'Black Hawk says, “There is not only one place to learn.” What does he mean?',
         {'A': 'Lakota children learn everywhere—in camp, on the plains, and from the sky.',
          'B': 'Lakota children go to a different school building every few weeks.',
          'C': 'Lakota children do not need to learn anything new at all.',
          'D': 'Lakota children only learn things from books like Jack’s.'}, 'A',
         ['There is not only one place to learn,” he said.',
          'In camp we learn to make clothes, tools, and tepees. On the plains we learn to ride and hunt.']),
        ('VOCABULARY IN CONTEXT', 'Jack says sadly, “The buffalo will vanish.” Here to “vanish” means to ___.',
         {'A': '消失；不复存在', 'B': '变多；增加', 'C': '迁徙；搬家', 'D': '生病；受伤'}, 'A',
         ['The buffalo will vanish. The old way of life for the Lakota will vanish, too.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack feel better after he talks sadly about the changes to come?',
         {'A': 'Annie says the Great Spirit will never vanish and will always take care of Black Hawk’s people.',
          'B': 'Annie says the buffalo herds on the plains will grow bigger and bigger every single year.',
          'C': 'Grandmother promises that the Lakota will never have to move their camp ever again.',
          'D': 'Black Hawk promises that he will come to visit Jack and Annie in Frog Creek very soon.'}, 'A',
         ['But the Great Spirit won’t ever vanish,” said Annie. “It will always take care of Black Hawk’s people.',
          'Jack smiled. Annie’s words made him feel better.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'The Lakota pack up to follow the buffalo, Jack learns about the Lakota way of life and learning, and the children say good-bye and wish themselves home.',
          'B': 'The Lakota hold a great buffalo hunt at dawn, and Jack and Annie stay behind in the camp with Grandmother to help pound the meat.',
          'C': 'Black Hawk walks with Jack and Annie to the tree house and asks if he can come to school with them back in Frog Creek.',
          'D': 'Jack and Annie decide to walk west with the Lakota, but Teddy runs away and they spend the whole day looking for him.'}, 'A',
         ['It is time to follow the buffalo,” said Grandmother.', 'I wish we could go home to our people,” he said.']),
    ],
    10: [
        ('VOCABULARY IN CONTEXT', '“Bright sunlight flooded the tree house.” Here “flooded” means ___.',
         {'A': '（光线）充满；涌进', 'B': '被水淹没', 'C': '慢慢变暗', 'D': '轻轻摇晃'}, 'A',
         ['Bright sunlight flooded the tree house.']),
        ('DETAIL', 'Where does Annie put the eagle’s feather?',
         {'A': 'On Morgan’s note, next to the silver pocket watch.',
          'B': 'In Jack’s notebook, between two blank pages.',
          'C': 'In her own hair, the way a Lakota girl might.',
          'D': 'On the windowsill, facing the Frog Creek woods.'}, 'A',
         ['She put it on Morgan’s note, next to the silver pocket watch from the Titanic.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie think Teddy had something to do with White Buffalo Woman?',
         {'A': 'Teddy disappeared just as she appeared, and came back just as she disappeared.',
          'B': 'Teddy barked at the lady and then followed her far across the prairie.',
          'C': 'Teddy was carrying a white feather in his mouth when he came back.',
          'D': 'Teddy led Annie straight to the lady and then stopped the buffalo himself.'}, 'A',
         ['One second Teddy disappeared in the grass. Then White Buffalo Woman appeared,” said Annie.',
          'When White Buffalo Woman disappeared, Teddy appeared.']),
        ('INFERENCE', 'Jack says, “maybe Teddy has good medicine,” and Annie answers, “Now you understand.” This shows that Jack ___.',
         {'A': 'has begun to believe Teddy may have a special, magical power',
          'B': 'thinks Teddy is sick and needs to take some medicine',
          'C': 'still believes Annie is just making the whole thing up',
          'D': 'wants to take Teddy back to Black Hawk and Grandmother'}, 'A',
         ['maybe Teddy has good medicine.', 'Now you understand,” said Annie, smiling.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to the Great Plains, are welcomed by Black Hawk and his Lakota grandmother, survive a stampede with help from White Buffalo Woman, and bring home an eagle’s feather to help free Teddy.',
          'B': 'Jack and Annie sail on the Titanic, rescue a small dog from the sinking ship, and bring home a silver pocket watch for Morgan.',
          'C': 'Jack and Annie become mountain men in the Rocky Mountains and hunt buffalo all summer long to earn a gift for Morgan.',
          'D': 'Jack and Annie visit a Lakota school building, learn to read the old books there, and bring home a sacred pipe for Teddy.'}, 'A',
         ['Now we have our gift from the prairie blue,” said Jack.',
          'Now we have the second thing to help free you from your spell.']),
    ],
}

BOOK_TITLE = 'Buffalo Before Breakfast'
BOOK_TITLE_CN = '野牛之地'
CHAPTER_TITLES = ["Teddy's Back!", 'Ocean of Grass', 'Black Hawk', 'Good Manners', 'Sunlight and Midnight',
                  'Stampede!', 'White Buffalo Woman', 'Sacred Circle', 'Lakota School', 'Good Medicine']


def chapter_text(chapter_index):
    """Rebuild Book 18 chapter text exactly as rebuild_docx_book does."""
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
            # infer the answer position; distribute A/B/C/D evenly across Book 18.
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
                'id': f'B18C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 18, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 18, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 18] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 18 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
