#!/usr/bin/env python3
"""Author and append the Book 12 (Polar Bears Past Bedtime) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-11.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book12_text as bt
import rebuild_book12 as rb

TARGET = ROOT / 'data' / 'questions.json'

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
        ('DETAIL', 'What was making the “Whoo” sound outside Jack’s window?',
         {'A': 'A white snowy owl.', 'B': 'A pack of wolves.', 'C': 'The howling wind.', 'D': 'Morgan le Fay.'}, 'A',
         ['A white snowy owl was sitting on a tree branch.']),
        ('VOCABULARY IN CONTEXT', 'Morgan is called “the enchantress librarian.” An “enchantress” is a ___.',
         {'A': '女巫；女魔法师', 'B': '图书管理员的学生', 'C': '猎人', 'D': '老师'}, 'A',
         ['Morgan le Fay, the enchantress librarian.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'A snowy owl appears at Jack’s window.', 'B': 'Morgan hands them a fourth scroll.',
          'C': 'They wish to go to the Arctic.', 'D': 'They climb the rope ladder to the tree house.'}, 'A',
         ['A white snowy owl was sitting on a tree branch.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack follow Annie into the dark night even though he feels weird?',
         {'A': 'He doesn’t want to be left behind.', 'B': 'Morgan ordered him to.',
          'C': 'He wants to catch the owl.', 'D': 'He is looking for wolves.'}, 'A',
         ['he didn’t want to be left behind.']),
        ('INFERENCE', 'When Jack asks Morgan “Are you serious?”, he is mainly ___.',
         {'A': 'worried they will freeze in the Arctic', 'B': 'excited to pet a polar bear',
          'C': 'bored by the trip', 'D': 'angry at Annie'}, 'A',
         ['we’ll freeze to death!']),
    ],
    2: [
        ('DETAIL', 'What did Jack and Annie see outside the tree house window in the Arctic?',
         {'A': 'An endless field of ice and snow.', 'B': 'A thick green forest.',
          'C': 'A busy little village.', 'D': 'A warm sandy beach.'}, 'A',
         ['an endless field of ice and snow.']),
        ('VOCABULARY IN CONTEXT', '“Her teeth chattering” tells you that Annie was ___.',
         {'A': '冷得发抖', 'B': '在大声说话', 'C': '在吃东西', 'D': '在大笑'}, 'A',
         ['her teeth chattering.']),
        ('DETAIL', 'According to the book, what does a seal hunter wear to stay warm?',
         {'A': 'Sealskin clothing.', 'B': 'A wool sweater.', 'C': 'A plastic raincoat.', 'D': 'A cotton shirt.'}, 'A',
         ['This seal hunter wears sealskin clothing']),
        ('CAUSE / PURPOSE / RESULT', 'Why are Jack and Annie so anxious as they wait in the tree house?',
         {'A': 'They are freezing and hear wolves howling closer.', 'B': 'They have lost the riddle scroll.',
          'C': 'The tree house is sinking into the snow.', 'D': 'Morgan is angry with them.'}, 'A',
         ['we’ll freeze to death']),
        ('INFERENCE', 'The face that suddenly appears at the window belongs to ___.',
         {'A': 'the seal hunter from the Arctic book', 'B': 'a hungry wolf',
          'C': 'Morgan le Fay', 'D': 'a polar bear'}, 'A',
         ['It was the seal hunter from the Arctic book.']),
    ],
    3: [
        ('DETAIL', 'Why did the seal hunter come to help Jack and Annie?',
         {'A': 'He had a dream that they needed help.', 'B': 'Morgan paid him to.',
          'C': 'He heard them shouting.', 'D': 'He was lost and found them.'}, 'A',
         ['I had a dream']),
        ('VOCABULARY IN CONTEXT', 'The warm hooded coats the hunter gives them are called ___.',
         {'A': 'parkas', 'B': 'masks', 'C': 'scrolls', 'D': 'mittens'}, 'A',
         ['They put the parkas on.']),
        ('DETAIL', 'What were the animals Jack had thought were wolves?',
         {'A': 'Siberian huskies pulling a dogsled.', 'B': 'Hungry polar bears.',
          'C': 'A herd of seals.', 'D': 'Arctic foxes.'}, 'A',
         ['they’re not wolves']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The hunter shouts “Mush!” and the huskies dash off.', 'B': 'Jack and Annie pull on the parkas.',
          'C': 'The hunter hands them fur boots and mittens.', 'D': 'Jack falls onto the snowy ground.'}, 'A',
         ['The huskies dashed off in a whirl of snow.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does the seal hunter give Jack and Annie sealskin clothing?',
         {'A': 'So they will not freeze.', 'B': 'To sell it to them.',
          'C': 'For a costume party.', 'D': 'To hide them from wolves.'}, 'A',
         ['fi-fr-freezing']),
    ],
    4: [
        ('DETAIL', 'What is the small, rounded snow house they stop at called?',
         {'A': 'An igloo.', 'B': 'A tent.', 'C': 'A log cabin.', 'D': 'A cave.'}, 'A',
         ['a small, rounded igloo']),
        ('DETAIL', 'According to the seal hunter, what did the polar bear teach his people to make?',
         {'A': 'Igloos, or snow houses.', 'B': 'Dogsleds.', 'C': 'Fishing nets.', 'D': 'Fire.'}, 'A',
         ['learned to make igloos from polar bears']),
        ('VOCABULARY IN CONTEXT', 'Each mask had a “blunt” nose. “Blunt” means ___.',
         {'A': '钝的；不尖的', 'B': '尖利的', 'C': '彩色的', 'D': '巨大的'}, 'A',
         ['a blunt nose']),
        ('CAUSE / PURPOSE / RESULT', 'Why do the seal hunter’s people always thank the animal spirits?',
         {'A': 'Because the animals help them survive in the ice and snow.',
          'B': 'Because the animals are magical.', 'C': 'Because Morgan told them to.',
          'D': 'Because they are afraid of the animals.'}, 'A',
         ['we always thank the animal spirits']),
        ('INFERENCE', 'When the hunter says polar bears can teach people to fly, Jack believes it is ___.',
         {'A': 'pretend, not a real fact', 'B': 'the best fact of all',
          'C': 'a serious warning', 'D': 'a scientific law'}, 'A',
         ['But I know that’s pretend.']),
    ],
    5: [
        ('DETAIL', 'What two small creatures were the dogs barking at?',
         {'A': 'Polar bear cubs.', 'B': 'Grey wolves.', 'C': 'Baby seals.', 'D': 'Arctic foxes.'}, 'A',
         ['Polar bear babies!']),
        ('DETAIL', 'What game do Jack, Annie, and the cubs end up playing?',
         {'A': 'Tag — “You’re it!”', 'B': 'Hide-and-seek.', 'C': 'A sledding race.', 'D': 'A snowball fight.'}, 'A',
         ['“You’re it!” she said.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack say they are on “thin ice”?',
         {'A': 'The ice keeps making cracking sounds.', 'B': 'The cubs warned them.',
          'C': 'The water feels warm.', 'D': 'The moon has turned orange.'}, 'A',
         ['Another crack rang out.']),
        ('VOCABULARY IN CONTEXT', 'The cubs scooted up a “snowbank.” A “snowbank” is ___.',
         {'A': '雪堆；雪坡', 'B': '一家银行', 'C': '一座冰屋', 'D': '一条河'}, 'A',
         ['scooted up a snowbank']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A giant polar bear appears, snorting, above them.', 'B': 'The cubs pretend to be hurt.',
          'C': 'Jack and Annie slide down the snowbank.', 'D': 'The dogs bark at the two cubs.'}, 'A',
         ['Staring down at them was a giant polar bear.']),
    ],
    6: [
        ('DETAIL', 'How does the mother polar bear cross the thin ice safely?',
         {'A': 'She stretches out her four legs and lies flat to spread her weight.',
          'B': 'She leaps across in one jump.', 'C': 'She swims beneath the ice.',
          'D': 'She tiptoes quickly across.'}, 'A',
         ['the polar bear stretched out her four legs and lay on the ice.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie want to put on the bear masks?',
         {'A': 'So the mother bear might think they are polar bears and to feel protected.',
          'B': 'To keep their faces warm.', 'C': 'To scare the cubs away.', 'D': 'For a ceremony.'}, 'A',
         ['Maybe they’ll protect us']),
        ('VOCABULARY IN CONTEXT', 'The cubs “whimpered.” To “whimper” is to ___.',
         {'A': '呜咽；啜泣', 'B': '哈哈大笑', 'C': '飞快奔跑', 'D': '呼呼大睡'}, 'A',
         ['The cubs whimpered louder.']),
        ('DETAIL', 'How do Jack and Annie finally get across the ice?',
         {'A': 'They copy the bear — spread out flat and push and slide.', 'B': 'They run across quickly.',
          'C': 'The seal hunter carries them.', 'D': 'They swim across.'}, 'A',
         ['Then he copied the bear.']),
        ('INFERENCE', 'When Jack feels “like a flying polar bear,” it shows the hunter’s saying was ___.',
         {'A': 'coming true in a magical way', 'B': 'completely a lie',
          'C': 'a plain scientific fact', 'D': 'a dangerous warning'}, 'A',
         ['He felt like a flying polar bear.']),
    ],
    7: [
        ('DETAIL', 'Once they are safe, how do Jack and Annie thank the polar bear?',
         {'A': 'They bow to her and thank her.', 'B': 'They give her some food.',
          'C': 'They sing her a song.', 'D': 'They quietly run away.'}, 'A',
         ['We thank you, he said, bowing.']),
        ('DETAIL', 'What amazing sight suddenly fills the Arctic sky?',
         {'A': 'The northern lights — a giant swirl of color.', 'B': 'A bright rainbow.',
          'C': 'A sudden snowstorm.', 'D': 'The rising sun.'}, 'A',
         ['the sky exploded.']),
        ('VOCABULARY IN CONTEXT', 'Jack stared at the polar bear “in awe.” “Awe” means ___.',
         {'A': '敬畏；惊叹', 'B': '害怕', 'C': '无聊', 'D': '生气'}, 'A',
         ['Jack stared at the polar bear in awe.']),
        ('PLOT RELATION', 'Annie thinks the lights are the polar bear’s spirit, but Jack believes ___.',
         {'A': 'there is a scientific reason for them', 'B': 'they are dangerous',
          'C': 'Morgan created them', 'D': 'the cubs made them'}, 'A',
         ['There’s got to be a scientific reason']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'All the dancing lights suddenly vanish.', 'B': 'The sky explodes with color.',
          'C': 'Jack and Annie bow to the polar bear.', 'D': 'The bear rises up on her hind legs.'}, 'A',
         ['all the dancing lights were gone']),
    ],
    8: [
        ('DETAIL', 'What brings the seal hunter back to Jack and Annie?',
         {'A': 'The dogsled, with howling huskies, comes into view.', 'B': 'A rescue helicopter.',
          'C': 'Morgan le Fay.', 'D': 'A friendly polar bear.'}, 'A',
         ['the dogsled came into view.']),
        ('CAUSE / PURPOSE / RESULT', 'What had made Jack and Annie feel brave out on the ice?',
         {'A': 'Wearing the bear masks.', 'B': 'Eating the seal meat.',
          'C': 'Watching the northern lights.', 'D': 'The hunter’s song.'}, 'A',
         ['the masks made us brave']),
        ('INFERENCE', 'What is the answer to Morgan’s fourth riddle?',
         {'A': 'A mask.', 'B': 'A polar bear.', 'C': 'The ice.', 'D': 'An igloo.'}, 'A',
         ['“A mask!” Jack and Annie said together.']),
        ('VOCABULARY IN CONTEXT', 'Annie’s words sounded “familiar” to Jack, meaning they ___.',
         {'A': '似曾相识；耳熟', 'B': '很奇怪', 'C': '很好笑', 'D': '听不懂'}, 'A',
         ['Annie’s words sounded familiar.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack give the bear masks back to the seal hunter?',
         {'A': 'They belong to the hunter — Jack had taken them by mistake.', 'B': 'They are broken.',
          'C': 'Annie no longer wants them.', 'D': 'Morgan asked for them.'}, 'A',
         ['The hunter took the masks']),
    ],
    9: [
        ('DETAIL', 'What did Jack find in place of the fourth riddle on the scroll?',
         {'A': 'One shimmering word: MASK.', 'B': 'A blank scroll.', 'C': 'A map of the Arctic.', 'D': 'A drawing of a bear.'}, 'A',
         ['In its place was one shimmering word: MASK']),
        ('DETAIL', 'Why won’t the tree house take them home at first?',
         {'A': 'There is a fifth scroll with a new riddle to solve.', 'B': 'The tree house is broken.',
          'C': 'The snow is too deep.', 'D': 'Morgan has taken the book.'}, 'A',
         ['a fifth scroll']),
        ('VOCABULARY IN CONTEXT', 'Jack says they must “unscramble” the letters — that is, ___.',
         {'A': '把打乱的字母重新排好', 'B': '把字母擦掉', 'C': '大声念出字母', 'D': '把字母藏起来'}, 'A',
         ['unscramble those letters']),
        ('PLOT RELATION', 'The first letters of the four answers are O-E-H-M. What do they spell?',
         {'A': 'HOME, when unscrambled.', 'B': 'MASK.', 'C': 'ICE.', 'D': 'BEAR.'}, 'A',
         ['Or home!']),
        ('CAUSE / PURPOSE / RESULT', 'Why is solving this last riddle so urgent?',
         {'A': 'An icy blizzard is freezing them inside the tree house.', 'B': 'The huskies are running away.',
          'C': 'Morgan is waiting outside.', 'D': 'The cubs are crying.'}, 'A',
         ['Icy winds battered the tree house.']),
    ],
    10: [
        ('DETAIL', 'What does Morgan give Jack and Annie for solving all the riddles?',
         {'A': 'A magic library card for each of them.', 'B': 'A gold coin.',
          'C': 'A polar bear cub.', 'D': 'A brand-new book.'}, 'A',
         ['A magic library card for each of you']),
        ('DETAIL', 'What are Jack and Annie now called?',
         {'A': 'Master Librarians.', 'B': 'Seal hunters.', 'C': 'Arctic knights.', 'D': 'Star explorers.'}, 'A',
         ['These are your Master Librarian cards']),
        ('VOCABULARY IN CONTEXT', 'Morgan speaks in a “soothing” voice. “Soothing” means ___.',
         {'A': '抚慰的；令人安心的', 'B': '很大声的', 'C': '生气的', 'D': '冰冷的'}, 'A',
         ['a soft, soothing voice.']),
        ('PLOT RELATION', 'Annie says the darkness is “like a mask.” How does this echo the riddle?',
         {'A': 'A mask hides the day but brings out your courage — just like the riddle’s answer.',
          'B': 'Masks are frightening in the dark.', 'C': 'The darkness is really a polar bear.',
          'D': 'They lost their masks in the woods.'}, 'A',
         ['It hides the day, but it brings out your courage.']),
        ('SUMMARY', 'Which best summarizes the whole book?',
         {'A': 'In the Arctic Jack and Annie befriend a seal hunter and polar bears, solve the mask riddle, and become Master Librarians.',
          'B': 'Jack and Annie explore an African plain full of lions.',
          'C': 'Jack and Annie visit a Wild West ghost town.',
          'D': 'Jack and Annie dive deep under the ocean.'}, 'A',
         ['You are the newest me']),
    ],
}

BOOK_TITLE = 'Polar Bears Past Bedtime'
BOOK_TITLE_CN = '雪原上的北极熊'
CHAPTER_TITLES = bt.TITLES


def build_book():
    texts = {c: rb.chapter_text(None, c - 1) for c in range(1, 11)}
    chapters, problems = [], []
    for chapter_number in range(1, 11):
        norm_text = re.sub(r'[“”"\']', '', texts[chapter_number])
        questions = []
        for question_number, (tag, stem, options, answer, evidence) in enumerate(CH[chapter_number], start=1):
            standard, skill, dok, difficulty = META[tag]
            for piece in evidence:
                if re.sub(r'[“”"\']', '', piece) not in norm_text:
                    problems.append(f'ch{chapter_number} Q{question_number}: evidence not found: {piece!r}')
            questions.append({
                'number': question_number, 'standard': standard, 'skill': skill, 'dok': dok,
                'stem': stem, 'options': options, 'answer': answer, 'evidence': evidence,
                'rationale': rationale_for(tag, options[answer]),
                'id': f'B12C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 12, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 12, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 12] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 12 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
