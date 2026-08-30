#!/usr/bin/env python3
"""Build Book 14 reader JSON (docx-sourced). FIXES = per-chapter OCR-debris
cleanup + narration back-fills; filled after inspecting the first rebuild + audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book

FIXES = {
    0: [  # ch1 — OCR confusions and punctuation
        ('“T have mine in my pocket,”', '“I have mine in my pocket,”'),
        ('The letters MI. on it', 'The letters ML on it'),
        ('winked al them', 'winked at them'),
        ('fur wasn’t quite', 'fun wasn’t quite'),
        ('we aren’t pretending', 'we weren’t pretending'),
        ('Brids sang', 'Birds sang'),
        ('Jack smiled.He', 'Jack smiled. He'),
        ('Master Librarians?* she asked.', 'Master Librarians?” she asked.'),
        ('On the cover was the title: The Time of the First Emperor:',
         'On the cover was the title: The Time of the First Emperor.'),
    ],
    1: [  # ch2 — restore the handwritten notebook entry
        ('sectet library card', 'secret library card'),
        ('T shirts, and sneakers', 'T-shirts, and sneakers'),
        ('straw shoes. and round hats', 'straw shoes, and round hats'),
        ('Over 2, 000 years ago', 'Over 2,000 years ago'),
        ('Jack pulled out his notebook and wrote:',
         'Jack pulled out his notebook and wrote:\nFirst emperor called Dragon King.'),
        ('palace is in that city” Jack looked up.',
         'palace is in that city.” Jack looked up.'),
        ('stood in their path.He', 'stood in their path. He'),
        ('“Wait, excuse me said Jack.”Do you know where we can find the Imperial Library?“',
         '“Wait, excuse me—” said Jack. “Do you know where we can find the Imperial Library?”'),
        ('“Oh, I-I just wondered,”', '“Oh, I—I just wondered,”'),
    ],
    2: [  # ch3
        ('“Okay,” he said. “But let’s find her fast.\nAnd remember to keep your head down so no one will notice us.“',
         '“Okay,” he said. “But let’s find her fast. And remember to keep your head down so no one will notice us.”'),
        ('field ill twilight', 'field at twilight'),
        ('gave Annic a shy smile', 'gave Annie a shy smile'),
        ('a basker near her loom', 'a basket near her loom'),
        ('The making of silk is China’s most valuable secret.\nAnyone who steals the secret will be arrested.\nThe Dragon King will have him put to death.“',
         'The making of silk is China’s most valuable secret. Anyone who steals the secret will be arrested. '
         'The Dragon King will have him put to death.”'),
    ],
    3: [  # ch4
        ('stecring the oxcart', 'steering the oxcart'),
        ('get into the city”', 'get into the city.”'),
        ('feet —lots of feet', 'feet—lots of feet'),
        ('Annie pecked out', 'Annie peeked out'),
        ('3, 700 miles', '3,700 miles'),
        ('“We -uh—”', '“We—uh—”'),
    ],
    4: [  # ch5
        ('But later, in the future.“', 'But later, in the future.”'),
        ('asked sofily', 'asked softly'),
        ('The scholar nodded\n', 'The scholar nodded.\n'),
        ('“Indeed it is! the scholar said quietly.', '“Indeed it is!” the scholar said quietly.'),
        ('said Jack, He held out', 'said Jack. He held out'),
        ('something 1 believe in', 'something I believe in'),
        ('said Annic.', 'said Annie.'),
        ('*I have never met ones so honored who were so young.“',
         '“I have never met ones so honored who were so young.”'),
    ],
    5: [  # ch6
        ('wagon wheels. silk cloth', 'wagon wheels, silk cloth'),
        ('his burial tomb.“', 'his burial tomb.”'),
        ('Jack whirled around\n', 'Jack whirled around.\n'),
        ('at once -the Dragon King', 'at once—the Dragon King'),
    ],
    6: [  # ch7 — restore the sentence ending lost at a page break
        ('“T’ll get it!”', '“I’ll get it!”'),
        ('“This is a burial tomb, remember? It’s\n“Let’s just take a quick look,”',
         '“This is a burial tomb, remember? It’s creepy.”\n“Let’s just take a quick look,”'),
        ('soldiers— thousands of them', 'soldiers—thousands of them'),
    ],
    7: [  # ch8 — restore fact-box and handwritten notebook text
        ('“It’s amazing,” Jack said Annie nodded.', '“It’s amazing,” Jack said. Annie nodded.'),
        ('The Dragon King had 7, 000 lifesize elay figures made for his burial tomb.',
         'The Dragon King had 7,000 life-size clay figures made for his burial tomb.'),
        ('Then, kneeling on the brick floor, he wrote:',
         'Then, kneeling on the brick floor, he wrote:\nNo two faces the same, not even the horses.'),
        ('“T’d better look this up,”', '“I’d better look this up,”'),
        ('said. “Save us!”', 'said, “Save us!”'),
        ('Jack felt faint. *I—I guess we’ll just have -have to\n“Look!” Annie said.',
         'Jack felt faint. “I—I guess we’ll just have—have to—”\n“Look!” Annie said.'),
        ('The ball of thread! It rolled out of your sack!“she said.',
         '“The ball of thread! It rolled out of your sack!” she said.'),
    ],
    8: [  # ch9
        ('“What what now?”', '“What—what now?”'),
        ('said Annie. *I guess those weren’t the same stairs that we went down.“',
         'said Annie. “I guess those weren’t the same stairs that we went down.”'),
        ('gong sounded, It was', 'gong sounded. It was'),
        ('rich houses.. past the poor houses', 'rich houses... past the poor houses'),
        ('“Let’s-go-home,”', '“Let’s—go—home,”'),
        ('found each other”', 'found each other.”'),
    ],
    9: [  # ch10 — OCR interleaved the final printed page
        ('said Annic.', 'said Annie.'),
        ('“I’m afraid it was a very dangerous time, she said.”For Viking raiders often attacked the seacoasts. “',
         '“I’m afraid it was a very dangerous time,” she said. “For Viking raiders often attacked the seacoasts.”'),
        ('He’d had cnough danger', 'He’d had enough danger'),
        ('“Jack! Annie!” came a voice. were just plain old cricket sounds again.\n'
         '“Coming!” Jack shouted. across their yard. mom asked. were saved by an ancient book.“\n'
         '“Yep!” said Jack and Annie.\nAnd they followed her inside.\n'
         'It was their mother calling them.\n'
         'The spell was broken. The cricket stories Jack and Annie ran down their street and\n'
         '“Did you have a good time in China?” their\n'
         '“It was pretty scary,” said Annie.\n'
         '“We got lost in a tomb,” said Jack. “But we Their mom smiled and shook her head.”My, books are wonderful, aren’t they?“she said.',
         '“Jack! Annie!” came a voice.\n'
         'It was their mother calling them.\n'
         'The spell was broken. The cricket stories were just plain old cricket sounds again.\n'
         '“Coming!” Jack shouted.\n'
         'Jack and Annie ran down their street and across their yard.\n'
         '“Did you have a good time in China?” their mom asked.\n'
         '“It was pretty scary,” said Annie.\n'
         '“We got lost in a tomb,” said Jack. “But we were saved by an ancient book.”\n'
         'Their mom smiled and shook her head. “My, books are wonderful, aren’t they?” she said.\n'
         '“Yep!” said Jack and Annie.\n'
         'And they followed her inside.'),
    ],
}

if __name__ == '__main__':
    rebuild_docx_book.run(14, FIXES)
