#!/usr/bin/env python3
"""Validate a book's content module: every SCENE_ANCHOR must occur verbatim in
its chapter text and every VOCABULARY word must resolve in that chapter.
Usage: validate_content.py <book_number>"""
import importlib
import re
import sys

sys.path.insert(0, 'scripts')
sys.path.insert(0, 'tmp/verify')
import rekey

book = int(sys.argv[1])
T = importlib.import_module(f'book{book}_text')
C = importlib.import_module(f'book{book}_content')


def strip(s):
    return re.sub(r'[“”"\'’]', '', s)


ok = True
for ci in range(10):
    paras = T.chapter_paragraphs(ci)
    toks = [m.group() for p in paras for m in re.finditer(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", p)]
    for ai, anc in enumerate(C.SCENE_ANCHORS[ci]):
        if not any(strip(anc) in strip(p) for p in paras):
            print(f'CH{ci + 1} ANCHOR{ai + 1} NOT FOUND: {anc[:48]!r}')
            ok = False
    std, ext = C.VOCABULARY[ci]
    for v in std + ext:
        if rekey.find_first(toks, v, set(), exact_only=False) < 0:
            print(f'CH{ci + 1} VOCAB NOT FOUND: {v!r}')
            ok = False
    if len(C.SCENES[ci]) != 3:
        print(f'CH{ci + 1} SCENES != 3')
        ok = False
print('ALL OK' if ok else 'ISSUES FOUND')
sys.exit(0 if ok else 1)
