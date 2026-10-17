#!/usr/bin/env python3
"""Author and append the Book 15 (Viking Ships at Sunrise) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-14.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 15 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book15_text + rebuild_book15
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book15_text as bt
import rebuild_book15 as rb
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
        ('DETAIL', 'According to Morgan, what was life like for people during the Dark Ages?',
         {'A': 'They had to work very hard just to feed and clothe themselves, with little time for play, learning, or art.',
          'B': 'They spent most of their days playing games and making music.',
          'C': 'They lived in rich cities full of libraries and schools.',
          'D': 'They sailed the seas trading gold and jewels.'}, 'A',
         ['People had to work very hard just to feed and clothe themselves.',
          'There was not a lot of time for playing, learning, or making art and music.']),
        ('VOCABULARY IN CONTEXT', 'Morgan says it is a dangerous time, “with Vikings raiding the coasts.” To “raid” means to ___.',
         {'A': '突袭；劫掠', 'B': '保护；守卫', 'C': '打扫；清理', 'D': '建造；修建'}, 'A',
         ['with Vikings raiding the coasts.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan warn Jack and Annie not to ask the ancient story for help too soon?',
         {'A': 'Help comes only at the true darkest hour; if they ask too soon, it will not come.',
          'B': 'The ancient story can only be used once a year.',
          'C': 'Asking too soon would wake the sleeping Vikings.',
          'D': 'Morgan wants them to pay for the help first.'}, 'A',
         ['It must be your darkest hour, when there is no hope left.',
          'If you ask for help too soon, it will not come.']),
        ('INFERENCE', 'Jack is “a little worried about the Vikings” before they leave. This hints that ___',
         {'A': 'the journey to Ireland may be dangerous',
          'B': 'the Vikings will quickly become their friends',
          'C': 'they will never find the tree house',
          'D': 'the trip will be calm and relaxing'}, 'A',
         ['He was a little worried about the Vikings.',
          'it was a very dangerous time, with Vikings raiding the coasts.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The wind blows, the tree house spins, and everything becomes still.',
          'B': 'Morgan hands Jack the paper with the Latin words on it.',
          'C': 'Jack and Annie climb the rope ladder into the tree house.',
          'D': 'Morgan gives Annie the research book about Ireland.'}, 'A',
         ['The tree house started to spin.',
          'Then everything was still.']),
    ],
    2: [
        ('DETAIL', 'What is Jack wearing when he wakes up in the tree house in ancient Ireland?',
         {'A': 'A shirt and trousers of heavy wool, leather slippers, and a leather bag in place of his backpack.',
          'B': 'His own jeans, T-shirt, and sneakers.',
          'C': 'A monk’s brown robe and lace-up sandals.',
          'D': 'A Viking helmet and an iron shield.'}, 'A',
         ['He was wearing a shirt and trousers, made of heavy wool. He also wore leather slippers.',
          'And in place of his backpack was a leather bag.']),
        ('VOCABULARY IN CONTEXT', 'Jack explains what “monks” are. Monks are ___.',
         {'A': '僧侣；修道士', 'B': '海盗；劫匪', 'C': '国王的士兵', 'D': '商人；小贩'}, 'A',
         ['Monks are religious people who spend their time praying and reading and helping people.']),
        ('INFERENCE', 'A thick rope suddenly drops down the stairs. What does Annie decide this means?',
         {'A': 'Someone is secretly trying to help them, just as Morgan once dropped the ladder.',
          'B': 'The Vikings are setting a trap for them.',
          'C': 'The rope fell by accident from a tree.',
          'D': 'They must climb back down to the tree house.'}, 'A',
         ['It’s like when Morgan dropped the ladder to us, said Annie.',
          'I bet someone’s trying to help us.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack want to wait before climbing the steep steps?',
         {'A': 'He wants to wait until the sun comes up so they can see in the mist.',
          'B': 'He is waiting for Brother Patrick to arrive.',
          'C': 'He needs to read the whole research book first.',
          'D': 'He is too tired from the trip to move.'}, 'A',
         ['We better wait till the sun comes up, he said.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'A deep, jolly voice greets Jack at the top of the cliff, calling him a little invader.',
          'B': 'Jack reads that in the Dark Ages learning and culture nearly vanished.',
          'C': 'Annie discovers that the tree house sits on a cliff above the ocean.',
          'D': 'A thick rope drops down the stone steps.'}, 'A',
         ['Aha! boomed a deep, jolly voice.']),
    ],
    3: [
        ('DETAIL', 'Who is the man Jack and Annie meet at the top of the cliff?',
         {'A': 'Brother Patrick, a Christian monk who lives on the island.',
          'B': 'A Viking warrior guarding the coast.',
          'C': 'Brother Michael, the old bookmaker.',
          'D': 'A fisherman sailing home to Frog Creek.'}, 'A',
         ['And I am Brother Patrick.',
          'a Christian monk']),
        ('VOCABULARY IN CONTEXT', 'Brother Patrick first wonders if the children are “invaders.” An “invader” is someone who ___.',
         {'A': '闯入、侵犯别人领地的人（入侵者）', 'B': '在图书馆工作的人',
          'C': '会讲古老故事的人', 'D': '航海很在行的水手'}, 'A',
         ['I did not truly think you were invaders, said Brother Patrick.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Brother Patrick say the monks must be careful of strangers?',
         {'A': 'Because of Viking raiders—when they see the serpent ships, they must hide or be taken as slaves.',
          'B': 'Because strangers might steal their fresh bread.',
          'C': 'Because dangerous wild animals live on the island.',
          'D': 'Because visitors always bring bad weather.'}, 'A',
         ['But on our small island, we are careful of strangers.',
          'When we see their serpent ships, we must hide or be taken as slaves.']),
        ('INFERENCE', 'After Jack shows the Latin words, Brother Patrick gives them “a mysterious look” and changes the subject. This suggests that ___',
         {'A': 'he already knows something about the story they are seeking',
          'B': 'he is unable to read at all',
          'C': 'he is angry that they woke him so early',
          'D': 'he has never once heard of Morgan'}, 'A',
         ['He gave Jack and Annie a mysterious look.',
          'But the monk changed the subject.']),
        ('PLOT RELATION', 'How does Brother Patrick’s attitude change after Jack and Annie show him their secret library cards?',
         {'A': 'He stops treating them as suspicious strangers and warmly welcomes them as friends.',
          'B': 'He becomes frightened and runs away from them.',
          'C': 'He decides they must be Viking spies.',
          'D': 'He refuses to speak to them any longer.'}, 'A',
         ['They both pulled out their secret library cards and showed them to Brother Patrick.',
          'Welcome, my friends, he said.']),
    ],
    4: [
        ('DETAIL', 'Which hut does Brother Patrick call the place of the monks’ most important work?',
         {'A': 'The largest beehive-like hut, their library, where they make books.',
          'B': 'The bakery, where they bake flat bread.',
          'C': 'The hut where they cobble their sandals.',
          'D': 'The vegetable garden by the gate.'}, 'A',
         ['This is where we do our most important work.',
          'This is our library, said Brother Patrick.']),
        ('VOCABULARY IN CONTEXT', 'Brother Patrick says the monks record the old “myths” of Ireland. “Myths” are ___.',
         {'A': '古老的神话、传说故事', 'B': '真实的历史账目',
          'C': '数学与算术题', 'D': '写给国王的信'}, 'A',
         ['We record Christian stories as well as the old myths of Ireland.',
          'the old women who sing the tales of long ago, when people believed in magic.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie shout “Civilization!” when she steps into the library?',
         {'A': 'Because the library full of books and learning is exactly the civilization they came to find.',
          'B': 'Because she sees the Vikings arriving at the gate.',
          'C': 'Because the many candles are far too bright.',
          'D': 'Because Brother Michael calls out her name.'}, 'A',
         ['Civilization! said Annie.',
          'Yes, this is where civilization hides, he said.']),
        ('INFERENCE', 'What can we tell about Brother Michael’s book from the way it is made?',
         {'A': 'It is a precious work of art, made slowly by hand with jewels, sheepskin, quill pens, and homemade paints.',
          'B': 'It was printed quickly by a machine.',
          'C': 'It is a cheap, ordinary notebook.',
          'D': 'It was made long ago by the Vikings.'}, 'A',
         ['Brother Michael showed them the cover of his book. It was decorated with gleaming red and blue jewels.',
          'I write on sheepskin and use goose quill pens, said Brother Michael. My paints are made of earth and plants.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Brother Michael points to a page he is painting, showing the very Latin words Jack and Annie seek.',
          'B': 'Brother Patrick shows the children the warm bakery.',
          'C': 'Annie declares that the library is civilization.',
          'D': 'Brother Michael explains that his paints are made of earth and plants.'}, 'A',
         ['He pointed to the writing at the top of the page.',
          'Serpens Magna']),
    ],
    5: [
        ('DETAIL', 'Why can’t Jack and Annie take the story back to Morgan right away?',
         {'A': 'Brother Michael has not yet finished it, so they will have to return for it later.',
          'B': 'Brother Patrick refuses to hand it over to them.',
          'C': 'The Vikings have already stolen the story.',
          'D': 'The story is written in a language no one can read.'}, 'A',
         ['But alas, Brother Michael has not yet completed his work.',
          'You will have to return for it.']),
        ('VOCABULARY IN CONTEXT', 'Brother Patrick wishes them well on their “voyage” home. A “voyage” is a ___.',
         {'A': '旅程；航行（尤指海上）', 'B': '一顿饭', 'C': '一场梦', 'D': '一本书'}, 'A',
         ['may God be with you on your voyage home.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Brother Patrick tell Jack and Annie they must leave the island right now?',
         {'A': 'The weather is good at the moment, but everything can change in an instant.',
          'B': 'The monks need to use the tree house themselves.',
          'C': 'Breakfast is about to be served in the bakery.',
          'D': 'Morgan is already waiting at the gate for them.'}, 'A',
         ['But you must go now, while the weather is with you, said the monk.',
          'Everything can change in an instant.']),
        ('INFERENCE', 'The gulls circle overhead and their cries “sounded like warnings.” This hints that ___',
         {'A': 'danger is coming to the island',
          'B': 'the birds are simply hungry for breakfast',
          'C': 'a calm day with no trouble is beginning',
          'D': 'the monks are being called to prayers'}, 'A',
         ['Their cries sounded like screams.',
          'They sounded like warnings.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack looks at the horizon and sees Viking ships with blazing serpent prows sailing toward the island.',
          'B': 'Brother Patrick recites, “Shine, O light of the sun.”',
          'C': 'Jack writes two lists in his notebook about making books and paint.',
          'D': 'The monks are called in to their sunrise prayers.'}, 'A',
         ['A ship was outlined against the sky!',
          'Oh, no, Jack whispered. Vikings!']),
    ],
    6: [
        ('DETAIL', 'What do the monks do as soon as they learn the Vikings are coming?',
         {'A': 'Brother Patrick tells them to gather the books and hide, and they run into the library.',
          'B': 'They sail out to fight the Vikings at sea.',
          'C': 'They ring the bell and go back to sleep.',
          'D': 'They hand every book to Jack and Annie.'}, 'A',
         ['Gather the books and hide.',
          'The monks ran into the library.']),
        ('VOCABULARY IN CONTEXT', 'Brother Patrick tells the monks to “make haste.” “Haste” means ___.',
         {'A': '急速；匆忙', 'B': '安静；沉默', 'C': '休息；睡觉', 'D': '快乐；高兴'}, 'A',
         ['Make haste! he said to the other monks.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Brother Patrick tell Jack and Annie NOT to use the stone steps to get down the cliff?',
         {'A': 'Because the Vikings will climb those same steps.',
          'B': 'Because the steps are covered in ice.',
          'C': 'Because the steps lead only to the cave.',
          'D': 'Because Brother Michael is painting on the steps.'}, 'A',
         ['Do not use the steps, Brother Patrick said.',
          'The Vikings will climb them.']),
        ('INFERENCE', 'Why does Brother Michael give Jack and Annie his life’s-work book of Irish tales?',
         {'A': 'So that at least part of the stories will survive, even if the Vikings destroy the rest.',
          'B': 'Because he no longer likes the book.',
          'C': 'Because Morgan ordered him to give it away.',
          'D': 'Because the book is too heavy for him to carry.'}, 'A',
         ['He hobbled over to them, holding out his book of Irish tales.',
          'It is better that the world should have some of it than none at all.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack tucks Brother Michael’s jeweled book into his bag, and they race to the two rocks.',
          'B': 'Annie yanks the bell rope to warn the monks.',
          'C': 'Jack pulls himself up the steep steps with his bare hands.',
          'D': 'Brother Patrick’s rosy face turns white with fear.'}, 'A',
         ['He gently placed the jeweled book in his leather bag.',
          'Then they raced to the rocks that Brother Patrick had told them about.']),
    ],
    7: [
        ('DETAIL', 'What do the Viking warriors look like when Jack and Annie see them through the mist?',
         {'A': 'They have long yellow hair under iron helmets and carry round wooden shields, swords, and axes.',
          'B': 'They wear brown robes like the monks.',
          'C': 'They are short with red hair and carry fishing nets.',
          'D': 'They wear golden crowns and ride horses.'}, 'A',
         ['Their long yellow hair hung down from beneath their iron helmets. They carried round wooden shields and swords and axes.']),
        ('VOCABULARY IN CONTEXT', 'The Viking ships “seemed deserted” as they bobbed in the waves. “Deserted” means ___.',
         {'A': '空无一人的；被弃的', 'B': '拥挤的；满员的', 'C': '崭新的；闪亮的', 'D': '进水的；正在下沉的'}, 'A',
         ['They seemed deserted as they bobbed in the shallow waves.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie decide to hide in one of the Viking ships?',
         {'A': 'The Viking warriors look ready to climb the cliff, so the children need to hide until they leave.',
          'B': 'They want to sail the ship home to Frog Creek.',
          'C': 'They are cold and want to warm up on the ship.',
          'D': 'Brother Patrick told them to wait aboard a ship.'}, 'A',
         ['We need to hide until they go,',
          'They crept back to where the ships were tied.']),
        ('INFERENCE', 'On the ship, “the fog and the movement of the ship made Jack feel as if he was in a dream,” and for a moment he forgot to be scared. This suggests that ___',
         {'A': 'being on the drifting ship felt strangely calm and unreal to him',
          'B': 'Jack had actually fallen fast asleep',
          'C': 'the danger of the Vikings was completely over',
          'D': 'Jack wished he could truly become a Viking'}, 'A',
         ['The fog and the movement of the ship made Jack feel as if he was in a dream.',
          'For a moment, he forgot to be scared of the Vikings.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The anchoring rope goes slack and the Viking ship slides out to sea.',
          'B': 'Annie slips on the steep path and bumps into Jack.',
          'C': 'They spot the serpent prows of the ships through the fog.',
          'D': 'Jack climbs over the low side of the smallest ship.'}, 'A',
         ['Then the rope went slack, and the Viking ship slid out to sea.']),
    ],
    8: [
        ('DETAIL', 'What do Jack and Annie find inside a storage box on the drifting ship?',
         {'A': 'Two small Viking helmets.',
          'B': 'Two wooden rowing oars.',
          'C': 'A map of the island.',
          'D': 'Brother Michael’s paints.'}, 'A',
         ['She lifted out two small Viking helmets.']),
        ('VOCABULARY IN CONTEXT', 'The book says the crew would “row with oars.” “Oars” are ___.',
         {'A': '划船用的桨', 'B': '船上的帆', 'C': '铁头盔', 'D': '储物的箱子'}, 'A',
         ['When there was no wind, the crew would take down the sails and row with oars.']),
        ('CAUSE / PURPOSE / RESULT', 'After reading the book, why does Annie insist that this is NOT yet their darkest hour?',
         {'A': 'Because there is still hope—they could row the ship to the island and find the tree house.',
          'B': 'Because the storm has already passed.',
          'C': 'Because Morgan has come to rescue them.',
          'D': 'Because the Vikings have all given up.'}, 'A',
         ['There’s still hope, said Annie.',
          'We can row to the other side of the island and find the tree house.']),
        ('INFERENCE', 'Why does putting on the Viking helmets matter to Jack and Annie?',
         {'A': 'Wearing the helmets makes them feel braver.',
          'B': 'The helmets keep the rain off their faces.',
          'C': 'The helmets help them see through the fog.',
          'D': 'The helmets make the ship move faster.'}, 'A',
         ['Now I feel like a Viking, too, she said.',
          'He was feeling braver himself.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'As Jack holds up the story and cries for help, a giant sea serpent rises from the wave.',
          'B': 'The strong current rips Jack’s oar out of his hands.',
          'C': 'Annie pulls two small helmets out of a storage box.',
          'D': 'A storm turns the sky black with thunder and lightning.'}, 'A',
         ['Save us, story! he cried.',
          'Rising from the oncoming wave was a giant sea serpent!']),
    ],
    9: [
        ('DETAIL', 'What does the great sea serpent do to help Jack and Annie?',
         {'A': 'It presses its long neck against the back of the ship and pushes it toward the shore.',
          'B': 'It swallows the Viking ship whole.',
          'C': 'It lifts the children onto its back and flies away.',
          'D': 'It builds a bridge of rocks to the island.'}, 'A',
         ['The great serpent was pressing its long neck against the back of the ship, pushing it toward the shore.']),
        ('VOCABULARY IN CONTEXT', 'The serpent’s body was covered with green “scales.” “Scales” are ___.',
         {'A': '（覆盖在蛇、鱼等身上的）鳞片', 'B': '巨大的翅膀', 'C': '锋利的牙齿', 'D': '长长的胡须'}, 'A',
         ['Its green scales were covered with sea slime.',
          'Its scales glittered pink and green in the sunlight.']),
        ('PLOT RELATION', 'How do Jack and Annie react differently when the sea serpent appears?',
         {'A': 'Jack is terrified and shouts for it to go away, while Annie welcomes it and urges it to help them.',
          'B': 'Both of them scream and hide under the sail.',
          'C': 'Both of them attack the serpent with their oars.',
          'D': 'Jack tries to make friends while Annie tries to drive it off.'}, 'A',
         ['Go away! shouted Jack.',
          'Come on! said Annie. You can do it!',
          'Hurry! Annie called to the serpent monster.']),
        ('CAUSE / PURPOSE / RESULT', 'Why do Jack and Annie suddenly rush to climb up to the tree house?',
         {'A': 'Two Vikings have spotted them and are coming down the stairs toward them.',
          'B': 'The sea serpent is chasing them across the shore.',
          'C': 'Brother Patrick is calling them back to the monastery.',
          'D': 'The Viking ship is about to explode.'}, 'A',
         ['Two Vikings were staring down at them!',
          'The Vikings shouted and started down the steep stairs.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The tree house spins away just as the Vikings reach the ledge.',
          'B': 'The serpent pushes the ship onto a sandbar near the shore.',
          'C': 'Jack grabs the Pennsylvania book inside the tree house.',
          'D': 'Annie spots two Vikings at the top of the cliff.'}, 'A',
         ['Just as the Vikings reached the ledge, the wind began to blow.',
          'The tree house started to spin.']),
    ],
    10: [
        ('DETAIL', 'What is the ancient Irish story Jack and Annie brought back about?',
         {'A': 'A great serpent named Sarph, who saved them by pushing their ship over the waves.',
          'B': 'A Viking king who conquered all of Ireland.',
          'C': 'Brother Michael’s daily life at the monastery.',
          'D': 'The very first Olympic games in Greece.'}, 'A',
         ['Sarph was a huge, ugly monster, said Jack.',
          'He saved us by pushing our ship over the stormy waves! Annie said.']),
        ('VOCABULARY IN CONTEXT', 'Morgan is called “the enchantress.” An “enchantress” is a ___.',
         {'A': '女魔法师；女巫', 'B': '女王；公主', 'C': '修女；女僧侣', 'D': '女教师；女向导'}, 'A',
         ['The enchantress sighed. She ran her hand over the sparkling cover.']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Morgan call Jack and Annie “both heroes”?',
         {'A': 'Because of their great courage in bringing the lost book safely back through such danger.',
          'B': 'Because they defeated the Vikings in a battle.',
          'C': 'Because they finished painting Brother Michael’s book.',
          'D': 'Because they built a new library for the monks.'}, 'A',
         ['Thank you also for your great courage, Morgan said.',
          'You are both heroes, too.']),
        ('PLOT RELATION', 'According to Morgan, what do the monster Sarph and the Vikings have in common?',
         {'A': 'Both could be heroes—the “ugly monster” saved the children, and the Vikings later added a lot to civilization.',
          'B': 'Both were completely evil and destroyed all of Ireland.',
          'C': 'Both were invented by Brother Michael.',
          'D': 'Both first came from ancient Greece.'}, 'A',
         ['Sometimes monsters can be heroes,',
          'Oh, most definitely, Vikings could be heroes, too, she said.']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to a monastery on an island off Dark Ages Ireland, find the lost story in the monks’ library, flee a Viking raid, are saved at sea by the serpent Sarph, and carry Brother Michael’s jeweled book safely home to Morgan.',
          'B': 'Jack and Annie explore ancient Pompeii and rescue a scroll as a volcano erupts.',
          'C': 'Jack and Annie sail with real Vikings to raid villages and steal treasure.',
          'D': 'Jack and Annie visit ancient Greece and win the first Olympic games.'}, 'A',
         ['And we brought back the lost book, said Jack.',
          'We found civilization on our trip, said Annie.']),
    ],
}

BOOK_TITLE = 'Viking Ships at Sunrise'
BOOK_TITLE_CN = '维京海盗船'
CHAPTER_TITLES = bt.TITLES


def chapter_text(chapter_index):
    """Rebuild Book 15 chapter text exactly as rebuild_docx_book does."""
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
            # infer the answer position; distribute A/B/C/D evenly across Book 15.
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
                'id': f'B15C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 15, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 15, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 15] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 15 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
