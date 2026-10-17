#!/usr/bin/env python3
"""Build Book 15 reader JSON (docx-sourced). FIXES = per-chapter OCR-debris
cleanup + narration back-fills; filled after inspecting the first rebuild + audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book

FIXES = {
    0: [  # ch1 — page-number debris, the Latin title's dropped drop-cap S
        ('5 A.M.All was quiet.', '5 A.M. All was quiet.'),
        ('“It’s hard to see, » said Jack.', '“It’s hard to see,” said Jack.'),
        ('St i/ i/65 Morgan handed the paper to Jack. On it were the words: erpens Magna The mysterious',
         'Morgan handed the paper to Jack. On it were the words:\nSerpens Magna\nThe mysterious'),
        ('in your darkest hour-”', 'in your darkest hour—”'),
        ('“Don’t worry?” said Annie.', '“Don’t worry,” said Annie.'),
    ],
    1: [  # ch2 — restore the notebook entry and the broken quotes
        ('“What do”civilization\' and \'monks\' mean?“asked Annie.',
         '“What do ‘civilization’ and ‘monks’ mean?” asked Annie.'),
        ('He wrote: brave monks in Ireic Then he looked at Annie. “If we find civilization, l think',
         'He wrote:\nbrave monks in Ireland\nThen he looked at Annie. “If we find civilization, I think'),
        ('said Annic.', 'said Annie.'),
        ('They might he slippery.', 'They might be slippery.'),
        ('It’s 100 dangerous.', 'It’s too dangerous.'),
        ('“Let’s find out, said Annie. She grabbed the rope.”T’ll use it first. Once I’m at the top, you can come after me.“',
         '“Let’s find out,” said Annie. She grabbed the rope. “I’ll use it first. Once I’m at the top, you can come after me.”'),
        ('climbing i 75 up the steps', 'climbing up the steps'),
    ],
    2: [  # ch3
        ('“I-I’m not an invader,” said Jack\n', '“I—I’m not an invader,” said Jack.\n'),
        ('so l could climb', 'so I could climb'),
        ('grahbed', 'grabbed'),
        ('The man looked puzzled “Not many boals can', 'The man looked puzzled. “Not many boats can'),
        ('“The”brother\' means I’m a Christian monk.“', '“The ‘brother’ means I’m a Christian monk.”'),
        ('Master Libraria shined', 'Master Librarian shined'),
        ('bowed hig head', 'bowed his head'),
        ('Viking rais ders', 'Viking raiders'),
        ('to the monk. erpens Magna\n', 'to the monk.\nSerpens Magna\n'),
        ('Morgan lo Fay, » said Annie.', 'Morgan le Fay,” said Annie.'),
        ('the gray sky ahead. *THR', 'the gray sky ahead.'),
    ],
    3: [  # ch4
        ('storytellers-the old women', 'storytellers—the old women'),
        ('worked on it TAR his whole life', 'worked on it his whole life'),
        ('see your work, » said Brother Patrick.', 'see your work,” said Brother Patrick.'),
        ('paintinges', 'paintings'),
        ('The words were: erpens Magna', 'The words were:\nSerpens Magna'),
    ],
    4: [  # ch5 — Jack's two-column notebook lists, restored to the narrated order
        ('completed his work.\nYou will have to return for it.“', 'completed his work. You will have to return for it.”'),
        ('“Oh, shoot, » said Annie.', '“Oh, shoot,” said Annie.'),
        ('how the magic worked Jack shrugged.', 'how the magic worked. Jack shrugged.'),
        ('our sunrise prayers.” said Brother Patrick.', 'our sunrise prayers,” said Brother Patrick.'),
        ('Brother Palrick', 'Brother Patrick'),
        ('He quickly made two lists: To make a book To make paint Sheepskin earth goose quill plants paints',
         'He quickly made two lists:\nTo make a book: sheepskin, goose quill, paints\nTo make paint: earth, plants'),
        ("The birds' cries", 'The birds’ cries'),
    ],
    5: [  # ch6
        ('“I\' 1l come too!”', '“I’ll come too!”'),
        ('down 1o the shore', 'down to the shore'),
        ('Just in case..”', 'Just in case...”'),
    ],
    6: [  # ch7
        ('whispered 10 Annie', 'whispered to Annie'),
        ('fell forward. bumping into Jack', 'fell forward, bumping into Jack'),
        ('in my stupid dress\n', 'in my stupid dress—”\n'),
        ('“We’re got to watch out', '“We’ve got to watch out'),
        ('“I don’t know,» said Jack.', '“I don’t know,” said Jack.'),
        ('whispered Annie. «We need to hide until they go, “whispered Jack.”Then we can look for the tree house.“',
         'whispered Annie.\n“We need to hide until they go,” whispered Jack. “Then we can look for the tree house.”'),
        ('“Come on.\nAnnie!“', '“Come on, Annie!”'),
        ('My dresstoo heavy!', 'My dress—too heavy!'),
        ('“I-lam!”', '“I—I am!”'),
    ],
    7: [  # ch8
        ('I can’t sec the island', 'I can’t see the island'),
        ('as many as thirtytwo.', 'as many as thirty-two.'),
        ('said Annic.', 'said Annie.'),
        ('real people before-people', 'real people before—people'),
        ('He put it on.lt made', 'He put it on. It made'),
    ],
    8: [  # ch9
        ('twostory', 'two-story'),
        ('“No-stay! Help us!”', '“No—stay! Help us!”'),
        ('Jack ducked\n', 'Jack ducked.\n'),
        ('“You can do it!\nGet us to shore before the ship sinks!“',
         '“You can do it! Get us to shore before the ship sinks!”'),
        ('“IWISHWECOULDGOTHERE!”', '“I WISH WE COULD GO THERE!”'),
    ],
    9: [  # ch10
        ('“T’m afraid the story', '“I’m afraid the story'),
        ('be heroes,”she said.', 'be heroes,” she said.'),
        ('said Morgan.“A place', 'said Morgan. “A place'),
        ('Irelandover', 'Ireland over'),
    ],
}

if __name__ == '__main__':
    rebuild_docx_book.run(15, FIXES)
