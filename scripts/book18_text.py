#!/usr/bin/env python3
"""Book 18 (Buffalo Before Breakfast) chapter text — docx source (prologue excluded)."""
from docx_book_text import BookText
CHAPTERS = [(1, "Teddy's Back!"), (2, 'Ocean of Grass'), (3, 'Black Hawk'), (4, 'Good Manners'),
            (5, 'Sunlight and Midnight'), (6, 'Stampede!'), (7, 'White Buffalo Woman'),
            (8, 'Sacred Circle'), (9, 'Lakota School'), (10, 'Good Medicine')]
_bt = BookText('Buffalo Before', CHAPTERS)
TITLES = _bt.TITLES
chapter_paragraphs = _bt.chapter_paragraphs
chapter_text = _bt.chapter_text
if __name__ == '__main__':
    _bt.dump('book18_text')
