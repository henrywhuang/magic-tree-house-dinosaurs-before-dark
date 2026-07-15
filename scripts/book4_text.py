#!/usr/bin/env python3
"""Print the clean OCR story text for a Book3 chapter (1-10). For item-writing / scene work."""
import sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'tmp/verify')
import rebuild_book4 as R
from difftext import ocr_chapter_text
ci = int(sys.argv[1]) - 1
pages = R.ocr_pages(3)
print(R.strip_title(R.normalize_rebuild(ocr_chapter_text(3, ci, pages)), ci))
