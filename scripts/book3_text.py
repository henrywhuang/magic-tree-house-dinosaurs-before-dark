#!/usr/bin/env python3
"""Print the clean OCR story text for a Book3 chapter (1-10). For item-writing / scene work."""
import sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'tmp/verify')
import rebuild_book3 as R
from difftext import ocr_chapter_text
ci = int(sys.argv[1]) - 1
pages = R.ocr_pages(2)
print(R.strip_title(R.normalize_rebuild(ocr_chapter_text(2, ci, pages)), ci))
