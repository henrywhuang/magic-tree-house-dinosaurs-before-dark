#!/usr/bin/env python3
"""Book 19 (Tigers at Twilight) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, 'How Far Away?'), (2, 'Kah and Ko'), (3, 'Life or Death'), (4, 'Swing Time'),
            (5, 'Night Walk'), (6, 'Swamp Creature'), (7, 'Trapped!'), (8, 'Wonder Dog'),
            (9, 'The Hermit'), (10, 'Who Are You, Really?')]
_bt = BookText('Tigers at', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book19_text')
