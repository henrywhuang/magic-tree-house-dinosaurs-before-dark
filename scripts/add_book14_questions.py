#!/usr/bin/env python3
"""Author and append the Book 14 (Day of the Dragon King) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-12.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 14 is a docx-sourced title, so the chapter text is
reconstructed exactly as ``rebuild_docx_book`` builds the reader JSON
(book14_text + rebuild_book14.FIXES + shared cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book14_text as bt
import rebuild_book14 as rb
import rebuild_docx_book as rdb

TARGET = ROOT / 'data' / 'questions.json'

# Balanced, non-repeating answer positions (one five-question row per chapter).
ANSWER_PATTERNS = ('BDACA', 'CADBD', 'ADBCB', 'DCABA', 'BACDC',
                   'CBDAD', 'ACDBB', 'DABCC', 'BCDAD', 'ADCBB')

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
        ('DETAIL', 'What does Jack take out of his dresser drawer to bring on the trip to China?',
         {'A': 'A thin wooden library card.', 'B': 'A bamboo strip with Chinese writing.',
          'C': 'An old paper map of China.', 'D': 'A dragon-shaped medal.'}, 'A',
         ['took out a thin wooden card.']),
        ('VOCABULARY IN CONTEXT', 'Morgan says the characters are the title of an “ancient Chinese legend.” A “legend” is ___.',
         {'A': '传说；世代流传下来的故事', 'B': '一本数学练习册', 'C': '一张地图', 'D': '一封信'}, 'A',
         ['the title of an ancient Chinese legend.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Jack drops his library card into his backpack.', 'B': 'Morgan hands Jack the research book.',
          'C': 'The tree house begins to spin.', 'D': 'Jack and Annie climb the rope ladder into the tree house.'}, 'A',
         ['Jack dropped the card into his backpack.']),
        ('CAUSE / PURPOSE / RESULT', 'Why must Jack and Annie hurry to find the ancient legend?',
         {'A': 'The Imperial Library is about to be destroyed.', 'B': 'A storm is coming to Frog Creek.',
          'C': 'Morgan will lock the tree house at noon.', 'D': 'Their mom wants them home for dinner.'}, 'A',
         ['before the Imperial Library is destroyed.']),
        ('INFERENCE', 'Morgan warns, “in your darkest hour, only the old legend can save you.” This suggests that ___.',
         {'A': 'the legend will become important when they are in real danger', 'B': 'the legend is only a bedtime story',
          'C': 'they should burn the legend once they read it', 'D': 'the research book is useless'}, 'A',
         ['only the old legend can save you.']),
    ],
    2: [
        ('DETAIL', 'What had happened to Jack and Annie’s clothes when Jack opened his eyes?',
         {'A': 'They had magically changed into ancient Chinese clothes.', 'B': 'They had turned into shiny armor.',
          'C': 'They had disappeared completely.', 'D': 'They were soaking wet from the rain.'}, 'A',
         ['Their clothes had magically changed.']),
        ('VOCABULARY IN CONTEXT', 'Annie says the land “looks so peaceful.” Here “peaceful” means ___.',
         {'A': '安宁的；平静的', 'B': '危险的；吓人的', 'C': '拥挤的；吵闹的', 'D': '寒冷的；结冰的'}, 'A',
         ['It looks so peaceful']),
        ('CAUSE / PURPOSE / RESULT', 'Why is the first emperor called the “Dragon King”?',
         {'A': 'He chose the dragon to be his symbol.', 'B': 'He could turn into a real dragon.',
          'C': 'He was born in the Year of the Dragon.', 'D': 'He kept a pet dragon in his palace.'}, 'A',
         ['he chose the dragon to be his symbol']),
        ('DETAIL', 'What favor does the young cowherd ask Jack and Annie to do?',
         {'A': 'Give a message to the silk weaver.', 'B': 'Help him herd his cows home.',
          'C': 'Carry his bag into the city.', 'D': 'Hide him from the Dragon King’s guards.'}, 'A',
         ['Give a message to the silk weaver.']),
        ('INFERENCE', 'The cowherd’s warning, “Beware of the Dragon King,” suggests that ___.',
         {'A': 'the Dragon King is dangerous and this place is not really peaceful',
          'B': 'the Dragon King is a kind and gentle ruler', 'C': 'the Dragon King is only a made-up character',
          'D': 'the Dragon King wants to give them a gift'}, 'A',
         ['Beware of the Dragon King,']),
    ],
    3: [
        ('DETAIL', 'What was the young woman doing on the open porch?',
         {'A': 'Weaving cloth on a loom.', 'B': 'Cooking rice over a fire.',
          'C': 'Feeding the oxen hay.', 'D': 'Painting a picture of a dragon.'}, 'A',
         ['a young woman was weaving cloth on a loom.']),
        ('VOCABULARY IN CONTEXT', 'The weaver gives Annie “a ball of yellow thread.” Here “thread” means ___.',
         {'A': '线；丝线', 'B': '面包', 'C': '硬币', 'D': '石头'}, 'A',
         ['a ball of yellow thread.']),
        ('DETAIL', 'How is silk made, according to the weaver?',
         {'A': 'From the cocoons of silkworms.', 'B': 'From the wool of sheep.',
          'C': 'From the leaves of tea plants.', 'D': 'From the petals of yellow flowers.'}, 'A',
         ['It is made from the cocoons of silkworms,']),
        ('CAUSE / PURPOSE / RESULT', 'Why does the silk weaver beg Jack not to write down how silk is made?',
         {'A': 'The making of silk is China’s most valuable secret, and stealing it is punished by death.',
          'B': 'Jack’s handwriting is too messy to read.', 'C': 'She wants to keep the recipe for a surprise gift.',
          'D': 'Writing is forbidden for children in China.'}, 'A',
         ['The making of silk is China’s most valuable secret.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A man points at them, and Jack and Annie run away.', 'B': 'Annie gives the weaver the cowherd’s message.',
          'C': 'The weaver hands Annie a ball of silk.', 'D': 'Jack feels how smooth the silk thread is.'}, 'A',
         ['A man was pointing at them.']),
    ],
    4: [
        ('SEQUENCE', 'What do Jack and Annie do FIRST when the shouting people come closer?',
         {'A': 'They dive into the back of the wooden cart and hide in the bags of grain.',
          'B': 'They jump out of the cart in the city.', 'C': 'They read about the Great Wall of China.',
          'D': 'They meet the driver of the cart.'}, 'A',
         ['dived into the back of the wooden cart.']),
        ('VOCABULARY IN CONTEXT', '“Suddenly the cart lurched forward.” To “lurch” is to ___.',
         {'A': '突然晃动；猛地前倾', 'B': '慢慢停下', 'C': '轻轻歌唱', 'D': '静静躺着'}, 'A',
         ['the cart lurched forward.']),
        ('CAUSE / PURPOSE / RESULT', 'According to the research book, why did the Dragon King force his subjects to build a wall?',
         {'A': 'To protect China from invaders.', 'B': 'To give the workers something fun to do.',
          'C': 'To block the river from flooding.', 'D': 'To hide his burial tomb.'}, 'A',
         ['start building a wall to protect China from invaders.']),
        ('DETAIL', 'What famous structure are the workers building?',
         {'A': 'The Great Wall of China.', 'B': 'The Imperial Library.',
          'C': 'A giant stone dragon.', 'D': 'The Dragon King’s palace.'}, 'A',
         ['The Great Wall of China is the longest structure ever built.']),
        ('INFERENCE', 'When the driver sees Jack’s paper book, “his mouth dropped open.” This shows he is ___.',
         {'A': 'amazed, because he has never seen a paper book before', 'B': 'bored by the strange object',
          'C': 'angry that they are reading', 'D': 'sleepy after the long ride'}, 'A',
         ['His mouth dropped open.']),
    ],
    5: [
        ('DETAIL', 'What is the cart driver’s real identity, even though he is dressed as a farmer?',
         {'A': 'He is a scholar.', 'B': 'He is a soldier.',
          'C': 'He is the Dragon King’s son.', 'D': 'He is a silk merchant.'}, 'A',
         ['I am a scholar!']),
        ('VOCABULARY IN CONTEXT', 'The scholar says scholars are “the most honored citizens.” Here “honored” means ___.',
         {'A': '受尊敬的；尊贵的', 'B': '贫穷的；可怜的', 'C': '害怕的；胆小的', 'D': '普通的；平凡的'}, 'A',
         ['the most honored citizens in China.']),
        ('CAUSE / PURPOSE / RESULT', 'Why is the Dragon King afraid of books and learning?',
         {'A': 'He wants people to think only what he wants them to think.', 'B': 'He cannot read or write himself.',
          'C': 'Books make the palace too crowded.', 'D': 'He is allergic to bamboo strips.'}, 'A',
         ['He wants people to think only what he wants them to think.']),
        ('PLOT RELATION', 'How does the scholar react when Jack and Annie show him their shimmering library cards?',
         {'A': 'He is amazed and bows to show his respect.', 'B': 'He laughs and calls them liars.',
          'C': 'He grabs the cards and runs away.', 'D': 'He throws the cards into the fire.'}, 'A',
         ['He bowed to show his respect.']),
        ('INFERENCE', 'When Jack describes libraries in every town, the scholar says, “It sounds like paradise.” This shows the scholar ___.',
         {'A': 'longs for a place where books are free and safe', 'B': 'thinks Frog Creek is a boring place',
          'C': 'does not believe Jack at all', 'D': 'wants to move to the Dragon King’s palace'}, 'A',
         ['It sounds like paradise,']),
    ],
    6: [
        ('DETAIL', 'When are the city gates closed each day?',
         {'A': 'At sunset, when the gong sounds.', 'B': 'At sunrise, when the roosters crow.',
          'C': 'At noon, when the market opens.', 'D': 'At midnight, when the moon rises.'}, 'A',
         ['every day at sunset,']),
        ('VOCABULARY IN CONTEXT', 'The curved roofs are meant to keep away “bad spirits.” Here “spirits” means ___.',
         {'A': '鬼魂；亡灵', 'B': '力气；精力', 'C': '饮料；果汁', 'D': '心情；情绪'}, 'A',
         ['To keep away the bad spirits,']),
        ('CAUSE / PURPOSE / RESULT', 'Why are the roofs of the larger houses curved?',
         {'A': 'To keep away bad spirits, which can only travel in straight lines.',
          'B': 'To let rainwater slide off quickly.', 'C': 'To make the houses look like dragons.',
          'D': 'To catch more sunlight in winter.'}, 'A',
         ['The spirits can only travel in straight lines,']),
        ('DETAIL', 'How many workers have been building the Dragon King’s burial tomb?',
         {'A': 'Three hundred thousand.', 'B': 'One hundred.', 'C': 'Seven thousand.', 'D': 'A dozen.'}, 'A',
         ['Three hundred thousand workers have been building his burial tomb.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The Dragon King steps outside in a rich robe and a tall hat.',
          'B': 'The oxcart crosses the wooden bridge over the moat.', 'C': 'The cart passes the busy market square.',
          'D': 'A dark cloud of smoke rises from the courtyard.'}, 'A',
         ['Stepping outside was a man in a rich, flowing robe and a tall hat.']),
    ],
    7: [
        ('DETAIL', 'What does the scholar point out to Jack and Annie near the fire?',
         {'A': 'A bamboo book that had fallen off a waiting stack — their story.', 'B': 'A hidden door behind the flames.',
          'C': 'The Dragon King’s crown.', 'D': 'A cage full of crickets.'}, 'A',
         ['He pointed to a bamboo book that had fallen off a waiting stack.']),
        ('VOCABULARY IN CONTEXT', 'Annie “snatched up the bundle of bamboo strips.” To “snatch” is to ___.',
         {'A': '抢夺；一把抓起', 'B': '慢慢阅读', 'C': '轻轻放下', 'D': '仔细数数'}, 'A',
         ['she had already snatched up the bundle of bamboo strips']),
        ('CAUSE / PURPOSE / RESULT', 'Why does the scholar tell them to run through the burial grounds?',
         {'A': 'The soldiers fear the spirits of the ancestors and will be afraid to follow.',
          'B': 'The burial grounds have a secret exit to the woods.', 'C': 'The Dragon King never goes there.',
          'D': 'It is the shortest way back to the cart.'}, 'A',
         ['They fear the spirits of the ancestors!']),
        ('DETAIL', 'How do Jack and Annie get away from the flying arrows?',
         {'A': 'They duck inside a doorway in one of the mounds.', 'B': 'They dive into the moat.',
          'C': 'They climb the palace tower.', 'D': 'They hide behind the bonfire.'}, 'A',
         ['Jack and Annie ducked inside.']),
        ('SEQUENCE', 'What do Jack and Annie find at the bottom of the steep steps?',
         {'A': 'A room filled with thousands of soldiers.', 'B': 'A pile of burning books.',
          'C': 'The silk weaver’s loom.', 'D': 'A chest full of jade jewelry.'}, 'A',
         ['a room filled with soldiers']),
    ],
    8: [
        ('DETAIL', 'What does Annie do to show Jack that the soldiers are not real?',
         {'A': 'She pulls a soldier’s nose.', 'B': 'She knocks a soldier over.',
          'C': 'She waves a torch at them.', 'D': 'She calls out their names.'}, 'A',
         ['Annie pulled the soldier’s nose.']),
        ('VOCABULARY IN CONTEXT', 'The tomb soldiers are lifesize “clay” figures. “Clay” is ___.',
         {'A': '黏土；陶土', 'B': '黄金', 'C': '玻璃', 'D': '木头'}, 'A',
         ['The clay was baked and painted.']),
        ('CAUSE / PURPOSE / RESULT', 'Why did the Dragon King have the clay army made?',
         {'A': 'He hoped it would protect him after he died.', 'B': 'He wanted to sell the figures at the market.',
          'C': 'He needed workers for the Great Wall.', 'D': 'He wanted gifts for the silk weaver.'}, 'A',
         ['the clay army would protect him after he died.']),
        ('INFERENCE', 'When Jack “tried not to panic,” it shows that he is ___.',
         {'A': 'frightened but struggling to stay calm', 'B': 'completely relaxed and happy',
          'C': 'bored and sleepy', 'D': 'proud of finding the tomb'}, 'A',
         ['Jack tried not to panic.']),
        ('SEQUENCE', 'What happens at the very END of this chapter?',
         {'A': 'The ball of yellow silk thread rolls out of the sack, leaving a trail.',
          'B': 'Annie pulls a soldier’s nose.', 'C': 'Jack reads about the clay army in the research book.',
          'D': 'Jack holds up the bamboo book and asks for help.'}, 'A',
         ['leaving a trail of yellow thread!']),
    ],
    9: [
        ('PLOT RELATION', 'How does the ball of silk thread help Jack and Annie?',
         {'A': 'It rolls ahead and leaves a trail that leads them out of the maze of soldiers.',
          'B': 'It ties the soldiers together so they cannot move.', 'C': 'It glows brightly enough to read the research book.',
          'D': 'It turns into a rope they climb up.'}, 'A',
         ['They followed the trail of thread down the row,']),
        ('VOCABULARY IN CONTEXT', 'After their straw shoes fall off, Jack and Annie run “barefoot.” “Barefoot” means ___.',
         {'A': '赤脚的；光着脚', 'B': '飞快的', 'C': '疲倦的', 'D': '悄悄的'}, 'A',
         ['Jack and Annie kept running barefoot.']),
        ('DETAIL', 'What warns Jack and Annie that the city gates are about to close?',
         {'A': 'A gong sounding from the tower of the city walls.', 'B': 'The silk weaver calling to them.',
          'C': 'The Dragon King’s soldiers shouting.', 'D': 'The crickets suddenly going silent.'}, 'A',
         ['a gong sounded.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie race through the city as fast as they can?',
         {'A': 'If they do not get out before the gates close, they will be trapped for the night.',
          'B': 'They want to buy something at the market.', 'C': 'They are chasing the ball of silk thread.',
          'D': 'They want to say goodbye to the scholar.'}, 'A',
         ['They’re going to close the gates!']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack and Annie see the silk weaver and the cowherd find each other and embrace.',
          'B': 'They tear through the closing city gates.', 'C': 'They run barefoot past the market.',
          'D': 'Jack collapses inside the tree house.'}, 'A',
         ['Two figures embraced at the edge of the field.']),
    ],
    10: [
        ('DETAIL', 'What is the name of the ancient legend Jack and Annie brought back?',
         {'A': '“The Silk Weaver and the Cowherd.”', 'B': '“The Day of the Dragon King.”',
          'C': '“The Great Wall of China.”', 'D': '“The Clay Army.”'}, 'A',
         ['It’s called The Silk Weaver and the Cowherd,']),
        ('VOCABULARY IN CONTEXT', 'Morgan says the couple were “heavenly beings who lived in the sky.” “Heavenly” means ___.',
         {'A': '天上的；天国的', 'B': '沉重的', 'C': '快乐的', 'D': '古老的'}, 'A',
         ['they were heavenly beings who lived in the sky,']),
        ('PLOT RELATION', 'Who were the silk weaver and the cowherd, according to the legend?',
         {'A': 'Heavenly beings who came to earth and fell in love.', 'B': 'A princess and a soldier of the Dragon King.',
          'C': 'Two scholars hiding from the emperor.', 'D': 'The Dragon King’s own children.'}, 'A',
         ['When they came to earth, they fell in love.']),
        ('CAUSE / PURPOSE / RESULT', 'Why can the two lovers meet only once a year?',
         {'A': 'The king and queen of the skies separated them by the Milky Way.',
          'B': 'The Dragon King locked them in the tomb.', 'C': 'They live on opposite sides of the Great Wall.',
          'D': 'They are too busy weaving silk and herding cows.'}, 'A',
         ['separated them by a heavenly river called the Milky Way.']),
        ('SUMMARY', 'Which sentence best summarizes the whole book?',
         {'A': 'In ancient China, Jack and Annie befriend a cowherd, a silk weaver, and a scholar, rescue an ancient legend from the book-burning Dragon King, and escape through his clay-army tomb.',
          'B': 'Jack and Annie explore the Arctic and make friends with polar bears.',
          'C': 'Jack and Annie visit a castle in Ireland and meet Viking raiders.',
          'D': 'Jack and Annie dig for pirate treasure on a sunny island.'}, 'A',
         ['We brought you the ancient legend,']),
    ],
}

BOOK_TITLE = 'Day of the Dragon King'
BOOK_TITLE_CN = '末代龙王'
CHAPTER_TITLES = bt.TITLES


def chapter_text(pages, chapter_index):
    """Reconstruct chapter text exactly as rebuild_docx_book builds the reader
    JSON: book14_text + rebuild_book14.FIXES + shared cleanup."""
    text = bt.chapter_text(chapter_index)
    for old, new in rb.FIXES.get(chapter_index, []):
        if old in text:
            text = text.replace(old, new)
    return rdb._cleanup(text).strip()


def build_book():
    texts = {c: chapter_text(None, c - 1) for c in range(1, 11)}
    chapters, problems = [], []
    for chapter_number in range(1, 11):
        norm_text = re.sub(r'[“”"\'’]', '', texts[chapter_number])
        questions = []
        for question_number, (tag, stem, options, answer, evidence) in enumerate(CH[chapter_number], start=1):
            standard, skill, dok, difficulty = META[tag]
            for piece in evidence:
                if re.sub(r'[“”"\'’]', '', piece) not in norm_text:
                    problems.append(f'ch{chapter_number} Q{question_number}: evidence not found: {piece!r}')
            # Source declarations keep the correct choice first for easy review.
            # Rotate it deterministically in the emitted quiz so learners cannot
            # infer the answer position; distribute A/B/C/D evenly across Book 14.
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
                'id': f'B14C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 14, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 14, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 14] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 14 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
