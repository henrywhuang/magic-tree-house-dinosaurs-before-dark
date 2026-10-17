#!/usr/bin/env python3
"""Build Book 18 reader JSON (docx-sourced, whole-book audio split). FIXES = OCR-debris cleanup + notes/lists restored, audited against the audiobook ASR."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book
FIXES = {
    0: [  # ch1 — debris, Morgan's note laid out as printed
        ('she said.\n“And Grandmother will', 'she said. “And Grandmother will'),
        ('\nEP#28K 71 Ter', ''),
        ('read it aloud: This little dog', 'read it aloud:\nThis little dog'),
        ('needs your help. To free him', 'needs your help.\nTo free him'),
        ('special things: A gift', 'special things:\nA gift'),
        (', A gift from', ',\nA gift from'),
        ('\nE#$P73', ''),
        ('“Yeah, » said Jack.', '“Yeah,” said Jack.'),
        ('2:20the time', '2:20—the time'),
    ],
    1: [  # ch2 — debris, Jack's (OCR-garbled) notebook entry
        ('\nEP#$377', ''),
        ('quickly wrote: east inno', 'quickly wrote:\nGreat Plains—lots of land'),
        ('ocean of grass, » Annie called', 'ocean of grass,” Annie called'),
        ('he sneezed\n', 'he sneezed.\n'),
        ('\nEP#788279', ''),
    ],
    2: [  # ch3 — debris, read-aloud passages + notebook entry on their own lines
        ('He read: In the early 1800s', 'He read:\nIn the early 1800s'),
        ('and wrote: early 1800s-Lakota were largest tribe of Great Plains Behind',
         'and wrote:\nearly 1800s—Lakota were largest tribe of Great Plains\nBehind'),
        ('Jack read: Everything changed', 'Jack read:\nEverything changed'),
        ('in the mid0s', 'in the mid-1800s'),
        ('settlers, » said Jack.', 'settlers,” said Jack.'),
        ('said Black Ep $782 Hawk.\n“I live with my grandmother”', 'said Black Hawk. “I live with my grandmother.”'),
        ('On one page, he read: Good', 'On one page, he read:\nGood'),
        ('On another page, he read: The Lakota', 'On another page, he read:\nThe Lakota'),
        ('information was: Holding up two fingers means\n“friend”.',
         'information was:\nHolding up two fingers means “friend.”'),
        ('all about EP## 8P$ 87 their', 'all about their'),
        ("means 'friend'.”", 'means ‘friend.’”'),
        ('Annie nodded\n', 'Annie nodded.\n'),
    ],
    3: [  # ch4 — debris, notebook entry, Jack's buffalo list
        ('She walked Title tall', 'She walked tall'),
        ('They Black Hawk led them', 'Then Black Hawk led them'),
        ('two fingers for\n“friend”.', 'two fingers for “friend.”'),
        ('They *THE all seemed', 'They all seemed'),
        ('porcupine quiIls', 'porcupine quills'),
        ('and wrote: Sow bear claws to shirt', 'and wrote:\nSew bear claws to shirt'),
        ('said Black Hawk.\n“Wait.”', 'said Black Hawk. “Wait.”'),
        ('“Food from his body.\nTepees from his skin, tools from his bones.“',
         '“Food from his body. Tepees from his skin, tools from his bones.”'),
        ('from his ribs.”: # 00P5 *TER Jack finished his list. buffalo skin-tepee bones-tools horns-cups hair-ropes ribs-sleds',
         'from his ribs.”\nJack finished his list.\nbuffalo\nskin—tepee\nbones—tools\nhorns—cups\nhair—ropes\nribs—sleds'),
    ],
    4: [  # ch5
        ('THE The fierce wolf', 'The fierce wolf'),
        ('said Black Hawk.\n“When I wear', 'said Black Hawk. “When I wear'),
        ('she said,\n“and grip', 'she said, “and grip'),
        ('“Wait-wait!”', '“Wait—wait!”'),
        ('on onc foot', 'on one foot'),
    ],
    5: [  # ch6
        ('“Wow,”whispered', '“Wow,” whispered'),
        ('Tic read to himself', 'He read to himself'),
        ('“bison”. At', '“bison.” At'),
        ('grownEP #* 8P$ 103 ups', 'grown-ups'),
        ('wanted to shoul,', 'wanted to shout,'),
        ('EP ##8K|105 A ripple', 'A ripple'),
        ('buffalo-calm buffalo', 'buffalo—calm buffalo'),
    ],
    6: [  # ch7
        ('said Annic.\n“and I got', 'said Annie, “and I got'),
        ("shouted. 'Stop!' Then", 'shouted. ‘Stop!’ Then'),
        ('Annie asked him.\n“Did you see', 'Annie asked him. “Did you see'),
        ('said Jack.\n“You mean like a ghost', 'said Jack. “You mean like a ghost'),
        ('turned his pony around\n', 'turned his pony around.\n'),
        ('they took off Behind them', 'they took off. Behind them'),
    ],
    7: [  # ch8
        ('to EP # $8฿5|113 the camp', 'to the camp'),
        ('to show off.\nShowing off made you', 'to show off. Showing off made you'),
        ('Everything is related.“', 'Everything is related.”'),
        ('“Me too, » said Annie.', '“Me too,” said Annie.'),
        ('in our circle,” said.\nGrandmother.', 'in our circle,” said Grandmother.'),
        ('said Grandmother.\n“It is the source', 'said Grandmother. “It is the source'),
        ('can be seen.\nSometimes not.“', 'can be seen. Sometimes not.”'),
        ('Grandmother said: She pulled', 'Grandmother said. She pulled'),
        ('prairic blue', 'prairie blue'),
        ('said Grandmother.\n“You can leave', 'said Grandmother. “You can leave'),
    ],
    8: [  # ch9 — debris, notebook entries, trailing TAR
        ('he asked.\n“Even when you', 'he asked. “Even when you'),
        ('in his notebook: land owned', 'in his notebook:\nland owned'),
        ('Jack explained Black Hawk laughed again.', 'Jack explained.\nBlack Hawk laughed again.'),
        ('Jack wrote: Lakota school is everywhere Grandmother turned',
         'Jack wrote:\nLakota school is everywhere\nGrandmother turned'),
        ('he said,\n“toward the sunrise', 'he said, “toward the sunrise'),
        ('Rides-LikeWind', 'Rides-Like-Wind'),
        ('two fingers for\n“friend”. Then', 'two fingers for “friend.” Then'),
        ('grass...all the way', 'grass... all the way'),
        ('EP#$8B$125 Annie put', 'Annie put'),
        ('Absolutely still.\nTAR', 'Absolutely still.'),
    ],
    9: [  # ch10 — scrambled closing lines restored (true last words: "grandmother's arms.")
        ('White Buffalo Woman,” she said\n', 'White Buffalo Woman,” she said.\n'),
        ('“Hmm..” said', '“Hmm...” said'),
        ('“Well..” said', '“Well...” said'),
        ('we turend our', 'we turned our'),
        ('Branches waved their leaves. the blue sky. thought. All things are related.',
         'Branches waved their leaves. Birds left the branches and swooped up into the blue sky.\n'
         'Black Hawk’s grandmother is right, he thought. All things are related.'),
        ('catch up with her. grandmother’s arms.\nBirds left the branches and swooped up into '
         'Black Hawk’s grandmother is right, he Together they ran out of the Frog Creek woods... '
         'up their street... and into their own',
         'catch up with her.\nTogether they ran out of the Frog Creek woods... up their street... '
         'and into their own grandmother’s arms.'),
    ],
}
if __name__ == '__main__':
    rebuild_docx_book.run(18, FIXES)
