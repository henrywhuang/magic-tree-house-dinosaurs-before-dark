#!/usr/bin/env python3
"""Book 17 (Tonight on the Titanic) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, 'A New Mission'), (2, 'The Unsinkable Ship'), (3, 'SOS'), (4, 'Put on Your Life Belts!'),
            (5, 'William and Lucy'), (6, 'Women and Children First'), (7, 'The Gift'),
            (8, 'Every Man for Himself'), (9, 'Time Stops'), (10, 'A Touch of Magic')]
_bt = BookText('Tonight On', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book17_text')
