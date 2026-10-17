#!/usr/bin/env python3
"""Book 15 (Viking Ships at Sunrise) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, 'Before Dawn'), (2, 'The Steep Climb'), (3, 'Brother Patrick'), (4, 'Books of Wonder'),
            (5, 'Warships on the Waves'), (6, 'The Vikings Are Coming!'), (7, 'Fogbound'),
            (8, 'Lost at Sea'), (9, 'Sea Monster!'), (10, 'Sunrise')]
_bt = BookText('Viking', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book15_text')
