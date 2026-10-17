#!/usr/bin/env python3
"""Build Book 20 reader JSON (docx-sourced, whole-book audio split). FIXES filled after audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import rebuild_docx_book
FIXES = {}
if __name__ == '__main__':
    rebuild_docx_book.run(20, FIXES)
