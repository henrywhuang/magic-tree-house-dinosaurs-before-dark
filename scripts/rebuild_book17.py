#!/usr/bin/env python3
"""Build Book 17 reader JSON (docx-sourced, whole-book audio split). FIXES = OCR-debris cleanup + notes/signs restored, audited against the audiobook ASR."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book
FIXES = {
    0: [  # ch1 — debris, Morgan's note laid out as printed
        ('E*9“Jack followed.', 'Jack followed.'),
        ('Annic shined', 'Annie shined'),
        ('that said: This little dog', 'that said:\nThis little dog'),
        ('needs your help. To free him', 'needs your help.\nTo free him'),
        ('special things: A gift', 'special things:\nA gift'),
        (', A gift from', ',\nA gift from'),
        ('Morgan P. S. Your', 'Morgan\nP.S. Your'),
        ('said Jack.\n“The ship won’t sink', 'said Jack. “The ship won’t sink'),
        ('he said. *TAR The wind', 'he said.\nThe wind'),
    ],
    1: [  # ch2 — debris, read-aloud passage, notebook entry, life-preserver sign
        ('“Arf! Arf!?”', '“Arf! Arf!”'),
        ('cold— very cold', 'cold—very cold'),
        ('old*TAR fashioned', 'old-fashioned'),
        ("lookouts' nest", 'lookouts’ nest'),
        ('he said He turned', 'he said. He turned'),
        ('he read: Late at night', 'he read:\nLate at night'),
        ('2, 200 passengers', '2,200 passengers'),
        ('“Oh, man, we’re in in” said Jack. He pulled out his notebook and wrote: April 14.1912',
         '“Oh, man, we’re in 1912,” said Jack. He pulled out his notebook and wrote:\nApril 14, 1912'),
        ('window —just', 'window—just'),
        ('read TAR more', 'read more'),
        ('“Hey-don’t', '“Hey—don’t'),
        ('the words: R.M.S.TITANIC *THE', 'the words:\nR.M.S. TITANIC'),
    ],
    2: [  # ch3
        ('lost ship-a safer one', 'lost ship—a safer one'),
        ('said Annie.\n“We can escape', 'said Annie. “We can escape'),
        ('ship hit something” Annie and Jack', 'ship hit something.”\nAnnie and Jack'),
        ('on the ship Jack looked', 'on the ship. Jack looked'),
        ('“Yes, Captain, » said', '“Yes, Captain,” said'),
        ('Annie whispered Jack shook his head.', 'Annie whispered.\nJack shook his head.'),
        ('quietly to Annie: After the Titanic hit the iceberg at:40 P.M.',
         'quietly to Annie:\nAfter the Titanic hit the iceberg at 11:40 P.M.'),
        ("“That' 's terrible", '“That’s terrible'),
        ('“I don’t know, » said Annie.', '“I don’t know,” said Annie.'),
        ('and wrote: *TER SOS sent out Titanic sinks at 2:20 A.M.',
         'and wrote:\nSOS sent out\nTitanic sinks at 2:20 A.M.'),
        ('Annic turned', 'Annie turned'),
        ('she whispered.\n“Everyone can', 'she whispered. “Everyone can'),
        ('the book again: On the Titanic', 'the book again:\nOn the Titanic'),
        ('Many thirdclass', 'Many third-class'),
        ('his notebook: Need twice', 'his notebook:\nNeed twice'),
        ('cabins thin way', 'cabins this way'),
    ],
    3: [  # ch4
        ('said Annie.\n“The floor’s', 'said Annie. “The floor’s'),
        ('a woman asked\n', 'a woman asked.\n'),
        ('dark coats, They', 'dark coats. They'),
        ('“Iknow,”', '“I know,”'),
        ('cabin doors. *TAR The doors', 'cabin doors. The doors'),
        ('said Jack.. “Maybe wo should', 'said Jack. “Maybe we should'),
    ],
    4: [  # ch5
        ('“I’m Annie, » said Annie.”And this is my brother, Jack.“',
         '“I’m Annie,” said Annie. “And this is my brother, Jack.”'),
        ('“Wait-can Teddy', '“Wait—can Teddy'),
        ('have time” started Jack', 'have time—” started Jack'),
    ],
    5: [  # ch6
        ('take all night.\nThere’s plenty of time for everyone on board to be rescued.“',
         'take all night. There’s plenty of time for everyone on board to be rescued.”'),
        ('“Indeed Many ships', '“Indeed. Many ships'),
        ('soothing voice.\n“There’s nothing', 'soothing voice. “There’s nothing'),
        ('Lucy turned to Jack. *TAR', 'Lucy turned to Jack.'),
        ('thirdclass deck', 'third-class deck'),
        ('no one hero seemed', 'no one here seemed'),
    ],
    6: [  # ch7
        ('“Very soon, » said Jack.', '“Very soon,” said Jack.'),
        ('said Jack.\n“You and William', 'said Jack. “You and William'),
        ('said Annie.\n“For your brother’s', 'said Annie. “For your brother’s'),
        ('“Goodbye, William.”', '“Good-bye, William.”'),
        ('she said.\n“It’s our father’s', 'she said. “It’s our father’s'),
        ('as Annic disappeared', 'as Annie disappeared'),
    ],
    7: [  # ch8
        ('came a loud voice.\n“Wait for me!”', 'came a loud voice. “Wait for me!”'),
        ('the uniformed man called.\n“Bring', 'the uniformed man called. “Bring'),
        ('out to Annic.', 'out to Annie.'),
        ('she shouted.\n“Thank you for your gift', 'she shouted. “Thank you for your gift'),
    ],
    8: [  # ch9
        ('coming from $0E*31|117 the ship', 'coming from the ship'),
        ('forward —all', 'forward—all'),
        ('the thirdclass corridor', 'the third-class corridor'),
        ('shouted Jack.\n“We’ll fall off', 'shouted Jack. “We’ll fall off'),
    ],
    9: [  # ch10 — debris + the scrambled closing lines put back in narration order
        ('said Jack. • “How did you', 'said Jack. “How did you'),
        ('she said.\n“Let’s put Teddy', 'she said. “Let’s put Teddy'),
        ('different ending” Jack nodded. That was exactly how he felt.\n'
         'E*310127 the memory of the sinking ship.\nThey had come home.\n“Good-bye.”\n'
         'Staring at the starry sky, he shuddered at He knew that he and Annie were lucky.\n'
         '“Good night, Titanic,” he said softly.',
         'different ending.”\nJack nodded. That was exactly how he felt.\n'
         'Staring at the starry sky, he shuddered at the memory of the sinking ship. '
         'He knew that he and Annie were lucky.\nThey had come home.\n'
         '“Good night, Titanic,” he said softly. “Good-bye.”'),
    ],
}
if __name__ == '__main__':
    rebuild_docx_book.run(17, FIXES)
