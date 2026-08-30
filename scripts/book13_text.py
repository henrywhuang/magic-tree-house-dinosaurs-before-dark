#!/usr/bin/env python3
"""Book 13 (Vacation Under the Volcano) chapter text — docx source, no prologue."""
from docx_book_text import BookText
CHAPTERS = [(1, 'A Secret Code'), (2, 'The End Is Near'), (3, 'Gladiators!'), (4, 'Scary Things'),
            (5, 'Books? Books?'), (6, 'The End Is Here'), (7, 'The Sky Is Falling'),
            (8, 'Nightmare at Noon'), (9, 'Save Us!'), (10, 'A Simple Explanation')]
_bt = BookText('Vacation Under', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book13_text')
