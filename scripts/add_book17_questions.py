#!/usr/bin/env python3
"""Author and append the Book 17 (Tonight on the Titanic) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-16.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 17 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book17_text + rebuild_book17
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book17_text as bt
import rebuild_book17 as rb
import rebuild_docx_book as rdb

TARGET = ROOT / 'data' / 'questions.json'

# Balanced, non-repeating answer positions (one five-question row per chapter).
# Totals across the book: A=13, B=13, C=12, D=12.
ANSWER_PATTERNS = ('CADBA', 'BDCAC', 'DBACB', 'DACBD', 'BCADA',
                   'CDBAB', 'ABDCD', 'DCBAC', 'BADCA', 'CBADB')

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
        ('DETAIL', 'What did Annie say the rain was telling them?',
         {'A': 'Come now!', 'B': 'Stay inside!', 'C': 'Go back to bed!', 'D': 'Watch out!'}, 'A',
         ['It’s saying, Come now!']),
        ('VOCABULARY IN CONTEXT', 'Morgan’s note says, “This little dog is under a spell.” Here a “spell” is ___.',
         {'A': '魔咒；咒语', 'B': '拼写（单词）', 'C': '一段时间', 'D': '一场重病'}, 'A',
         ['This little dog is under a spell and needs your help.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Morgan’s note, what must happen to free the little dog?',
         {'A': 'Jack and Annie must be given four special gifts from four different places.',
          'B': 'Jack and Annie must find Morgan and bring her back to the tree house.',
          'C': 'Jack and Annie must show their Master Librarian cards to the dog.',
          'D': 'Jack and Annie must read four books aloud to the dog in one night.'}, 'A',
         ['To free him, you must be given four special things']),
        ('INFERENCE', 'When Jack sees that the book is called The Unsinkable Ship, he says, “Well, at least that’s good.” What does Jack think?',
         {'A': 'A ship that cannot sink should be a safe place to visit.',
          'B': 'The ship in the book has already sunk to the bottom.',
          'C': 'The book will be too boring to read on the trip.',
          'D': 'Teddy has chosen the wrong book for their mission.'}, 'A',
         ['The title of the book was The Unsinkable Ship.', 'The ship won’t sink, even if it is lost.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Teddy pushes a book with his nose to choose their first trip.',
          'B': 'Jack and Annie find a small, sad dog in the tree house.',
          'C': 'Annie tells Jack that the rain is saying, “Come now!”',
          'D': 'Jack picks up Morgan’s note from the tree house floor.'}, 'A',
         ['Teddy trotted over to a book.', 'He pushed it with his nose.']),
    ],
    2: [
        ('DETAIL', 'According to the research book, what was the ocean liner doing late at night on April 14, 1912?',
         {'A': 'Making her first voyage across the Atlantic Ocean to New York City.',
          'B': 'Sailing home to England after many trips around the world.',
          'C': 'Carrying soldiers across the Pacific Ocean to a faraway war.',
          'D': 'Waiting in a harbor for the stormy weather to end.'}, 'A',
         ['Late at night, on April 14, 1912, an English ocean liner was making her first voyage across the Atlantic Ocean.',
          'She was going to New York City.']),
        ('VOCABULARY IN CONTEXT', 'Jack and Annie see “a huge iceberg looming out of the sea.” Here “looming” means ___.',
         {'A': '（巨大而吓人地）赫然出现', 'B': '慢慢地融化', 'C': '沉入海底', 'D': '漂向远方'}, 'A',
         ['a huge iceberg looming out of the sea']),
        ('INFERENCE', 'Jack tells Annie, “You have to wait until someone gives it to you.” What can you infer about how they will get the gift?',
         {'A': 'Someone they meet on the ship will have to give it to them.',
          'B': 'They will find it hidden somewhere inside the tree house.',
          'C': 'Teddy will sniff it out from under the wooden deck.',
          'D': 'Morgan will send it to them by magic right away.'}, 'A',
         ['You can’t go looking for a gift,” said Jack.', 'You have to wait until someone gives it to you.']),
        ('PLOT RELATION', 'After the ship scrapes past the iceberg, how are Annie’s and Jack’s reactions different?',
         {'A': 'Annie thinks it was just a little bump, but Jack is worried and wants to read more.',
          'B': 'Annie is terrified and wants to go home, but Jack calmly goes off to find the gift.',
          'C': 'Annie wants to read the book, but Jack wants to go out on the deck at once.',
          'D': 'Annie and Jack are both sure that the ship is going to sink right away.'}, 'A',
         ['It was just a little bump.', 'But Jack was worried.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Annie shines the flashlight on a life preserver hanging from the railing.',
          'B': 'A shout comes from the lookouts’ nest: “Iceberg ahead!”',
          'C': 'Jack reads that the ship was going to New York City.',
          'D': 'Annie notices that they are dressed like old-fashioned kids.'}, 'A',
         ['she shined the flashlight on a life preserver hanging from the railing.']),
    ],
    3: [
        ('VOCABULARY IN CONTEXT', '“An SOS is the international distress signal in Morse code.” Here “distress” means ___.',
         {'A': '危难；遇险', 'B': '庆祝；欢乐', 'C': '天气；风暴', 'D': '问候；致意'}, 'A',
         ['An SOS is the international distress signal in Morse code.']),
        ('DETAIL', 'According to Jack’s book, how many lifeboats did the Titanic have?',
         {'A': '20 lifeboats, but it needed twice as many to save everyone.',
          'B': '40 lifeboats, which was enough for every passenger.',
          'C': '10 lifeboats, all of them kept on the lower decks.',
          'D': '2 lifeboats, saved only for the captain and his crew.'}, 'A',
         ['On the Titanic, there were 20 lifeboats.', 'To save all the passengers, the ship needed twice as many.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why did no ship arrive in time to help the Titanic?',
         {'A': 'The only nearby ship had turned off its radio, and the others were too far away.',
          'B': 'The radio operator forgot to send out the SOS message.',
          'C': 'The captain told all of the other ships to stay away.',
          'D': 'A big storm kept every other ship inside its harbor.'}, 'A',
         ['Unfortunately, the only ship near the Titanic had turned off its radio for the night.',
          'All the other ships who received the message were too far away to help.']),
        ('PLOT RELATION', 'How does what Jack reads about the third-class passengers lead to Annie’s plan?',
         {'A': 'Many of them did not know where to go, so Annie decides they can help someone find the lifeboats.',
          'B': 'They were all safe already, so Annie decides that she and Jack should go home at once.',
          'C': 'They were sending the SOS, so Annie decides that they should help the radio operator.',
          'D': 'They had the gift for Teddy, so Annie decides that they should go and ask for it.'}, 'A',
         ['because they were on the lower decks and didn’t know where to go.',
          'We can help someone find the lifeboats,” she said.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie learn the Titanic is sinking, hear the captain order an SOS, and plan to guide people from the lower decks to the lifeboats.',
          'B': 'Jack and Annie decide there is nothing they can do, so they hurry back to the tree house and go home.',
          'C': 'Jack and Annie explore the ship’s library and gym, then fall asleep in an empty room on the top deck.',
          'D': 'Jack and Annie help the radio operator fix his machine so that other ships can rescue the Titanic in time.'}, 'A',
         ['Send the international call for help', 'We’ll start at the grand stairway,” said Jack.']),
    ],
    4: [
        ('DETAIL', 'What time did the fancy clock at the top of the grand stairway show?',
         {'A': '12:20, twenty minutes after midnight.',
          'B': '11:40, twenty minutes before midnight.',
          'C': '1:50, ten minutes before two o’clock.',
          'D': '2:20, twenty minutes after two o’clock.'}, 'A',
         ['The hands of the clock were at 12:20.']),
        ('VOCABULARY IN CONTEXT', 'Annie says, “The floor’s slanting down.” Here “slanting” means ___.',
         {'A': '倾斜', 'B': '发亮', 'C': '震动', 'D': '裂开'}, 'A',
         ['The floor’s slanting down.']),
        ('CAUSE / PURPOSE / RESULT', 'Why is the floor of the hallway slanting down?',
         {'A': 'The front of the ship is already sinking.',
          'B': 'The hallway was built on top of a hill.',
          'C': 'The carpet has slipped on the wet floor.',
          'D': 'The ship is turning sharply to the left.'}, 'A',
         ['That means the front of the ship is already sinking,” he said.']),
        ('INFERENCE', 'The man in the uniform calls it “a little accident,” and the people on the third-class deck are “all joking and laughing.” What can you infer?',
         {'A': 'Most passengers did not yet believe they were in real danger.',
          'B': 'The passengers knew the ship was sinking but were very brave.',
          'C': 'The ship had already stopped sinking by this time.',
          'D': 'The passengers were laughing at Teddy’s loud barking.'}, 'A',
         ['There’s been a little accident,” the man in the uniform said cheerfully.',
          'They were all joking and laughing.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Teddy barks at a closed door, and a very small boy peeks out.',
          'B': 'Annie shouts at the card players to go up to the boat deck.',
          'C': 'A man in a white uniform knocks on the stateroom doors.',
          'D': 'Jack and Annie see water sloshing at the end of a hallway.'}, 'A',
         ['The dog began barking at a closed door.', 'A very small boy peeked out.']),
    ],
    5: [
        ('DETAIL', 'How old did the little boy, William, look?',
         {'A': 'About four years old.', 'B': 'About twelve years old.',
          'C': 'About eight years old.', 'D': 'About two years old.'}, 'A',
         ['He looked about four years old.']),
        ('VOCABULARY IN CONTEXT', 'Annie shouts, “Come out! It’s an emergency!” An “emergency” is ___.',
         {'A': '紧急情况', 'B': '惊喜派对', 'C': '睡前故事', 'D': '好消息'}, 'A',
         ['It’s an emergency!']),
        ('PLOT RELATION', 'Who are Lucy and William, and why are they on the ship without their parents?',
         {'A': 'They are sister and brother traveling to meet their parents in New York.',
          'B': 'They are cousins whose parents are asleep in another cabin.',
          'C': 'They are the captain’s children, and their parents work on the ship.',
          'D': 'They are friends who ran away from their parents in England.'}, 'A',
         ['This is my brother, William.', 'Our parents aren’t here. They’re in New York,” she said.']),
        ('INFERENCE', 'Jack “didn’t feel any extra weight in his knapsack,” and Teddy “felt as light as air.” This suggests that ___.',
         {'A': 'Teddy is no ordinary dog and may have some magic',
          'B': 'Teddy has quietly fallen out of Jack’s knapsack',
          'C': 'Jack is so strong that nothing ever feels heavy',
          'D': 'Teddy is very sick and has not eaten for days'}, 'A',
         ['Jack didn’t feel any extra weight in his knapsack.', 'The little dog felt as light as air.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Teddy finds William and his sister Lucy; Jack and Annie warn them, help them into coats and life belts, and they all run as the sea water creeps in.',
          'B': 'Jack and Annie wake up William and Lucy, but the two children refuse to leave and go straight back to sleep.',
          'C': 'Lucy and William show Jack and Annie a secret way up to the lifeboats and lead them safely there.',
          'D': 'Jack and Annie find William’s parents and help the whole family reach the boat deck together.'}, 'A',
         ['Just get your coats and your life belts.', 'The green sea water was slowly moving down the hall.']),
    ],
    6: [
        ('VOCABULARY IN CONTEXT', '“With a hiss and rush of light, a rocket streaked into the sky.” Here “streaked” means ___.',
         {'A': '飞快地划过', 'B': '慢慢地飘落', 'C': '静静地停住', 'D': '左右摇晃'}, 'A',
         ['With a hiss and rush of light, a rocket streaked into the sky.']),
        ('DETAIL', 'What did one of the card players tell Annie when she yelled at them to go to the lifeboats?',
         {'A': 'Even if the ship did sink, it would take all night.',
          'B': 'All of the lifeboats had already left the ship.',
          'C': 'They would go as soon as their card game was over.',
          'D': 'The captain had told them to stay in the room.'}, 'A',
         ['even if this ship does sink, it will take all night']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Lucy think Jack and Annie have brought them to a party?',
         {'A': 'The deck is bright, a band plays lively music, and a rocket bursts into colored balls.',
          'B': 'People are dancing and singing in the third-class cabins down below.',
          'C': 'Annie promised her that there would be cake waiting on the top deck.',
          'D': 'The card players invite her and William to sit down and join their game.'}, 'A',
         ['A band played lively music.', 'You’ve brought us to a party.']),
        ('INFERENCE', 'Jack asks Lucy, “Don’t you remember the water downstairs?” Then “Lucy’s smile faded.” This shows that Lucy ___.',
         {'A': 'suddenly understands again that the danger is real',
          'B': 'is angry that Jack has spoiled her happy party',
          'C': 'has forgotten everything that happened below',
          'D': 'is too cold and sleepy to keep on smiling'}, 'A',
         ['Don’t you remember the water downstairs?', 'Lucy’s smile faded.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Someone shouts, “Women and children first!” and Annie pulls Lucy and William toward a lifeboat.',
          'B': 'The card players laugh at Annie and say there is plenty of time for everyone.',
          'C': 'A rocket booms in the sky and bursts into many colored balls above the deck.',
          'D': 'The cold sea water creeps up the stairs, step by step, behind the children.'}, 'A',
         ['Women and children first!” someone shouted.', 'She pulled Lucy and William toward a lifeboat.']),
    ],
    7: [
        ('DETAIL', 'What gift does Lucy give Jack and Annie?',
         {'A': 'Her father’s silver watch on a chain.',
          'B': 'Her mother’s gold ring in a box.',
          'C': 'William’s little toy boat made of wood.',
          'D': 'Her own warm coat and life belt.'}, 'A',
         ['She reached into her coat pocket and pulled out a silver watch on a chain.', 'It’s our father’s watch.']),
        ('VOCABULARY IN CONTEXT', 'Lucy says, “We carried it on the voyage for good luck.” A “voyage” is ___.',
         {'A': '（乘船的）航行；旅程', 'B': '口袋', 'C': '舞会', 'D': '船舱'}, 'A',
         ['We carried it on the voyage for good luck.']),
        ('CAUSE / PURPOSE / RESULT', 'Why did Lucy want to stay on the Titanic instead of getting into the lifeboat at first?',
         {'A': 'The brightly lit ship seemed solid and safe compared to the tiny lifeboat.',
          'B': 'She wanted to wait on the ship until her parents came to find her.',
          'C': 'She had left her father’s watch behind in their cabin downstairs.',
          'D': 'The man in the uniform told her there was no room for her.'}, 'A',
         ['I’d rather stay here,” she said to Jack and Annie.',
          'The brightly lit Titanic seemed so solid and safe compared to the little lifeboat.']),
        ('PLOT RELATION', 'Why does Lucy decide to give her father’s watch to Jack and Annie?',
         {'A': 'She feels that Jack and Annie were her family’s good luck that night.',
          'B': 'She wants them to tell her parents what time the ship sank.',
          'C': 'She thinks the watch is broken and is no longer useful.',
          'D': 'Annie asked her for a gift to free Teddy from his spell.'}, 'A',
         ['I have a feeling that the two of you were our good luck tonight.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Lucy is afraid to leave the bright ship, but she bravely boards the lifeboat with William after giving Jack and Annie her father’s watch; then a man tosses Annie in, too.',
          'B': 'Lucy and William refuse to get into the lifeboat, so Jack and Annie take them back to the tree house to keep them safe from the sinking ship.',
          'C': 'Jack and Annie climb into the lifeboat with Lucy and William, and the four children row away together from the sinking ship.',
          'D': 'Lucy loses her father’s watch on the deck, and Jack and Annie search everywhere until they find it and give it back to her.'}, 'A',
         ['This is a gift for both of you,” she said.', 'And he tossed Annie into the lifeboat.']),
    ],
    8: [
        ('DETAIL', 'When Jack and Annie looked at the watch after Lucy’s lifeboat floated away, what did they find?',
         {'A': 'It was 2:05, and they had only fifteen minutes left.',
          'B': 'It was 1:50, and they had thirty minutes left.',
          'C': 'It was 12:20, and they had two hours left.',
          'D': 'It was 2:20, and the ship had already sunk.'}, 'A',
         ['The time was 2:05.', 'Only fifteen minutes left!” said Annie.']),
        ('VOCABULARY IN CONTEXT', '“But the crowd started to panic.” To “panic” means to ___.',
         {'A': '惊慌失措', 'B': '安静下来', 'C': '唱起歌来', 'D': '排好队伍'}, 'A',
         ['But the crowd started to panic.']),
        ('CAUSE / PURPOSE / RESULT', 'Why was the lifeboat with Annie in it brought back up to the ship?',
         {'A': 'Lady Blackwell, a woman in a fur coat, shouted for it to wait for her.',
          'B': 'Jack told the uniformed man that Annie was his little sister.',
          'C': 'The lifeboat was already much too full to go all the way down.',
          'D': 'One of the cables broke while the boat was being lowered.'}, 'A',
         ['A woman in a fur coat appeared at the railing.', 'Bring the boat back up for Lady Blackwell!']),
        ('INFERENCE', 'The captain shouts, “It’s every man for himself!” What does this order tell the crew?',
         {'A': 'They can stop their jobs and try to save their own lives.',
          'B': 'Each man must help one passenger into a lifeboat.',
          'C': 'Every man must stay at his post until the very end.',
          'D': 'The men should go below and try to fix the ship.'}, 'A',
         ['It’s every man for himself!” the captain shouted to all of his crew.',
          'The men all stopped what they were doing and ran up the deck.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack and Annie reach the smokestacks and find that the tree house is gone.',
          'B': 'Jack pulls Annie out of the lifeboat and back onto the sinking ship.',
          'C': 'Lucy and William’s little lifeboat floats off into the darkness.',
          'D': 'The band plays a slow, calm song that sounds like a church hymn.'}, 'A',
         ['The magic tree house was gone!']),
    ],
    9: [
        ('VOCABULARY IN CONTEXT', '“There was more frantic barking.” Here “frantic” means ___.',
         {'A': '急切而疯狂的', 'B': '轻柔的', 'C': '开心的', 'D': '断断续续的'}, 'A',
         ['There was more frantic barking.']),
        ('DETAIL', 'Where did Jack finally see the tree house in the dark?',
         {'A': 'Stuck between a smokestack and the railing, lying on its side.',
          'B': 'Floating in the black ocean right next to a lifeboat.',
          'C': 'Sitting high on top of the lookouts’ nest at the front.',
          'D': 'Hidden under the grand clock at the top of the stairs.'}, 'A',
         ['It was stuck between a smokestack and the railing.', 'It was lying on its side.']),
        ('CAUSE / PURPOSE / RESULT', 'How did Annie find the tree house?',
         {'A': 'Teddy’s barking led her to it.',
          'B': 'She saw its light shining in the dark.',
          'C': 'Jack read where it was in the book.',
          'D': 'A sailor pointed the way for her.'}, 'A',
         ['Teddy’s barking led me here!” cried Annie.']),
        ('INFERENCE', 'Jack “closed his eyes, waiting to be washed away.” This shows that at that moment Jack ___.',
         {'A': 'had almost given up hope of escaping',
          'B': 'was falling asleep because he was so tired',
          'C': 'was sure that Teddy would come to save him',
          'D': 'thought the water would soon go back down'}, 'A',
         ['Maybe the tree house fell into the ocean!” shouted Jack.',
          'He closed his eyes, waiting to be washed away.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'With the tree house missing and the ship tipping, Teddy vanishes from Jack’s knapsack; his barking leads Annie to the tree house, and she pulls Jack in before they wish to go home.',
          'B': 'Jack and Annie give up looking for the tree house, so they jump into the ocean and swim over to Lucy and William’s lifeboat.',
          'C': 'Teddy falls overboard into the sea, and Jack and Annie climb down into a lifeboat to search the dark water for him.',
          'D': 'The lights go out, so Jack and Annie wait quietly on the grand staircase until the ship finally stops sinking.'}, 'A',
         ['Teddy wasn’t there!', 'She pulled him into the tree house.']),
    ],
    10: [
        ('DETAIL', 'When Annie shines her flashlight on Lucy’s watch, what does she see?',
         {'A': 'The watch has stopped, and its hands are at 2:20.',
          'B': 'The watch is still ticking, and it says 2:05.',
          'C': 'The watch is running fast, and it says 1:50.',
          'D': 'The watch’s hands are spinning around and around.'}, 'A',
         ['The watch had stopped.', 'The hands were at 2:20.']),
        ('VOCABULARY IN CONTEXT', 'Jack says the Titanic is “a true story, but it’s also like a myth now.” A “myth” is ___.',
         {'A': '神话；传说', 'B': '谜语', 'C': '新闻报道', 'D': '日记'}, 'A',
         ['It’s a true story, but it’s also like a myth now.']),
        ('INFERENCE', 'Why does Annie say that 2:20 is “when time stopped for the Titanic”?',
         {'A': 'The watch stopped at the very moment the ship went down, when the Titanic’s story ended.',
          'B': 'All of the clocks on the Titanic were broken when the ship hit the iceberg.',
          'C': 'The Titanic was always running late and never kept the right time.',
          'D': 'Morgan used her magic to stop all the clocks in the whole world.'}, 'A',
         ['That’s exactly when the ship went down,” he said.',
          'I guess that’s when time stopped for the Titanic,” she said.']),
        ('PLOT RELATION', 'Why does Annie put the watch on Morgan’s note and say, “A gift from a ship lost at sea”?',
         {'A': 'The watch is the first of the four special gifts needed to break Teddy’s spell.',
          'B': 'She wants to give the watch to Morgan so that Morgan can keep it.',
          'C': 'Morgan’s note asked them to return a lost watch to the sea.',
          'D': 'She plans to trade the watch for a brand-new research book.'}, 'A',
         ['And now we have the first gift to break the spell he’s under,” said Annie.',
          'A gift from a ship lost at sea,” she said softly.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie take Teddy, a little dog under a spell, to the sinking Titanic, help Lucy and William reach a lifeboat, receive their father’s watch, and escape home with the first gift to free Teddy.',
          'B': 'Jack and Annie sail to New York on the Titanic, warn the captain about the iceberg in time, and save the great ship and all of its passengers from sinking.',
          'C': 'Jack and Annie travel to the Titanic to rescue Morgan, who has been put under a spell by a magic dog, and bring her home safely to Frog Creek.',
          'D': 'Jack and Annie visit an old ship museum, where Teddy finds a silver watch hidden in the library, and they decide to keep it as a souvenir.'}, 'A',
         ['Lucy’s gift,” she said.', 'He saved our lives,” he said.']),
    ],
}

BOOK_TITLE = 'Tonight on the Titanic'
BOOK_TITLE_CN = '泰坦尼克号遇险记'
CHAPTER_TITLES = ['A New Mission', 'The Unsinkable Ship', 'SOS', 'Put on Your Life Belts!',
                  'William and Lucy', 'Women and Children First', 'The Gift',
                  'Every Man for Himself', 'Time Stops', 'A Touch of Magic']


def chapter_text(chapter_index):
    """Rebuild Book 17 chapter text exactly as rebuild_docx_book does."""
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
            # infer the answer position; distribute A/B/C/D evenly across Book 17.
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
                'id': f'B17C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 17, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 17, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 17] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 17 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
