#!/usr/bin/env python3
"""Book 16 (Hour of the Olympics) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, 'Just One More'), (2, 'Any Girls Here?'), (3, 'The Secret Poet'), (4, 'Not Fair!'),
            (5, 'Hi, Zeus'), (6, 'Mystery Man'), (7, 'Go! Go! Go!'), (8, 'Save Annie!'),
            (9, 'Fly Away Home'), (10, "They're All Here")]
_bt = BookText('Hour of', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book16_text')
