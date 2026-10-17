#!/usr/bin/env python3
"""Build Book 19 reader JSON (docx-sourced, whole-book audio split). FIXES = OCR-debris cleanup, read-aloud/notebook blocks, scrambled ch10 ending."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book

FIXES = {
    0: [  # ch1 — Morgan's note set as printed lines; page-number debris
        ('Teddy sneezed, as if to say. Of course!', 'Teddy sneezed, as if to say, Of course!'),
        ('read: This little dog is under a spell and needs your help. To free him, you must be given '
         'four special things: A gift from a ship lost at sea, A gift from the prairie blue, '
         'A gift from a forest far away, A gift from a kangaroo.',
         'read:\nThis little dog is under a spell and needs your help. To free him, you must be given '
         'four special things:\nA gift from a ship lost at sea,\nA gift from the prairie blue,\n'
         'A gift from a forest far away,\nA gift from a kangaroo.'),
        ('Morgan Jack touched the first two gifts', 'Morgan\nJack touched the first two gifts'),
        ('\nH1571 A TEE', ''),
    ],
    1: [  # ch2 — dialogue split mid-quote, read-aloud + notebook blocks, stray "on:" from ch3
        ('He’s Jack.\nAnd he’s Teddy. What are your names?“', 'He’s Jack. And he’s Teddy. What are your names?”'),
        ('His name is Ko.\n“Oh, brother,”', 'His name is Ko.”\n“Oh, brother,”'),
        ('the gray monkeys.\nHe read: This monkey is called a langur(say lun-GOOR). The word langur means\n“having a long tail.”',
         'the gray monkeys. He read:\nThis monkey is called a langur (say lun-GOOR). The word langur means “having a long tail.”'),
        ('He wrote: langur means long tail Annie’s laughter', 'He wrote:\nlangur means long tail\nAnnie’s laughter'),
        ('caught up with Annic.', 'caught up with Annie.'),
        ('“\'Wildlife\' means', '“‘Wildlife’ means'),
        ('“What happened there?” he said Annie shrugged', '“What happened there?” he said.\nAnnie shrugged'),
        ('He read aloud: Tigers sharpen', 'He read aloud:\nTigers sharpen'),
        ('just came this way” on:', 'just came this way.”'),
    ],
    2: [  # ch3 — word-halves from the picture page ("wor-/ried.", "any-/thing.", "trunk/move!")
        ('Jack read more: A wild tiger', 'Jack read more:\nA wild tiger'),
        ('said Annie, Jack went Tigers usually', 'said Annie. Jack went on:\nTigers usually'),
        ('began hooting. Kookoo-koo!', 'began hooting. Koo-koo-koo!'),
        ('Jack’s hair stood on end\n', 'Jack’s hair stood on end.\n'),
        ('himself into the tree. ried.', 'himself into the tree.'),
        ('from branch to branch. thing.“', 'from branch to branch.'),
        ('“Maybe the tiger’s gone,” said Annie. move!', '“Maybe the tiger’s gone,” said Annie.'),
        ('Their dark faces looked wor-', 'Their dark faces looked worried.'),
        ('able to see anyKah and Ko hooted again.', 'able to see anything.”\nKah and Ko hooted again.'),
        ('he saw the tree trunk\n', 'he saw the tree trunk move!\n'),
        ('He read aloud: The python', 'He read aloud:\nThe python'),
        ('He read more: To kill', 'He read more:\nTo kill'),
        ('they’re saying, » said Annie.', 'they’re saying,” said Annie.'),
    ],
    3: [  # ch4 — the yell was OCR'd in Cyrillic letters
        ('“АААННН!”', '“AAAHHH!”'),
        ('the langurs\' tree', 'the langurs’ tree'),
    ],
    4: [  # ch5
        ('“But-”', '“But—”'),
        ('let go of the branch. • Then', 'let go of the branch. Then'),
        ('\nTo tal Saba flapped', '\nSaba flapped'),
        ('said Annic sleepily', 'said Annie sleepily'),
        ('dreams-dreams', 'dreams—dreams'),
    ],
    5: [  # ch6 — rhino read-aloud blocks, notebook list, stray "more:" put back after "He read"
        ('Then he rememberedhe was in India, on an elephant’s back! th 5 He sat up.',
         'Then he remembered—he was in India, on an elephant’s back!\nHe sat up.'),
        ('her side-feet first-and fell', 'her side—feet first—and fell'),
        ('Then he looked around Saba had joined', 'Then he looked around. Saba had joined'),
        ('Annie waded into the stream. more:', 'Annie waded into the stream.'),
        ('He read: The one-horned rhinoceros, or“rhino”,', 'He read:\nThe one-horned rhinoceros, or “rhino”,'),
        ('by mistake.A loud-noise will', 'by mistake. A loud noise will'),
        ('he thought. He read The Indian rhino', 'he thought. He read more:\nThe Indian rhino'),
        ('\nTER Jack started', '\nJack started'),
        ('“Whoa!”. • said Annie.', '“Whoa!” said Annie.'),
        ('notebook and wrote: one-horned rhino an endangered animal needs glasses',
         'notebook and wrote:\none-horned rhino\nan endangered animal\nneeds glasses'),
        ('\nHtừ5 103', ''),
    ],
    6: [  # ch7
        ('chapter called“Tiger Traps.” He read: Poachers', 'chapter called “Tiger Traps.” He read:\nPoachers'),
        ('I’II push down', 'I’ll push down'),
        ('she whispered The tiger', 'she whispered.\nThe tiger'),
        ('he started toward them.\nThat', 'he started toward them.'),
    ],
    7: [  # ch8
        ('over to the bank\n', 'over to the bank.\n'),
        ('“Wait-what about Teddy?”', '“Wait—what about Teddy?”'),
        ('Annie said She pulled', 'Annie said. She pulled'),
        ('sounded *TAR worried.', 'sounded worried.'),
        ('again, » said Annie.”Come on.“', 'again,” said Annie. “Come on.”'),
    ],
    8: [  # ch9 — speeches split mid-quote; picture-page debris
        ('“Knock, knock, » Annie', '“Knock, knock,” Annie'),
        ('The blind man smiled\n', 'The blind man smiled.\n'),
        ('alone to think.\nI live in the forest so I can learn from nature.“',
         'alone to think. I live in the forest so I can learn from nature.”'),
        ('one voice-the one great voice', 'one voice—the one great voice'),
        ('large flowers.it came up', 'large flowers. It came up'),
        ('graceful beauty —and his fierce, savage nature.\nYou cannot have one without the other.“',
         'graceful beauty—and his fierce, savage nature. You cannot have one without the other.”'),
        ('“Oh..right,”', '“Oh... right,”'),
        ('friend, » said the blind man.”Our world would not be complete without him.“',
         'friend,” said the blind man. “Our world would not be complete without him.”'),
        ('with Annie. to 121 T tra In the distance', 'with Annie.\nIn the distance'),
    ],
    9: [  # ch10 — the last page's lines were scrambled by OCR; restored in reading order
        ('Annie shrugged\n', 'Annie shrugged.\n'),
        ('“If the Ht5125 traveled all night with the elephants?” of the forest told him.“\n'
         '“Hmm,” said Jack. listened.\n'
         'He heard a woodpecker pecking.\n'
         'He heard crickets chirping.\n'
         'He heard a screen door opening. kids.“the one great voice of home. hermit couldn’t see, '
         'how did he know about the tree house? And how did he know that we had\n'
         '“Easy,” said Annie. “The one great voice He closed his eyes for a moment and '
         'He heard a car going down the street.\n'
         'He heard a mom saying, “Time for dinner, All the sounds were like one great voice',
         '“If the hermit couldn’t see, how did he know about the tree house? And how did he know '
         'that we had traveled all night with the elephants?”\n'
         '“Easy,” said Annie. “The one great voice of the forest told him.”\n'
         '“Hmm,” said Jack.\n'
         'He closed his eyes for a moment and listened.\n'
         'He heard a car going down the street.\n'
         'He heard a woodpecker pecking.\n'
         'He heard crickets chirping.\n'
         'He heard a screen door opening.\n'
         'He heard a mom saying, “Time for dinner, kids.”\n'
         'All the sounds were like one great voice—the one great voice of home.'),
    ],
}

if __name__ == '__main__':
    rebuild_docx_book.run(19, FIXES)
