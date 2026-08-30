#!/usr/bin/env python3
"""Author and append the Book 13 (Vacation Under the Volcano) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-12.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 13 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book13_text + rebuild_book13
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book13_text as bt
import rebuild_book13 as rb
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
        ('DETAIL', 'What two letters glowed on Jack’s secret library card?',
         {'A': 'The letters ML, for Master Librarian.', 'B': 'The letters FC, for Frog Creek.',
          'C': 'The letters MF, for Morgan le Fay.', 'D': 'The word POMPEII.'}, 'A',
         ['ran his finger over its shimmering letters: ML.']),
        ('VOCABULARY IN CONTEXT', 'Morgan gives them “an important mission.” A “mission” is a ___.',
         {'A': '任务；使命', 'B': '假期；休假', 'C': '书本；图书', 'D': '梦；梦境'}, 'A',
         ['I have an important mission for you']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan send Jack and Annie to the ancient Roman town?',
         {'A': 'To rescue a lost story before its library is lost forever.',
          'B': 'To take a relaxing vacation in the mountains.',
          'C': 'To find out what caused Annie’s nightmare.',
          'D': 'To deliver a new book to Camelot.'}, 'A',
         ['I need you to get it before the library becomes lost forever.']),
        ('INFERENCE', 'Annie’s nightmare of fire and shaking ground is a hint that ___.',
         {'A': 'something dangerous will happen on this trip',
          'B': 'the trip will be calm and boring',
          'C': 'they will never find the tree house',
          'D': 'Morgan is angry with them'}, 'A',
         ['I dreamed fires were burning,', 'Do you think it was a warning?']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The magic tree house starts to spin and carries them off.',
          'B': 'Jack takes his secret library card from the drawer.',
          'C': 'Morgan hands Jack the book about Roman times.',
          'D': 'Annie tells Jack about her scary nightmare.'}, 'A',
         ['the tree house started to spin.']),
    ],
    2: [
        ('DETAIL', 'What are Jack and Annie wearing when they wake up in the tree house?',
         {'A': 'Tunics and lace-up sandals, like ancient Roman kids.',
          'B': 'Their own jeans, T-shirts, and sneakers.',
          'C': 'Warm parkas and fur boots.',
          'D': 'Gladiator armor and helmets.'}, 'A',
         ['he had on a white tunic with a belt, sandals that laced up',
          'look just like kids in an ancient Roman town.']),
        ('VOCABULARY IN CONTEXT', 'The old woman “wore a black cloak.” A “cloak” is a kind of ___.',
         {'A': '斗篷；披风', 'B': '帽子；头盔', 'C': '鞋子；凉鞋', 'D': '袋子；背包'}, 'A',
         ['She wore a black cloak.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie say they should go home right away?',
         {'A': 'She feels the ground shake and senses something is wrong.',
          'B': 'She is cold and hungry.',
          'C': 'She has lost the story title.',
          'D': 'She wants to watch the gladiators fight.'}, 'A',
         ['The ground shook. I heard it rumble, too,', 'I really think we should go home now.']),
        ('INFERENCE', 'The grove being “strangely silent” with no birds is an early sign that ___.',
         {'A': 'nature is warning that danger is coming',
          'B': 'it is the middle of the night',
          'C': 'the birds are all resting at the beach',
          'D': 'Jack has frightened the birds away'}, 'A',
         ['The grove was strangely silent.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'An old woman warns them, “Go home, strangers!”',
          'B': 'Jack and Annie cross a small wooden bridge into town.',
          'C': 'Jack reads that the seaside town is called Pompeii.',
          'D': 'Jack and Annie wake up wearing Roman clothes.'}, 'A',
         ['Go home, strangers!']),
    ],
    3: [
        ('VOCABULARY IN CONTEXT', 'The book says people who could see the future and warn others were “soothsayers.” A soothsayer is someone who ___.',
         {'A': '能预见未来、向别人发出警告', 'B': '在公共澡堂里干活',
          'C': '在集市上卖水果', 'D': '训练角斗士打斗'}, 'A',
         ['there were people who could see into the future and warn others about what they saw.',
          'These people were called soothsayers.']),
        ('DETAIL', 'The fancy building with large columns turned out to be ___.',
         {'A': 'the Temple of Jupiter.', 'B': 'the town library.',
          'C': 'the amphitheater.', 'D': 'the house of Brutus.'}, 'A',
         ['they came to a fancy building with large columns.',
          'This is the Temple of Jupiter, their chief god.']),
        ('PLOT RELATION', 'How do Annie and Jack differ about the soothsayer’s warning?',
         {'A': 'Annie believes the warning, while Jack thinks soothsayers are just from olden times.',
          'B': 'Both of them ignore the soothsayer completely.',
          'C': 'Both are certain the soothsayer is lying.',
          'D': 'Jack trusts her, but Annie is too scared to listen.'}, 'A',
         ['She was giving us a warning.', 'Soothsayers are from olden times.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie keep walking past the Baths and the Temple?',
         {'A': 'They are searching for a library, and neither building is one.',
          'B': 'They are afraid of the crowds inside.',
          'C': 'They are chasing after the soothsayer.',
          'D': 'They are hunting for the gladiators.'}, 'A',
         ['We have to find the lost library.', 'Is that a library?']),
        ('INFERENCE', 'When Jack sees the chained, shield-carrying warriors, he realizes they are not soldiers but ___.',
         {'A': 'gladiators', 'B': 'guards', 'C': 'soothsayers', 'D': 'farmers'}, 'A',
         ['Soldiers, thought Jack.', 'Gladiators!']),
    ],
    4: [
        ('DETAIL', 'According to Jack’s book, what were gladiators forced to do?',
         {'A': 'Fight each other or wild animals like lions or bears.',
          'B': 'Guard the Temple of Jupiter day and night.',
          'C': 'Row the boats down in the harbor.',
          'D': 'Sell goods in the busy forum.'}, 'A',
         ['They were forced to fight each other or wild animals like lions or bears.']),
        ('VOCABULARY IN CONTEXT', 'Jack “felt a chill go down his spine.” His “spine” is his ___.',
         {'A': '脊柱；脊背', 'B': '手臂', 'C': '喉咙', 'D': '膝盖'}, 'A',
         ['Jack felt a chill go down his spine.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does the soothsayer finally decide to help Jack and Annie?',
         {'A': 'She sees the shimmering letters on Annie’s secret library card.',
          'B': 'Jack pays her a handful of coins.',
          'C': 'Annie promises to take her home with them.',
          'D': 'A guard orders her to help them.'}, 'A',
         ['She pulled out her secret library card.',
          'The soothsayer stared for a moment at the card and the shimmering letters on it.']),
        ('INFERENCE', 'The soothsayer says, “After today, there will be nothing left in Pompeii.” She means that ___.',
         {'A': 'a terrible disaster will destroy the whole town today',
          'B': 'everyone will leave on vacation tomorrow',
          'C': 'the shops will simply close for the night',
          'D': 'the library will be moved to Rome'}, 'A',
         ['After today, there will be nothing left in Pompeii,', 'Nothing at all.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack and Annie race off toward the vacation villa of Brutus.',
          'B': 'A guard blocks them from entering the amphitheater.',
          'C': 'The soothsayer lists the scary things happening in Pompeii.',
          'D': 'Annie pulls out her secret library card.'}, 'A',
         ['Then Annie and Jack started running to the vacation villa.']),
    ],
    5: [
        ('DETAIL', 'What did Jack learn that Romans did while they ate in the dining room?',
         {'A': 'They lay down on couches while they ate.',
          'B': 'They stood around a tall table.',
          'C': 'They always ate outside in the garden.',
          'D': 'They sat cross-legged on the floor.'}, 'A',
         ['People from Roman times lay down on couches while they ate.']),
        ('VOCABULARY IN CONTEXT', 'The main hall had a large opening in the “ceiling.” The ceiling is the ___.',
         {'A': '天花板；顶棚', 'B': '地板', 'C': '墙壁', 'D': '大门'}, 'A',
         ['The main hall had a large opening in the ceiling.']),
        ('INFERENCE', 'Why does Jack think the rolls of paper on the shelves might hold the lost story?',
         {'A': 'His book says Romans wrote their “books” on scrolls of papyrus.',
          'B': 'The soothsayer told him to look on those shelves.',
          'C': 'The scrolls all have pictures of Hercules.',
          'D': 'Morgan drew an X on a map of the villa.'}, 'A',
         ['They wrote their "books" on scrolls of papyrus', 'I bet our ancient lost story is in there!']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie keep rushing from room to room saying “Books? Books?”',
         {'A': 'She is in a hurry to find the books so they can leave the dangerous town.',
          'B': 'She wants to buy the silver dishes.',
          'C': 'She is trying to catch the goldfish.',
          'D': 'She is looking for Brutus himself.'}, 'A',
         ['We have to look in all the rooms for books!', 'No books in this whole villa.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack reads about papyrus and guesses the scrolls hold the lost story.',
          'B': 'Jack and Annie slip into the empty main hall.',
          'C': 'Annie finds the room with rolls of paper on the shelves.',
          'D': 'Jack peeks into the dining room with its couches.'}, 'A',
         ['He found a section called WRITING.']),
    ],
    6: [
        ('VOCABULARY IN CONTEXT', 'Jack sees a picture of “a volcano erupting.” To “erupt” means to ___.',
         {'A': '（火山）喷发；爆发', 'B': '慢慢地冷却', 'C': '安静地睡着', 'D': '缓缓地升起'}, 'A',
         ['he found a picture of a volcano erupting over a town.']),
        ('DETAIL', 'How did Jack and Annie know they had found the right scroll?',
         {'A': 'Its Latin title matched the words on Morgan’s paper.',
          'B': 'It was the biggest scroll on the shelf.',
          'C': 'It had a picture of Hercules on it.',
          'D': 'It glowed with shimmering letters.'}, 'A',
         ['The words at the top matched the one on their paper.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack suddenly panic after reading about Mount Vesuvius?',
         {'A': 'He realizes the deadly eruption happens on this very day.',
          'B': 'He has lost the ancient scroll.',
          'C': 'He cannot read the Latin story.',
          'D': 'A guard is chasing them through the villa.'}, 'A',
         ['it erupted into a deadly volcano.', 'Oh, man, what time is it?']),
        ('INFERENCE', 'How does Jack figure out that it is already noon?',
         {'A': 'The sundial’s shadow can hardly be seen, which the book says happens at noon.',
          'B': 'A clock inside the villa chimes twelve times.',
          'C': 'The soothsayer shouts the time to him.',
          'D': 'The sun is setting in the west.'}, 'A',
         ['The shadow on the sundial can hardly be seen at noon.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack hears a terrible blast, the loudest sound he has ever heard.',
          'B': 'Annie finds the scroll with the matching title.',
          'C': 'Jack reads that Vesuvius erupted at noon.',
          'D': 'Jack and Annie race to the sundial in the garden.'}, 'A',
         ['Just then he heard a terrible blast.']),
    ],
    7: [
        ('VOCABULARY IN CONTEXT', 'The patio stones “were trembling.” “Trembling” means ___.',
         {'A': '颤抖；抖动', 'B': '发光；闪耀', 'C': '静止不动', 'D': '变得温暖'}, 'A',
         ['The patio stones were trembling.']),
        ('DETAIL', 'According to Jack’s book, why was there no running lava from Mount Vesuvius?',
         {'A': 'The magma cooled so fast that it froze into pumice rocks.',
          'B': 'The lava all flowed into the sea first.',
          'C': 'Heavy rain put the lava out.',
          'D': 'The volcano was really much too cold.'}, 'A',
         ['The magma from the volcano cooled so fast that it froze into small grayish white rocks called pumice']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie tie pillows onto their heads?',
         {'A': 'To protect their heads from the falling ash and pumice.',
          'B': 'To keep their ears warm in the cold.',
          'C': 'To disguise themselves as Romans.',
          'D': 'To carry the scrolls more safely.'}, 'A',
         ['We have to cover our heads!', 'Tie it around your head with your belt!']),
        ('INFERENCE', 'Why does the sky turn dark and smoky gray in the middle of the day?',
         {'A': 'A huge cloud of pumice and ash is blocking out the sun.',
          'B': 'Night has simply fallen early.',
          'C': 'A heavy rainstorm is rolling in.',
          'D': 'Jack’s glasses have gotten dirty.'}, 'A',
         ['A thick black cloud was spreading over the earth like an umbrella.',
          'That must be the cloud of pumice and ash!']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack and Annie run out into the dark, burning streets.',
          'B': 'Roof tiles begin falling into the garden.',
          'C': 'Jack reads about magma and pumice.',
          'D': 'They tie pillows onto their heads with their belts.'}, 'A',
         ['They ran from the vacation villa into the dark, burning streets.']),
    ],
    8: [
        ('VOCABULARY IN CONTEXT', 'The Temple’s “walls were crumbling.” “Crumbling” means ___.',
         {'A': '崩塌；碎裂', 'B': '闪闪发光', 'C': '缓缓升起', 'D': '牢牢立着'}, 'A',
         ['Its mighty columns had fallen, and its walls were crumbling.']),
        ('DETAIL', 'Which way do Jack and Annie run, compared with everyone else?',
         {'A': 'Toward Mount Vesuvius, while others run away from it.',
          'B': 'Away from Mount Vesuvius, just like everyone else.',
          'C': 'Into the Public Baths to hide from the ash.',
          'D': 'Back to the house of Brutus.'}, 'A',
         ['So while others ran away from Mount Vesuvius, Jack and Annie ran toward it.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack decide to run toward the erupting mountain?',
         {'A': 'The tree house is in the olive grove, which lies in the direction of Vesuvius.',
          'B': 'He wants a closer look at the glowing lava.',
          'C': 'The soothsayer told him to climb the mountain.',
          'D': 'He is trying to rescue the chained gladiators.'}, 'A',
         ['The tree house is in the olive grove!', 'Head in the direction of Mount Vesuvius!']),
        ('PLOT RELATION', 'How does the erupting town connect to the nightmare Annie had in Chapter 1?',
         {'A': 'The dark, burning, shaking scene is exactly what Annie dreamed.',
          'B': 'The nightmare has nothing to do with the eruption.',
          'C': 'Annie had dreamed of a peaceful beach, not fire.',
          'D': 'It was really Jack who had the nightmare.'}, 'A',
         ['This is just like my nightmare!']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack and Annie discover that the bridge has vanished.',
          'B': 'The roof of the Public Baths caves in.',
          'C': 'The columns of the Temple of Jupiter fall.',
          'D': 'Annie shouts “That way!” in the forum.'}, 'A',
         ['The bridge had vanished.']),
    ],
    9: [
        ('VOCABULARY IN CONTEXT', 'The pumice “piled up in huge drifts, like snow.” Here “drifts” are ___.',
         {'A': '（堆积成的）大堆；堆积物', 'B': '小溪；水流', 'C': '一串脚印', 'D': '飞舞的火花'}, 'A',
         ['Pumice had piled up in huge drifts, like snow.']),
        ('DETAIL', 'What did Annie do to try to save them when they were trapped in the pumice?',
         {'A': 'She held up the ancient scroll and shouted, “Save us, story!”',
          'B': 'She dug a tunnel through the pumice.',
          'C': 'She called out for the soothsayer.',
          'D': 'She climbed up onto Jack’s shoulders.'}, 'A',
         ['Annie grabbed it and pulled out the ancient scroll.', 'Save us, story!']),
        ('CAUSE / PURPOSE / RESULT', 'What makes the giant gladiator appear and rescue them?',
         {'A': 'Annie holds up the ancient story and begs it to save them.',
          'B': 'Jack finally digs himself free.',
          'C': 'Morgan flies in on the magic tree house.',
          'D': 'The soothsayer pulls them out of the pumice.'}, 'A',
         ['In your darkest hour, only the ancient story can save you!', 'Then someone lifted Jack up into the air.']),
        ('INFERENCE', 'The rescuer “looked like a gladiator—but even bigger than the ones they had seen earlier.” This suggests he is ___.',
         {'A': 'no ordinary man, but someone truly extraordinary',
          'B': 'one of the chained gladiators from the amphitheater',
          'C': 'the soothsayer wearing a disguise',
          'D': 'Jack’s own father'}, 'A',
         ['The man looked like a gladiator—but even bigger than the ones they had seen earlier.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The tree house spins and everything becomes still.',
          'B': 'Jack and Annie sink into the deep pumice.',
          'C': 'The giant gladiator lifts them to the far bank.',
          'D': 'Annie holds up the ancient scroll to the sky.'}, 'A',
         ['Jack felt the tree house start to spin.', 'Then everything was still.']),
    ],
    10: [
        ('VOCABULARY IN CONTEXT', 'Morgan says Jack and Annie were “truly brave.” “Brave” means ___.',
         {'A': '勇敢的；无畏的', 'B': '疲倦的', 'C': '害怕的', 'D': '诚实的'}, 'A',
         ['But you were truly brave,']),
        ('DETAIL', 'Morgan reveals that the rescued scroll is a lost tale about which hero?',
         {'A': 'Hercules, a son of Jupiter.', 'B': 'Jupiter, the chief god.',
          'C': 'Brutus, who owned the villa.', 'D': 'Apollo, the sun god.'}, 'A',
         ['a lost tale about Hercules.', 'He was a son of Jupiter.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan say she is “deeply grateful” to Jack and Annie?',
         {'A': 'They risked everything to bring her the ancient story.',
          'B': 'They cleaned all the dust off the scroll.',
          'C': 'They defeated the gladiators in a fight.',
          'D': 'They drew her a detailed map of Pompeii.'}, 'A',
         ['You risked everything to bring this to me.']),
        ('PLOT RELATION', 'What is Annie’s “simple explanation” for how Hercules could save them?',
         {'A': 'In Roman times people believed Hercules was real, so he was real to them there.',
          'B': 'Hercules is truly real everywhere and in every time.',
          'C': 'The giant was really Morgan in disguise.',
          'D': 'They only imagined the whole rescue.'}, 'A',
         ['But in Roman times, lots of people believed he was real.',
          'since we were in Roman times, he was real to us.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to ancient Pompeii, rescue a lost scroll as Mount Vesuvius erupts, are saved by a Hercules-like giant, and bring the story safely home to Morgan.',
          'B': 'Jack and Annie explore the frozen Arctic and make friends with polar bears.',
          'C': 'Jack and Annie visit a castle in Camelot and meet King Arthur.',
          'D': 'Jack and Annie sail the ocean hunting for a sunken treasure ship.'}, 'A',
         ['You witnessed a famous event in history.', 'most of the people of Pompeii did escape.']),
    ],
}

BOOK_TITLE = 'Vacation Under the Volcano'
BOOK_TITLE_CN = '庞贝城的末日'
CHAPTER_TITLES = bt.TITLES


def chapter_text(chapter_index):
    """Rebuild Book 13 chapter text exactly as rebuild_docx_book does."""
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
            # infer the answer position; distribute A/B/C/D evenly across Book 13.
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
                'id': f'B13C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 13, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 13, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 13] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 13 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
