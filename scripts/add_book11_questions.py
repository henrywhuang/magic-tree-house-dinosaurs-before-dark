#!/usr/bin/env python3
"""Author and append the Book 11 (Lions at Lunchtime) reading-comprehension set.

Book 11 is not in the 1-10 assessment DOCX, so the 50 items (5 per chapter) are
written here to the same schema as Books 1-10, ability-oriented (RL.5.x mix).
Every ``evidence`` string is verified to occur verbatim in the chapter text
(tmp/book11_text) before writing, so the shown proof is faithful to the story.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book11_text as bt
import rebuild_book11 as rb  # its chapter_text applies the OCR fixes the reader shows

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


# (tag, stem, {A..D}, answer, [evidence...]).  evidence must be verbatim story text
# (verified below); vocabulary items use the meaning as its own rationale support.
CH = {
    1: [
        ('DETAIL', 'What did Jack’s heavy pack hold as he walked home from the grocery store?',
         {'A': 'A big jar of peanut butter and a loaf of bread.', 'B': 'Two ancient scrolls and a book.',
          'C': 'A notebook, a pencil, and a camera.', 'D': 'A cowboy hat and a pair of boots.'}, 'A',
         ['It held a big jar of peanut butter and a loaf of bread.']),
        ('VOCABULARY IN CONTEXT', 'In “a small, delicate animal,” the word “delicate” most nearly means ___.',
         {'A': '娇小柔弱的', 'B': '凶猛危险的', 'C': '又高又壮的', 'D': '肮脏的'}, 'A',
         ['In the shadows stood a small, delicate animal.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Morgan hands Annie the third riddle.', 'B': 'Jack and Annie follow the gazelle into the woods.',
          'C': 'Annie makes a wish to go to Africa.', 'D': 'Jack opens the book to a picture of African animals.'}, 'B',
         ['They followed as fast as they could.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie want to become Master Librarians?',
         {'A': 'So they can help Morgan in her work.', 'B': 'So they can keep the magic books forever.',
          'C': 'So they can live in the tree house.', 'D': 'So they never have to go home.'}, 'A',
         ['So you can help me in my work?']),
        ('INFERENCE', 'What can you tell about the magic tree house from the end of the chapter?',
         {'A': 'It carries them to the place in the picture when they make a wish.',
          'B': 'It only travels exactly at noon.', 'C': 'It cannot move unless Morgan is inside.',
          'D': 'It flies slowly like a bird.'}, 'A',
         ['I wish we could go there,', 'The tree house had started to spin.']),
    ],
    2: [
        ('DETAIL', 'What was eating leaves off the tree outside the tree house window?',
         {'A': 'A giraffe.', 'B': 'A zebra.', 'C': 'A gazelle.', 'D': 'An elephant.'}, 'A',
         ['A giraffe was eating leaves off the tree.']),
        ('VOCABULARY IN CONTEXT', 'Jack explains that to “migrate” means to ___.',
         {'A': '一年中去别的地方待一段时间', 'B': '整天睡大觉', 'C': '互相打架', 'D': '停在原地不动'}, 'A',
         ['It means they go someplace else for part of the year']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie leave the tree house and head for the river?',
         {'A': 'To help the wild beasts migrate across the river.', 'B': 'To look for the hidden lions.',
          'C': 'To find Morgan le Fay.', 'D': 'To wash the mud off her clothes.'}, 'A',
         ['I have to help them migrate.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack reads aloud about the animals migrating.', 'B': 'Annie shouts, “Jump, beasts! Jump!”',
          'C': 'Annie walks through the tall grass between the zebras and giraffes.',
          'D': 'A giraffe eats leaves outside the window.'}, 'C',
         ['she started to walk through the tall grass, between the zebras and giraffes.']),
        ('INFERENCE', 'The repeated question “Where are the lions?” shows that Jack is mainly ___.',
         {'A': 'worried about running into the lions', 'B': 'bored with the trip',
          'C': 'hoping to pet a lion', 'D': 'looking for Morgan'}, 'A',
         ['Where are the lions?']),
    ],
    3: [
        ('DETAIL', 'According to the Africa book, why do lions tend to avoid giraffes?',
         {'A': 'The giraffe has a very powerful kick.', 'B': 'Giraffes are too tall to catch.',
          'C': 'Giraffes can run much faster than lions.', 'D': 'Giraffes travel in huge herds.'}, 'A',
         ['The giraffe has a very powerful kick, which makes it dangerous to attack.']),
        ('DETAIL', 'Why must every baby zebra learn its own mother’s pattern?',
         {'A': 'Because no two zebras have exactly the same pattern of stripes.',
          'B': 'Because zebras cannot see colors.', 'C': 'Because mothers change their stripes each year.',
          'D': 'Because baby zebras live far from their mothers.'}, 'A',
         ['no two zebras have exactly the same pattern of stripes']),
        ('SUMMARY', 'Which sentence best summarizes this chapter?',
         {'A': 'While Jack stops to study the animals and take notes, Annie suddenly disappears near the river.',
          'B': 'Jack and Annie ride a giraffe to safety past the lions.',
          'C': 'An elephant sprays Jack and Annie until they are clean.',
          'D': 'Jack and Annie share a picnic with a Masai warrior.'}, 'A',
         ['She had vanished.']),
        ('VOCABULARY IN CONTEXT', '“She had vanished” tells you that Annie had ___.',
         {'A': '消失不见了', 'B': '睡着了', 'C': '大声喊叫', 'D': '过了河'}, 'A',
         ['She had completely disappeared.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack run as fast as he can at the end of the chapter?',
         {'A': 'Annie has disappeared and is calling for help.', 'B': 'A lion is chasing him.',
          'C': 'He wants to be first across the river.', 'D': 'He has dropped his notebook in the grass.'}, 'A',
         ['“Help!” called Annie.']),
    ],
    4: [
        ('DETAIL', 'What had Annie fallen into near the water?',
         {'A': 'A pool of mud.', 'B': 'The rushing river.', 'C': 'A deep, dark hole.', 'D': 'A patch of thorns.'}, 'A',
         ['Annie had fallen into a pool of mud near the water.']),
        ('DETAIL', 'What did Jack use to reach Annie and pull her toward the roots?',
         {'A': 'A fallen tree branch.', 'B': 'A long rope.', 'C': 'His backpack strap.', 'D': 'A giraffe’s neck.'}, 'A',
         ['He saw a fallen tree branch near the bank.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack say “Uh-oh” when a shadow passes over them?',
         {'A': 'A huge vulture is circling overhead.', 'B': 'A lion has appeared on the bank.',
          'C': 'A storm cloud has blocked the sun.', 'D': 'The wildebeests have reached them.'}, 'A',
         ['A huge vulture circled overhead.']),
        ('VOCABULARY IN CONTEXT', 'When Jack says “Concentrate, Annie,” he wants her to ___.',
         {'A': '集中注意力', 'B': '大声呼救', 'C': '松开树枝', 'D': '游到对岸'}, 'A',
         ['“Concentrate, Annie,” said Jack']),
        ('INFERENCE', 'How does Annie finally pull herself free of the mud?',
         {'A': 'She lets go of the branch and grabs the tree roots.', 'B': 'The wildebeests push her out.',
          'C': 'Jack lifts her out with the branch alone.', 'D': 'The vulture frightens the mud away.'}, 'A',
         ['She lunged for the roots. She grabbed them!']),
    ],
    5: [
        ('DETAIL', 'How does Annie get the swimming wildebeests to a safe spot?',
         {'A': 'She waves them in like a traffic policeman.', 'B': 'She throws grass to lead them.',
          'C': 'She builds a little bridge.', 'D': 'She rides across on one of them.'}, 'A',
         ['She waved them in like a traffic policeman.']),
        ('VOCABULARY IN CONTEXT', 'Jack says a “predator” is an animal that ___.',
         {'A': '捕捉并吃掉别的动物', 'B': '只吃青草', 'C': '会像人一样大笑', 'D': '帮助别的动物过河'}, 'A',
         ['It means it catches things and eats them,']),
        ('DETAIL', 'According to the book, what does the hyena have a reputation for being?',
         {'A': 'A thief and a coward.', 'B': 'A brave hunter.', 'C': 'A loyal friend.', 'D': 'The fastest runner.'}, 'A',
         ['The hyena has a reputation for being a thief and a coward.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie make monster faces and rush at the hyenas?',
         {'A': 'To scare the hyenas away.', 'B': 'To make the hyenas laugh with them.',
          'C': 'To catch a hyena for the book.', 'D': 'To warn the drinking zebras.'}, 'A',
         ['The hyenas yelped and scurried off.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Something very big begins coming out of the trees by the pond.',
          'B': 'The wildebeests scramble safely over the riverbank.',
          'C': 'Two laughing hyenas move closer to Jack and Annie.',
          'D': 'Annie waves the wildebeests toward a sandy spot.'}, 'A',
         ['something very big was coming out of the trees.']),
    ],
    6: [
        ('DETAIL', 'What steps out of the shadows and wades into the pond?',
         {'A': 'An elephant.', 'B': 'A lion.', 'C': 'A hyena.', 'D': 'A giraffe.'}, 'A',
         ['an elephant stepped out of the shadows.']),
        ('DETAIL', 'How does the elephant get Jack and Annie clean?',
         {'A': 'It sprays them with water from its trunk.', 'B': 'It rolls them in soft grass.',
          'C': 'It wipes them with big leaves.', 'D': 'It nudges them into the deep pond.'}, 'A',
         ['He’s giving me a shower!']),
        ('VOCABULARY IN CONTEXT', 'Annie says she is “spick-and-span” now, which means she is ___.',
         {'A': '干干净净的', 'B': '又累又饿的', 'C': '满身泥巴的', 'D': '冷得发抖的'}, 'A',
         ['Finally, she was clean and soaking wet.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie decide to follow the little gray bird?',
         {'A': 'She feels the bird needs help and is trying to tell them something.',
          'B': 'The bird has stolen her backpack.', 'C': 'Jack orders her to chase it.',
          'D': 'She wants to catch it for the elephant.'}, 'A',
         ['She’s trying to tell us something,']),
        ('INFERENCE', 'What is Jack afraid they might run into in the forest?',
         {'A': 'A snake or a lion.', 'B': 'Another elephant.', 'C': 'The two hyenas again.',
          'D': 'A Masai warrior.'}, 'A',
         ['a snake or a lion,']),
    ],
    7: [
        ('DETAIL', 'What is the round brown thing hanging from the low branch?',
         {'A': 'A beehive.', 'B': 'A bird’s nest.', 'C': 'A basket of fruit.', 'D': 'A honeycomb lantern.'}, 'A',
         ['It’s a beehive.']),
        ('DETAIL', 'What is the little gray bird called?',
         {'A': 'A honey guide.', 'B': 'A honeybird.', 'C': 'A Masai finch.', 'D': 'A bee-eater.'}, 'A',
         ['This bird is called a honey guide.']),
        ('CAUSE / PURPOSE / RESULT', 'How do Jack and Annie make the bees scatter?',
         {'A': 'They wave giant fan-like weeds near the tree.', 'B': 'They light a small smoky fire.',
          'C': 'They splash water on the hive.', 'D': 'They shout loudly at the bees.'}, 'A',
         ['They waved them near the tree, and the bees scattered.']),
        ('SUMMARY', 'Which sentence best summarizes this chapter?',
         {'A': 'A honey guide leads Jack and Annie to a beehive; they take the honey, solve the riddle, and meet a Masai warrior.',
          'B': 'Jack and Annie ride a giraffe safely past the sleeping lions.',
          'C': 'An elephant sprays Jack and Annie until the mud is gone.',
          'D': 'Annie sinks into a mud hole and Jack pulls her out.'}, 'A',
         ['This bird is called a honey guide.']),
        ('INFERENCE', 'What is the answer to Morgan’s riddle?',
         {'A': 'Honey.', 'B': 'A giraffe.', 'C': 'The magic tree house.', 'D': 'A gazelle.'}, 'A',
         ['We’ve answered Morgan’s riddle.']),
    ],
    8: [
        ('DETAIL', 'What does Jack finally offer the warrior from his pack?',
         {'A': 'Peanut butter and bread to make a sandwich.', 'B': 'His Africa book.',
          'C': 'Only the honeycomb.', 'D': 'His backpack and notebook.'}, 'A',
         ['How about a peanut butter and honey sandwich?']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie make sandwiches for themselves too?',
         {'A': 'So the warrior doesn’t have to eat alone.', 'B': 'Because they are suddenly very hungry.',
          'C': 'To use up the last of the bread.', 'D': 'To show the warrior how to chew.'}, 'A',
         ['So he doesn’t have to eat alone.']),
        ('VOCABULARY IN CONTEXT', 'The warrior had a “dignified” smile. “Dignified” most nearly means ___.',
         {'A': '庄重而有尊严的', 'B': '害怕紧张的', 'C': '愤怒的', 'D': '滑稽可笑的'}, 'A',
         ['He had a kind, dignified smile.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'They see a bunch of lions sleeping under the tree that holds the tree house.',
          'B': 'The warrior bites into his sandwich.', 'C': 'They eat their sandwiches in silence.',
          'D': 'The warrior vanishes gracefully into the trees.'}, 'A',
         ['they saw a bunch of lions sleeping in the shade of a tree']),
        ('INFERENCE', 'How does the warrior feel about Jack and Annie by the end of the picnic?',
         {'A': 'Friendly—he smiles kindly before leaving in peace.', 'B': 'Angry that they took his honey.',
          'C': 'Frightened of the two children.', 'D': 'Bored and ready to ignore them.'}, 'A',
         ['The warrior smiled. He had a kind, dignified smile.']),
    ],
    9: [
        ('DETAIL', 'According to the book, what do the other animals do while the lions rest after eating?',
         {'A': 'They graze nearby.', 'B': 'They run far away.', 'C': 'They hide up in the trees.',
          'D': 'They attack the sleeping lions.'}, 'A',
         ['the other animals graze nearby.']),
        ('DETAIL', 'What is Jack’s first plan for getting past the lions?',
         {'A': 'To tiptoe very quietly to the rope ladder.', 'B': 'To ride away on a giraffe.',
          'C': 'To wait until it gets dark.', 'D': 'To scare them with monster faces.'}, 'A',
         ['tiptoe to the rope ladder,']),
        ('CAUSE / PURPOSE / RESULT', 'What makes the big lion wake up and finally sit straight up?',
         {'A': 'The hyenas’ sudden high-pitched laughter.', 'B': 'Jack shouting his new plan.',
          'C': 'The giraffe stepping on its tail.', 'D': 'The tree house beginning to spin.'}, 'A',
         ['high-pitched laughter split the air.']),
        ('PLOT RELATION', 'How do Jack and Annie finally reach the rope ladder safely?',
         {'A': 'They walk under a giraffe, moving in the same rhythm, because lions avoid giraffes.',
          'B': 'They simply outrun the lion to the ladder.', 'C': 'The Masai warrior carries them.',
          'D': 'The elephant sprays the lion away.'}, 'A',
         ['Get under that giraffe,']),
        ('INFERENCE', 'Why does Jack’s giraffe plan work?',
         {'A': 'Because lions tend to avoid giraffes, so hiding under one keeps them safe.',
          'B': 'Because giraffes can run faster than lions.', 'C': 'Because the giraffe fights off the lion.',
          'D': 'Because giraffes make the children invisible.'}, 'A',
         ['He remembered something he’d read—lions avoid giraffes.']),
    ],
    10: [
        ('DETAIL', 'What does Annie say was the “true honey” of the trip?',
         {'A': 'The giraffe—sweet and golden, with danger all around it.', 'B': 'The honey from the beehive.',
          'C': 'The jar of peanut butter.', 'D': 'Morgan’s ancient scroll.'}, 'A',
         ['The giraffe was the true honey on that trip,']),
        ('SEQUENCE', 'Which event happens FIRST after they return to the tree house?',
         {'A': 'Jack puts the Africa book with the other books.', 'B': 'They cross their yard and go through the front door.',
          'C': 'They start up their sunny street.', 'D': 'They leave the Frog Creek woods.'}, 'A',
         ['put it with the other books.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie decide to just say they ate their sandwiches on the way home?',
         {'A': 'The real story is far too long and strange to explain to Mom.',
          'B': 'They are not hungry for lunch.', 'C': 'They have lost the sandwiches.',
          'D': 'Their mom already saw the whole trip.'}, 'A',
         ['it’s a really long story,']),
        ('SUMMARY', 'Based on this last chapter, which best summarizes the whole adventure?',
         {'A': 'On an African trip Jack and Annie survived mud, hyenas, and lions, shared a picnic with a Masai warrior, and answered Morgan’s riddle—honey.',
          'B': 'Jack and Annie explored a Wild West ghost town.', 'C': 'Jack and Annie bounced across the moon.',
          'D': 'Jack and Annie tamed a wild mustang.'}, 'A',
         ['a giraffe saved us from a lion.']),
        ('VOCABULARY IN CONTEXT', 'Jack’s heart was still “racing.” Here “racing” means his heart was ___.',
         {'A': '剧烈地快速跳动', 'B': '停止了跳动', 'C': '慢慢平静下来', 'D': '发出很大声响'}, 'A',
         ['His heart was still racing.']),
    ],
}

BOOK_TITLE = 'Lions at Lunchtime'
BOOK_TITLE_CN = '狮口大逃亡'
CHAPTER_TITLES = bt.TITLES


def build_book():
    texts = {c: rb.chapter_text(None, c - 1) for c in range(1, 11)}
    chapters = []
    problems = []
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
            # infer the answer position; distribute A/B/C/D evenly across Book 11.
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
                'id': f'B11C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 11, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 11, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 11] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 11 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
