#!/usr/bin/env python3
"""Rebuild Book1 chapter data from the ORIGINAL OCR text (authoritative American book text),
timed by faster-whisper ASR word timestamps, preserving scenes + page structure + keyword highlights.

Text source : 1勇闯恐龙谷.pdf_by_PaddleOCR-VL-1.6.json  (via tmp/verify/difftext.ocr_chapter_text)
Timing source: tmp/asr/chXX.json  (faster-whisper large-v3 word timestamps)
Output       : tmp/rebuilt/chapter-XX.json  (staging; copy to data/ after proofread)
"""
import sys, re, json, difflib
sys.path.insert(0, 'tmp/verify')
from difftext import ocr_chapter_text, ocr_pages, normalize
from extract_final import chapter_vocab
import rekey  # find_first / find_phrase / norm for keyword matching

TITLES = ['into the woods','the monster','where is here','henry','gold in the grass',
          'dinosaur valley','ready set go','a giant shadow','the amazing ride','home before dark']

def norm_match(w):
    return re.sub(r'[^a-z]', '', w.lower())

def normalize_rebuild(t):
    """Light normalization that PRESERVES em-dashes and curly quotes (unlike difftext.normalize,
    which merged em-dash -> hyphen and thus joined 'wings—and' into one token). Also repairs a few
    OCR word-splits of proper nouns and line-break hyphenation."""
    t = t.replace('…', '...')
    for a, b in [('Anato- sauruses', 'Anatosauruses'), ('Anato sauruses', 'Anatosauruses'),
                 ('Anato saurus', 'Anatosaurus'), ('Tyranno saurus', 'Tyrannosaurus'),
                 ('Pteran odon', 'Pteranodon'), ('Trice ratops', 'Triceratops')]:
        t = t.replace(a, b)
    t = re.sub(r'([A-Za-z])-\n([a-z])', r'\1-\2', t)   # join line-broken hyphenated compounds (keep hyphen)
    return t

def strip_title(text, ci):
    lines = [ln for ln in text.split('\n')]
    out, dropping = [], True
    for ln in lines:
        s = ln.strip()
        if dropping:
            key = norm_match(s)
            if not key:
                continue
            if re.match(r'^chapter\d+$', key) or key == norm_match(TITLES[ci]) or key == 'chapter'+norm_match(TITLES[ci]):
                continue
            # also drop a bare "chapter" or roman/number-only line
            if key in ('chapter',) or re.match(r'^chapter(one|two|three|four|five|six|seven|eight|nine|ten)$', key):
                continue
            dropping = False
        out.append(ln)
    return '\n'.join(out)

def tokenize_paragraph(para):
    """Return list of {word, before, after} preserving punctuation/spacing like the app schema."""
    toks = list(re.finditer(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", para))
    words, pos = [], 0
    for m in toks:
        s, e = m.start(), m.end()
        before = para[pos:s]
        j = e
        while j < len(para) and not para[j].isspace() and not para[j].isalnum():
            j += 1
        after = para[e:j]
        words.append({'word': m.group(), 'before': before, 'after': after})
        pos = j
    return words

def build_ocr_words(ci, pages):
    text = strip_title(normalize_rebuild(ocr_chapter_text(0, ci, pages)), ci)
    paras = [ln for ln in text.split('\n') if ln.strip()]
    words = []
    for pi, para in enumerate(paras):
        for w in tokenize_paragraph(para):
            w['para'] = pi
            words.append(w)
    return words, len(paras)

def assign_timestamps(ocr_words, asr_words):
    """Align OCR words to ASR words; transfer ASR start/end; interpolate the rest."""
    ow = [norm_match(w['word']) for w in ocr_words]
    aw = [norm_match(w['word']) for w in asr_words]
    for w in ocr_words:
        w['start'] = None; w['end'] = None
    sm = difflib.SequenceMatcher(None, ow, aw, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                a = asr_words[j1 + k]
                ocr_words[i1 + k]['start'] = float(a['start'])
                ocr_words[i1 + k]['end'] = float(a['end'])
    # interpolate missing (None) timestamps between anchors
    n = len(ocr_words)
    # find first/last anchors
    anchored = [i for i in range(n) if ocr_words[i]['start'] is not None]
    if not anchored:
        raise RuntimeError('no alignment anchors!')
    first, last = anchored[0], anchored[-1]
    # leading
    for i in range(first):
        ocr_words[i]['start'] = max(0.0, ocr_words[first]['start'] - (first - i) * 0.28)
        ocr_words[i]['end'] = ocr_words[i]['start'] + 0.26
    # trailing
    for i in range(last + 1, n):
        ocr_words[i]['start'] = ocr_words[last]['end'] + (i - last - 1) * 0.30
        ocr_words[i]['end'] = ocr_words[i]['start'] + 0.28
    # middle gaps
    i = first
    while i <= last:
        if ocr_words[i]['start'] is not None:
            i += 1; continue
        p = i - 1
        q = i
        while q <= last and ocr_words[q]['start'] is None:
            q += 1
        t0 = ocr_words[p]['end']; t1 = ocr_words[q]['start']
        gap = max(0.0, t1 - t0); m = q - i
        for k in range(m):
            s = t0 + gap * (k + 1) / (m + 1)
            ocr_words[i + k]['start'] = round(s, 3)
            ocr_words[i + k]['end'] = round(min(t1, s + gap / (m + 1)), 3)
        i = q
    # enforce monotonic start
    for i in range(1, n):
        if ocr_words[i]['start'] < ocr_words[i-1]['start']:
            ocr_words[i]['start'] = ocr_words[i-1]['start']
            if ocr_words[i]['end'] < ocr_words[i]['start']:
                ocr_words[i]['end'] = ocr_words[i]['start'] + 0.1
    for w in ocr_words:
        w['start'] = round(w['start'], 3); w['end'] = round(w['end'], 3)

def old_page_bounds(ci):
    d = json.load(open(f'data/chapter-{ci+1:02d}.json'))
    bounds = []
    for page in d['pages']:
        pw = [w for para in page for w in para.get('words', [])]
        bounds.append(pw[0]['start'] if pw else None)
    bounds = [b for b in bounds if b is not None]
    return d.get('scenes', []), bounds, d.get('chapter')

def assign_pages(ocr_words, num_paras, bounds):
    """Assign each paragraph to a page by the time of its first word; page count = len(bounds)."""
    npages = len(bounds)
    # first word time per paragraph
    para_time = {}
    for w in ocr_words:
        para_time.setdefault(w['para'], w['start'])
    def page_of(t):
        pg = 0
        for k in range(npages):
            if t >= bounds[k]:
                pg = k
        return pg
    para_page = {pi: page_of(para_time[pi]) for pi in range(num_paras) if pi in para_time}
    # enforce non-decreasing page across paragraphs (reading order)
    cur = 0
    for pi in range(num_paras):
        if pi not in para_page:
            para_page[pi] = cur; continue
        cur = max(cur, para_page[pi]); para_page[pi] = cur
    for w in ocr_words:
        w['page'] = para_page[w['para']]

def apply_keywords(ocr_words, ci, pages):
    kb, tz = chapter_vocab(0, ci, pages)
    vocab = kb + tz
    tokens = [w['word'] for w in ocr_words]
    used = set()
    singles = [v for v in vocab if ' ' not in v]
    phrases = [v for v in vocab if ' ' in v]
    for V in phrases:
        idxs = rekey.find_phrase(tokens, V, used); used.update(idxs)
    rest = []
    for V in singles:
        k = rekey.find_first(tokens, V, used, exact_only=True)
        if k >= 0: used.add(k)
        else: rest.append(V)
    for V in rest:
        k = rekey.find_first(tokens, V, used, exact_only=False)
        if k >= 0: used.add(k)
    for i, w in enumerate(ocr_words):
        w['key'] = i in used

def build_chapter(ci, pages):
    ocr_words, num_paras = build_ocr_words(ci, pages)
    asr = json.load(open(f'tmp/asr/ch{ci+1:02d}.json'))
    assign_timestamps(ocr_words, asr['words'])
    scenes, bounds, chapter_val = old_page_bounds(ci)
    assign_pages(ocr_words, num_paras, bounds)
    apply_keywords(ocr_words, ci, pages)
    # finalize word dicts + build pages
    flat = []
    for i, w in enumerate(ocr_words):
        flat.append({'i': i, 'word': w['word'], 'before': w['before'], 'after': w['after'],
                     'start': w['start'], 'end': w['end'], 'key': w['key'], 'page': w['page']})
    npages = len(bounds)
    pages_out = []
    for pg in range(npages):
        pg_words = [w for w in flat if w['page'] == pg]
        # group by original paragraph
        paras = {}
        for w, ow in zip([x for x in flat if x['page']==pg], [o for o,f in zip(ocr_words,flat) if f['page']==pg]):
            paras.setdefault(ow['para'], []).append(w)
        page_paras = [{'words': paras[k]} for k in sorted(paras)]
        pages_out.append(page_paras)
    return {'chapter': chapter_val, 'scenes': scenes, 'words': flat, 'pages': pages_out}

if __name__ == '__main__':
    import os
    os.makedirs('tmp/rebuilt', exist_ok=True)
    pages = ocr_pages(0)
    chapters = [int(a)-1 for a in sys.argv[1:]] if len(sys.argv) > 1 else list(range(10))
    for ci in chapters:
        d = build_chapter(ci, pages)
        json.dump(d, open(f'tmp/rebuilt/chapter-{ci+1:02d}.json', 'w'), ensure_ascii=False, indent=1)
        keyn = sum(1 for w in d['words'] if w['key'])
        print(f'ch{ci+1:02d}: {len(d["words"])} words, {len(d["pages"])} pages, {keyn} keywords, span {d["words"][0]["start"]}-{d["words"][-1]["end"]}s')
