#!/usr/bin/env python3
"""Build Book 13 reader JSON (docx-sourced). FIXES = per-chapter OCR-debris
cleanup + narration back-fills; filled after inspecting the first rebuild + audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book

FIXES = {
    0: [  # ch1 — dialogue punctuation + the Latin title printed as an image
        ('mission for you,” sho said.', 'mission for you,” she said.'),
        ('“Well, there have been many great libraries lost in history, » said Morgan.”And with them, we have lost many wonderful stories.“',
         '“Well, there have been many great libraries lost in history,” said Morgan. '
         '“And with them, we have lost many wonderful stories.”'),
        ('“It is,” said Morgan. “But luckily, with the help of the tree house and you two Master Librarians, some of those stories can be saved.\n'
         'Such as this one“Morgan showed them the piece of paper.',
         '“It is,” said Morgan. “But luckily, with the help of the tree house and you two Master Librarians, '
         'some of those stories can be saved. Such as this one—”\nMorgan showed them the piece of paper.'),
        ('There was strange writing on it:',
         'There was strange writing on it:\nVir Fortissimus in Mundo.'),
        ('I almost forgot-I’m', 'I almost forgot—I’m'),
        ('Look at US.', 'Look at us.'),
        ('There it was-the magic tree house.', 'There it was—the magic tree house.'),
    ],
    1: [  # ch2 — restore the printed fact box + two handwritten notebook entries
        ('“I wonder where we are, » said Jack. He opened the book about Roman times. He read aloud: '
         'Almost 2, 000 years ago, on August, A. D. 79, the seaside town of Pompeii (pom-PAY) was a typical '
         'Roman town. Many Romans went there on their vacation. They built large houses called villas and '
         'planted groves of olive trees along the slopes of a mountain called Mount Vesuvius '
         '(vuh-SOO-vee-us) Annie kept looking out the window as Jack pulled out his notebook and pencil. '
         'He wrote: Jack looked out the window again.',
         '“I wonder where we are,” said Jack. He opened the book about Roman times. He read aloud:\n'
         'Almost 2,000 years ago, on August 24, A.D. 79, the seaside town of Pompeii (pom-PAY) was a typical '
         'Roman town. Many Romans went there on their vacation. They built large houses called villas and '
         'planted groves of olive trees along the slopes of a mountain called Mount Vesuvius '
         '(vuh-SOO-vee-us).\nAnnie kept looking out the window as Jack pulled out his notebook and pencil. He wrote:\n'
         'Vacation in Pompeii. August 24, A.D. 79. Houses called villas.\nJack looked out the window again.'),
        ('And that mountain must be Mount Vesuvius.“', '“And that mountain must be Mount Vesuvius.”'),
        ('Jack frowned.“I think', 'Jack frowned. “I think'),
        ('when he stepped onto the ground Annie', 'when he stepped onto the ground. Annie'),
        ('teenagers talked and laughed They', 'teenagers talked and laughed. They'),
        ('said Annie. smiling.', 'said Annie, smiling.'),
        ('He pulled out his notebook. He wrote:',
         'He pulled out his notebook. He wrote:\nForum: center of town.'),
    ],
    2: [  # ch3
        ('looked nuts to me.” said Jack.', 'looked nuts to me,” said Jack.'),
        ('“That sounds like going to the pool,” said!\nAnnie.',
         '“That sounds like going to the pool,” said Annie.'),
        ('gods and goddesses“myths.”', 'gods and goddesses “myths.”'),
        ('said Annie.“I like', 'said Annie. “I like'),
        ('“Right,” said Annie. “Come on, hurry.\nLet’s keep looking.“',
         '“Right,” said Annie. “Come on, hurry. Let’s keep looking.”'),
    ],
    3: [  # ch4
        ('“There’re more scary things.', '“There are more scary things.'),
    ],
    4: [  # ch5
        ('“This must be the dining room, » said Jack.',
         '“This must be the dining room,” said Jack.'),
        ('“Aha!” said Jack.. “That’s a library of scroIs!',
         '“Aha!” said Jack. “That’s a library of scrolls!'),
    ],
    5: [  # ch6 — Latin title was an image; remaining fixes are OCR confusions
        ('Jack pulled out the piece of paper with the Latin title on it:',
         'Jack pulled out the piece of paper with the Latin title on it:\nVir Fortissimus in Mundo.'),
        ('said Annic.', 'said Annie.'),
        ('lo0king for', 'looking for'),
        ('August 24, A. D. 79-that\' that’s today!', 'August 24, A.D. 79—that’s today!'),
        ('volcano —at noon!', 'volcano—at noon!'),
        ('I don’tknow', 'I don’t know'),
    ],
    6: [  # ch7
        ('around them pots, plants, the mermaid fountain.',
         'around them—pots, plants, the mermaid fountain.'),
        ('“I’ll check--”', '“I’ll check—”'),
        ('called pumice(PUM-iss)', 'called pumice (PUM-iss)'),
        ('fallen rooftiles', 'fallen roof tiles'),
    ],
    7: [  # ch8
        ('In the forum, everyoneshoppers, soldiers, gladiators, fruit sellers—was running',
         'In the forum, everyone—shoppers, soldiers, gladiators, fruit sellers—was running'),
    ],
    8: [  # ch9
        ('looked like a gladiator-but even bigger', 'looked like a gladiator—but even bigger'),
    ],
    9: [  # ch10 — opening paragraphs were interleaved by OCR
        ('Jack didn’t move. He and never been so tired', 'Jack didn’t move. He had never been so tired'),
        ('The first thing he saw was his backpack. The white tunics and lace-up sandals were gone. '
         'So were their pillow hats and the leather bag. and his lases on his shit, a voice came from '
         'Jack let out a long, deep breath. As he clebehind him. “I’m very glad to see you safe and sound.”',
         'The first thing he saw was his backpack. The white tunics and lace-up sandals were gone. '
         'So were their pillow hats and the leather bag.\nJack let out a long, deep breath. '
         'As he cleaned his glasses on his shirt, a voice came from behind him. '
         '“I’m very glad to see you safe and sound.”'),
        ('“It-it was pretty scary,”', '“It—it was pretty scary,”'),
        ('The Strongest Man in the WorId', 'The Strongest Man in the World'),
        ('save us-and Hercules', 'save us—and Hercules'),
        ('“I don’t know...”', '“I don’t know...”'),
        ('“Yeah,” said Jack..', '“Yeah,” said Jack.'),
        ('home--and a restful vacation.', 'home—and a restful vacation.'),
        ('What is that story about-the one we just rescued?',
         'What is that story about—the one we just rescued?'),
    ],
}

if __name__ == '__main__':
    rebuild_docx_book.run(13, FIXES)
