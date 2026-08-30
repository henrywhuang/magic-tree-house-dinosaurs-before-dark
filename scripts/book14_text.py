#!/usr/bin/env python3
"""Book 14 (Day of the Dragon King) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, 'The Bamboo Book'), (2, 'The Cowherd'), (3, 'The Silk Weaver'), (4, 'The Great Wall'),
            (5, 'The Scholar'), (6, 'The Dragon King'), (7, 'The Burning of the Books'),
            (8, 'The Tomb'), (9, 'The Silk Path'), (10, 'The Ancient Legend')]
_bt = BookText('Day of', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book14_text')
