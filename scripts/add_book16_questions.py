#!/usr/bin/env python3
"""Author and append the Book 16 (Hour of the Olympics) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-13.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 16 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book16_text + rebuild_book16
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book16_text as bt
import rebuild_book16 as rb
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
        ('DETAIL', 'What is the title of the research book Morgan gives Jack and Annie?',
         {'A': 'A Day in Ancient Greece.', 'B': 'The Lost Story of Hercules.',
          'C': 'A Day in Ancient Rome.', 'D': 'Master Librarians of Camelot.'}, 'A',
         ['They read the title: A Day in Ancient Greece.']),
        ('VOCABULARY IN CONTEXT', 'Morgan asks if they are ready for their next “mission.” A “mission” is a ___.',
         {'A': '任务；使命', 'B': '假期；度假', 'C': '游戏；比赛', 'D': '图书馆'}, 'A',
         ['Are you ready for your next mission?']),
        ('CAUSE / PURPOSE / RESULT', 'Why did Jack sleep in his jeans and T-shirt?',
         {'A': 'He didn’t want to waste any time before the trip.',
          'B': 'He was too tired to change into pajamas.',
          'C': 'Annie told him to stay dressed.',
          'D': 'His pajamas were in the wash.'}, 'A',
         ['I didn’t want to waste any time,” said Jack.']),
        ('INFERENCE', 'When Jack asks if this is their last mission, Morgan says, “Ask me that question after this mission.” This suggests that ___.',
         {'A': 'she will only answer once they finish this journey',
          'B': 'she is certain this is their very last mission',
          'C': 'she has forgotten how many missions are left',
          'D': 'she wants them to stop being Master Librarians'}, 'A',
         ['Ask me that question after this mission,” said Morgan.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The tree house starts to spin and everything goes silent.',
          'B': 'Annie hands Jack her secret library card.',
          'C': 'Morgan gives Jack the research book about Greece.',
          'D': 'Jack and Annie climb the rope ladder into the tree house.'}, 'A',
         ['The tree house started to spin.', 'Then everything was silent.']),
    ],
    2: [
        ('DETAIL', 'What does the research book say about how often the Olympic Games took place?',
         {'A': 'Every four years, more than 40,000 people traveled to Olympia.',
          'B': 'Every year, thousands gathered in the city of Athens.',
          'C': 'Once in a lifetime, and only kings could attend.',
          'D': 'Every ten years, in the city of Rome.'}, 'A',
         ['Every four years, more than 40,000 people traveled to Olympia,']),
        ('VOCABULARY IN CONTEXT', 'The book says, “Past the olive grove was a field filled with white tents.” A “grove” is ___.',
         {'A': '树林；（橄榄）树丛', 'B': '河流', 'C': '山洞', 'D': '城墙'}, 'A',
         ['Past the olive grove was a field filled with white tents.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why did men play the women’s parts in Greek plays?',
         {'A': 'Women were not allowed to act, so men played the female roles.',
          'B': 'Women were too busy watching the Olympic Games.',
          'C': 'There were not enough women living in Olympia.',
          'D': 'Women were only allowed to sing in the chorus.'}, 'A',
         ['Women were not allowed to act, so men played the female roles, too.']),
        ('INFERENCE', 'Annie looks for girls, but Jack “only saw men and boys—no women or girls at all.” This hints that in ancient Greece ___.',
         {'A': 'women and girls did not take part in public life like men',
          'B': 'everyone had already gone home for the day',
          'C': 'the girls were all hiding inside the white tents',
          'D': 'the whole town of Olympia was completely empty'}, 'A',
         ['But he only saw men and boys—no women or girls at all.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A man with a short white beard walks toward Jack and Annie.',
          'B': 'Jack reads that the Olympic Games began in ancient Greece.',
          'C': 'Jack and Annie land in an olive tree beside a field of tents.',
          'D': 'Jack sees the actor pull off her wig, revealing a boy.'}, 'A',
         ['A man with a short white beard was walking toward them.']),
    ],
    3: [
        ('VOCABULARY IN CONTEXT', 'Plato says he is a “philosopher,” which he explains as “a lover of wisdom.” A philosopher is someone who ___.',
         {'A': '热爱智慧（的人）；哲学家', 'B': '训练奥运选手的人',
          'C': '建造神庙的人', 'D': '在集市上卖橄榄的人'}, 'A',
         ['I am a philosopher.', 'A lover of wisdom,” said Plato.']),
        ('DETAIL', 'What two letters glittered on Jack and Annie’s secret library cards?',
         {'A': 'The letters M and L, for Master Librarian.',
          'B': 'The letters O and G, for Olympic Games.',
          'C': 'The letters F and C, for Frog Creek.',
          'D': 'The letters P and A, for Pennsylvania.'}, 'A',
         ['The letters M and L that stood for Master Librarian glittered on the cards.']),
        ('PLOT RELATION', 'What is the relationship between Plato and the secret poet?',
         {'A': 'The poet is a friend of Plato’s who wrote a brilliant story.',
          'B': 'The poet is one of Plato’s students at school.',
          'C': 'The poet is a servant who cleans Plato’s courtyard.',
          'D': 'The poet is a stranger Plato has only just met.'}, 'A',
         ['This was written by a brilliant poet—a friend of mine, in fact.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie decide they should show Plato their secret library cards?',
         {'A': 'Because he is a lover of wisdom, the wise kind of person Morgan told them to trust.',
          'B': 'Because Plato demanded to see the cards at once.',
          'C': 'Because they wanted to buy a scroll from him.',
          'D': 'Because the cards would show them the way to the games.'}, 'A',
         ['I think we should show him our cards,” she said in a low voice.',
          'He’s a lover of wisdom.']),
        ('INFERENCE', 'The book says, “Girls were not allowed to go to school.” This helps explain why ___.',
         {'A': 'a girl who could read and write would be very unusual in ancient Greece',
          'B': 'the boys of Olympia disliked going to school',
          'C': 'the courtyard of the house was empty that day',
          'D': 'Plato himself was unable to read the poet’s story'}, 'A',
         ['Girls were not allowed to go to school.']),
    ],
    4: [
        ('DETAIL', 'How did the young poet learn to read and write?',
         {'A': 'She taught herself.', 'B': 'Plato taught her at his school.',
          'C': 'Her mother taught her at home.', 'D': 'She learned it at the Olympic Games.'}, 'A',
         ['I taught myself,” the woman answered.']),
        ('VOCABULARY IN CONTEXT', 'The poet says her story can be called the work of “Anonymous.” Plato explains that “anonymous” means ___.',
         {'A': '匿名的；没有人知道是谁写的', 'B': '非常有名的',
          'C': '写得很糟糕的', 'D': '用希腊语写的'}, 'A',
         ['No, anonymous means that no one knows who wrote it,” said Plato.']),
        ('CAUSE / PURPOSE / RESULT', 'Why must Jack and Annie take the poet’s story back to their faraway home?',
         {'A': 'Because the poet will get in trouble if the story is read in her own land.',
          'B': 'Because the story is far too long to read in Greece.',
          'C': 'Because Morgan already keeps a copy of it in Greece.',
          'D': 'Because the poet plans to move to Frog Creek herself.'}, 'A',
         ['But she will get in trouble if it is read in our land. You must take it back to your faraway home, where it will be safe.']),
        ('INFERENCE', 'Plato says his country is a democracy that believes in “freedom for our citizens,” but “right now that only means men.” We can infer that ___.',
         {'A': 'women were not treated as full citizens with the same freedoms',
          'B': 'everyone, including women, already had equal rights',
          'C': 'only the children of Olympia were truly free',
          'D': 'the democracy had no rules or laws at all'}, 'A',
         ['My country is a democracy. We believe in freedom for our citizens. But I’m afraid right now that only means men.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack joins Plato and heads toward the Olympic grounds.',
          'B': 'The poet hands Jack her scroll to carry home.',
          'C': 'Plato explains what the word “Anonymous” means.',
          'D': 'Annie decides to go back to the outdoor theater.'}, 'A',
         ['He and Jack turned and joined the crowd heading toward the Olympic grounds.']),
    ],
    5: [
        ('DETAIL', 'What did Plato say the winners of the games would wear?',
         {'A': 'Crowns made from the branches of the sacred olive tree.',
          'B': 'Golden helmets shaped like the head of Zeus.',
          'C': 'Purple capes like the ones the actors wore.',
          'D': 'Bronze medals earned in the gymnasium.'}, 'A',
         ['The olive tree is our sacred tree,', 'The winners of the games will wear crowns made from its branches.']),
        ('VOCABULARY IN CONTEXT', 'Plato calls the olive tree “our sacred tree.” Here “sacred” means ___.',
         {'A': '神圣的；供奉神灵的', 'B': '普通的；平常的', 'C': '枯死的', 'D': '高大的'}, 'A',
         ['The olive tree is our sacred tree,” he said.']),
        ('INFERENCE', 'The statue of Zeus was “at least two stories high,” and Jack “felt very small.” This suggests that ___.',
         {'A': 'the Greeks built the statue huge to show how powerful they believed Zeus was',
          'B': 'Jack was actually shrinking smaller and smaller',
          'C': 'the temple was really too small for any visitors',
          'D': 'Zeus was a living giant who lived in the temple'}, 'A',
         ['The statue was at least two stories high.', 'Jack felt very small.']),
        ('CAUSE / PURPOSE / RESULT', 'Why had all the athletes come to the temple of Zeus the day before?',
         {'A': 'To swear to Zeus that they had trained for ten months and to promise to obey the rules.',
          'B': 'To pay money so they could enter the chariot race.',
          'C': 'To choose which sacred olive tree to cut down.',
          'D': 'To watch a play performed at the outdoor theater.'}, 'A',
         ['Yesterday all the athletes came here,', 'They swore to Zeus that they had trained for ten months.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Trumpets sound and Plato says the Olympic parade is beginning.',
          'B': 'Plato shows Jack the giant statue inside the temple of Zeus.',
          'C': 'Jack writes in his notebook that the olive tree is sacred.',
          'D': 'They pass the statue of Nike, the goddess of victory.'}, 'A',
         ['The hour has come,” said Plato.', 'The Olympic parade begins!']),
    ],
    6: [
        ('VOCABULARY IN CONTEXT', 'Plato says, “Foot races are the oldest event of the Olympics.” An “event” here is ___.',
         {'A': '（运动会的）比赛项目', 'B': '观众席', 'C': '奖牌', 'D': '神庙'}, 'A',
         ['Foot races are the oldest event of the Olympics.']),
        ('DETAIL', 'What did Plato say the boxers were wearing?',
         {'A': 'Special gloves and bronze helmets.',
          'B': 'Long capes and lace-up sandals.',
          'C': 'Olive crowns and full armor.',
          'D': 'Purple tunics and wigs.'}, 'A',
         ['boxers wear gloves and helmets']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack keep studying the short soldier at the sidelines?',
         {'A': 'Because something about the soldier seems strange, and the soldier keeps looking back at him.',
          'B': 'Because the soldier is about to race in the chariots.',
          'C': 'Because Plato told Jack to keep an eye on the soldier.',
          'D': 'Because the soldier is holding Jack’s lost notebook.'}, 'A',
         ['But something was strange.', 'He was still studying the short soldier, who seemed to be looking back at him.']),
        ('INFERENCE', 'The short soldier “was dressed like the actor from the outdoor theater.” This is a clue that ___.',
         {'A': 'Annie got her soldier costume from the theater she went back to',
          'B': 'the real actor had left the stage to join the army',
          'C': 'Plato was the one hiding under the disguise',
          'D': 'all the soldiers came from the theater each day'}, 'A',
         ['The soldier was dressed like the actor from the outdoor theater.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack realizes that the short soldier is really Annie.',
          'B': 'Plato leads Jack to the seats next to the judges.',
          'C': 'The runners and boxers march past in the parade.',
          'D': 'Plato explains that the men in armor race in full armor.'}, 'A',
         ['The short soldier was Annie.']),
    ],
    7: [
        ('VOCABULARY IN CONTEXT', 'People stared at the small soldier with the “high-pitched voice.” A “high-pitched” voice is ___.',
         {'A': '尖细的；音调很高的', 'B': '低沉的', 'C': '沙哑的', 'D': '很轻、几乎听不见的'}, 'A',
         ['A few people began staring at the strange small soldier with the high-pitched voice.']),
        ('DETAIL', 'How many horses pulled each chariot in the race?',
         {'A': 'Four horses.', 'B': 'Two horses.', 'C': 'Six horses.', 'D': 'One horse.'}, 'A',
         ['Each chariot was pulled by four horses.']),
        ('PLOT RELATION', 'When Jack shouts, “It’s not a joke!”, why does Plato misunderstand him?',
         {'A': 'Plato thinks Jack means the games are serious, not that Annie is in danger.',
          'B': 'Plato cannot hear Jack at all over the roaring crowd.',
          'C': 'Plato already knows that Annie is the short soldier.',
          'D': 'Plato thinks Jack is asking to race in the chariots.'}, 'A',
         ['Of course not,” said Plato.', 'We take the games very seriously.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack suddenly decide he has to leave the games right away?',
         {'A': 'He has to get Annie away before she gets into terrible trouble.',
          'B': 'He is bored by the long chariot race.',
          'C': 'Plato has asked him to go home now.',
          'D': 'He wants to find the young poet again.'}, 'A',
         ['He had to get Annie away before it was too late!']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Two big guards reach Annie first.',
          'B': 'The trumpet sounds and the horses take off.',
          'C': 'Annie pulls off her helmet and her pigtails fly up.',
          'D': 'Someone in the crowd shouts for the guards.'}, 'A',
         ['But two big guards got to Annie first.']),
    ],
    8: [
        ('VOCABULARY IN CONTEXT', 'The crowd shouted, “Arrest her! Arrest her!” To “arrest” someone means to ___.',
         {'A': '逮捕；抓起来', 'B': '欢迎；迎接', 'C': '表扬；夸奖', 'D': '帮助；救助'}, 'A',
         ['The crowd began to shout.', 'Arrest her! Arrest her!']),
        ('DETAIL', 'What does Jack promise the guard as he tries to save Annie?',
         {'A': 'That he will take her home.',
          'B': 'That he will pay a large fine.',
          'C': 'That he will race in the chariots.',
          'D': 'That he will never return to Olympia.'}, 'A',
         ['I promise I’ll take her home!']),
        ('INFERENCE', 'When Annie cries, “Jack! The story!”, Jack understands that ___.',
         {'A': 'this is their darkest hour, when only the lost story can save them',
          'B': 'he should read the Greek story aloud to the crowd',
          'C': 'he must hand the poet’s story over to the guards',
          'D': 'Annie wants to hear the story read to her right now'}, 'A',
         ['This is definitely our darkest hour!']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack hold the poet’s scroll up to the sky?',
         {'A': 'He is begging the lost story to save Annie.',
          'B': 'He wants the crowd to read the Greek words on it.',
          'C': 'He is trying to show the story to Plato in the stands.',
          'D': 'He wants to keep the scroll safe from the dust.'}, 'A',
         ['He held the story up to the sky.', 'Save Annie!” he shouted.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A huge white horse gallops out of the dust straight toward Jack.',
          'B': 'The guards try to pull Annie away from the race.',
          'C': 'Jack holds the scroll up and shouts, “Save Annie!”',
          'D': 'The crowd begins to shout, “Arrest her!”'}, 'A',
         ['All heads turned to watch as a huge white horse galloped out of the dust.',
          'And he was galloping straight toward Jack.']),
    ],
    9: [
        ('VOCABULARY IN CONTEXT', 'When its wheels bumped onto the grass, the winged horse “coasted to the ground.” To “coast” here means to ___.',
         {'A': '滑行；平稳地落下', 'B': '猛烈地坠落', 'C': '快速地起飞', 'D': '原地打转'}, 'A',
         ['Finally, the winged horse coasted to the ground near the olive grove.']),
        ('DETAIL', 'What amazing thing happened to the white horse in the sky?',
         {'A': 'It grew giant feathery wings and pulled the chariot into the sky.',
          'B': 'It turned into a shining golden statue.',
          'C': 'It changed into the young poet.',
          'D': 'It vanished into a cloud of dust.'}, 'A',
         ['The white horse had grown giant feathery wings and was pulling their chariot into the sky.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie have to leave the beautiful white horse behind?',
         {'A': 'They have to go before the guards find them.',
          'B': 'The horse is too tired to carry them any farther.',
          'C': 'Morgan has ordered them to leave the horse.',
          'D': 'The horse really belongs to Plato.'}, 'A',
         ['Come on, Annie. We have to go before they find us,” said Jack.']),
        ('INFERENCE', 'Annie’s “eyes filled with tears” and “a tear rolled down her cheek” as the horse flew away. This shows that Annie ___.',
         {'A': 'had come to love the horse and was sad to say good-bye',
          'B': 'was frightened of the huge white horse',
          'C': 'was glad the horse was finally gone',
          'D': 'had dust in her eyes from the chariot race'}, 'A',
         ['Her eyes filled with tears.', 'A tear rolled down her cheek.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The tree house spins and everything becomes still.',
          'B': 'The winged horse coasts to the ground near the olive grove.',
          'C': 'Annie strokes the horse’s neck and whispers, “Thank you.”',
          'D': 'The white horse disappears behind the clouds.'}, 'A',
         ['The tree house began to spin.', 'Then everything was still.']),
    ],
    10: [
        ('VOCABULARY IN CONTEXT', 'Morgan says the heroes became “constellations” in the night sky. A “constellation” is ___.',
         {'A': '星座（由一组星星组成的图案）', 'B': '一片云', 'C': '一道闪电', 'D': '一轮明月'}, 'A',
         ['Hercules is a constellation,” said Morgan.']),
        ('DETAIL', 'Who is Pegasus, according to Morgan?',
         {'A': 'The great white winged horse in Greek mythology.',
          'B': 'The chief god of the ancient Greeks.',
          'C': 'A famous Greek poet and thinker.',
          'D': 'The goddess of victory.'}, 'A',
         ['He’s the great white winged horse in Greek mythology.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan say Jack and Annie can still see Pegasus and their other story friends?',
         {'A': 'In the night sky, the old story characters appear as stars.',
          'B': 'The characters are hiding among the dark trees.',
          'C': 'Morgan painted their pictures on the tree house wall.',
          'D': 'The characters followed them home all the way from Greece.'}, 'A',
         ['Look up,” said Morgan. “Your friends are in the night sky. They are stars.']),
        ('PLOT RELATION', 'How are Jack and Annie’s four missions tied together at the end of the book?',
         {'A': 'The heroes from all four rescued stories now appear together as constellations in the sky.',
          'B': 'All four of the stories turn out to have been written by Plato.',
          'C': 'All four heroes come home to live with them in Frog Creek.',
          'D': 'The four stories are all lost again in the night sky.'}, 'A',
         ['In the night, you can see all the story characters that saved you on your last four missions,” said Morgan.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to the ancient Olympics, meet Plato, rescue a secret poet’s story, are carried to safety by the winged horse Pegasus, and bring the story home to Morgan.',
          'B': 'Jack and Annie explore a Roman town and barely escape an erupting volcano.',
          'C': 'Jack and Annie sail the wild seas hunting for buried pirate treasure.',
          'D': 'Jack and Annie visit the frozen Arctic and make friends with polar bears.'}, 'A',
         ['You were very lucky to be bringing me the story of Pegasus.',
          'Plato helped us find it,” said Jack.']),
    ],
}

BOOK_TITLE = 'Hour of the Olympics'
BOOK_TITLE_CN = '古希腊奥运会'
CHAPTER_TITLES = bt.TITLES


def chapter_text(chapter_index):
    """Rebuild Book 16 chapter text exactly as rebuild_docx_book does."""
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
            # infer the answer position; distribute A/B/C/D evenly across Book 16.
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
                'id': f'B16C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 16, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 16, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 16] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 16 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
