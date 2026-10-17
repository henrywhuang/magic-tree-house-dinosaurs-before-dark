#!/usr/bin/env python3
"""Build Book 16 reader JSON (docx-sourced). FIXES = per-chapter OCR-debris
cleanup + narration back-fills; filled after inspecting the first rebuild + audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book

FIXES = {
    0: [  # ch1
        ('said Jack from his bed\n', 'said Jack from his bed.\n'),
        ('pitchblack', 'pitch-black'),
        ('flashlignt', 'flashlight'),
        ('“It certainly is, » said Morgan.', '“It certainly is,” said Morgan.'),
        ('asked Morgan. *TAR', 'asked Morgan.'),
        ('the wisest person you meet,” she said\n', 'the wisest person you meet,” she said.\n'),
        ('said Annic.', 'said Annie.'),
        ('Absolen iv sileni.', 'Absolutely silent.'),
    ],
    1: [  # ch2 — notebook entry on its own line
        ('olive tree —just like Pompeii', 'olive tree—just like Pompeii'),
        ('40, 000 people', '40,000 people'),
        ('Jack wrote in his notebook: Olympiafirst Olympics take place',
         'Jack wrote in his notebook:\nOlympia—first Olympics take place'),
        ('I don’t sec any girls', 'I don’t see any girls'),
        ('He put the book away, “Let’s', 'He put the book away. “Let’s'),
    ],
    2: [  # ch3 — drop the unreadable OCR of the Greek title (not narrated)
        ('“You must be from far away,”', '“You must be from far away.”'),
        ('Frog Creek, Pennsylvania.\nIt’s very far away.“', 'Frog Creek, Pennsylvania. It’s very far away.”'),
        ('he said.\nTIPAZOS\n', 'he said.\n'),
        ('warn you-never tell', 'warn you—never tell'),
        ('must have gon l to the games', 'must have gone to the games'),
    ],
    3: [  # ch4
        ('He put it into his backpack\n', 'He put it into his backpack.\n'),
        ('“I cannot,”she said.', '“I cannot,” she said.'),
        ('It’s not fairnot at all.', 'It’s not fair—not at all.'),
        ('but Plate stopped her', 'but Plato stopped her'),
        ('However..”', 'However...”'),
        ('we should ho home now', 'we should go home now'),
        ('“T’ll go back', '“I’ll go back'),
        ('when you\' ro done', 'when you’re done'),
    ],
    4: [  # ch5 — notebook entries on their own lines
        ('Plato told Jack,\n“the day of the chariot races.”', 'Plato told Jack, “the day of the chariot races.”'),
        ('“It in where our athletes', '“It is where our athletes'),
        ('copy us (iro• eks,” Plato said.', 'copy us Greeks,” Plato said.'),
        ('and wrote: Ancient Greeks invented gyms', 'and wrote:\nAncient Greeks invented gyms'),
        ('And he wrote: Olive tree is sacred Next they passed',
         'And he wrote:\nOlive tree is sacred\nNext they passed'),
        ('Jack quickly wrote: Nike is goddess of victory', 'Jack quickly wrote:\nNike is goddess of victory'),
        ('TAR He took Jack', 'He took Jack'),
        ('came here.” said Plato.', 'came here,” said Plato.'),
        ('promised i• obey', 'promised to obey'),
    ],
    5: [  # ch6 — notebook entries on their own lines
        ('next to the judges.” said Plato.', 'next to the judges,” said Plato.'),
        ('up the steps l their seats', 'up the steps to their seats'),
        ('athletes-the best', 'athletes—the best'),
        ('“The athletes in front are the runners, » said Plato.”Foot races are the oldest event of the Olympics.“',
         '“The athletes in front are the runners,” said Plato. “Foot races are the oldest event of the Olympics.”'),
        ('and wrote: oldest event is foot races', 'and wrote:\noldest event is foot races'),
        ('Jack wrote: boxers wear', 'Jack wrote:\nboxers wear'),
        ('And Jack wrote: wrestlers When Jack', 'And Jack wrote:\nwrestlers\nWhen Jack'),
        ('most of his faco, But', 'most of his face. But'),
        ('This soldior was short-really short.', 'This soldier was short—really short.'),
        ('notebook: some runners race in armor Jack finished',
         'notebook:\nsome runners race in armor\nJack finished'),
    ],
    6: [  # ch7
        ('said Jack.. “Thanks', 'said Jack. “Thanks'),
    ],
    7: [  # ch8
        ('the viewing stand The guards', 'the viewing stand. The guards'),
        ('Jack yelled His voice', 'Jack yelled. His voice'),
        ('for someone or something-to help them', 'for someone—or something—to help them'),
    ],
    8: [  # ch9
        ('the screaming crowd He felt', 'the screaming crowd. He felt'),
        ('Then ho gave her', 'Then he gave her'),
        ('Absolutely still. *THE', 'Absolutely still.'),
    ],
    9: [  # ch10 — OCR scrambled the lines of the closing walk home
        ('the tree ho use.', 'the tree house.'),
        ('“Pegasus, » said Morgan.”He’s the great white winged horse in Greek mythology.“',
         '“Pegasus,” said Morgan. “He’s the great white winged horse in Greek mythology.”'),
        ('found the TER scroll', 'found the scroll'),
        ('They are all here Hercules', 'They are all here—Hercules'),
        ('said Morgan. «The Romans imagined him kneeling in the sky, holding a club over his head.“',
         'said Morgan. “The Romans imagined him kneeling in the sky, holding a club over his head.”'),
        ('TAR She waved her hand again', 'She waved her hand again'),
        ('Jack couldn’t see a thing. ding his way home.\nBut he didn’t ask Annie to turn on the flashlight. '
         'For once, he wasn’t worried about finHe felt as if someone—or something-was leading',
         'Jack couldn’t see a thing.\nBut he didn’t ask Annie to turn on the flashlight. '
         'For once, he wasn’t worried about finding his way home.\nHe felt as if someone—or something—was leading'),
        ('giant wings. somewhere high above.', 'giant wings somewhere high above.'),
    ],
}

if __name__ == '__main__':
    rebuild_docx_book.run(16, FIXES)
