#!/usr/bin/env python3
"""Build Book3 (木乃伊之谜 / Mummies in the Morning) reader data — reuses the Book1 pipeline:
OCR original text (authoritative American book text) timed by faster-whisper ASR word timestamps,
with per-chapter keyword highlights from the book's 课标+拓展 vocab lists.

Unlike the Book1 rebuild there is no prior data, so pages/scenes are created here:
one page per chapter with a placeholder scene image (cover.jpg); per-scene illustrations can be
curated separately later, exactly like Book1/Book2.

Text : 3木乃伊之谜.pdf_by_PaddleOCR-VL-1.6.json (OCR, via tmp/verify tooling, book index 2)
Timing: tmp/asr/book4-chXX.json (faster-whisper large-v3)
Output: tmp/rebuilt/book-04-chapter-XX.json (staging)
"""
import sys, re, json, difflib
sys.path.insert(0, 'tmp/verify')
from difftext import ocr_chapter_text, ocr_pages
from extract_final import chapter_vocab
import rekey

BOOK = 3
TITLES = ['Too Late!', 'The Bright Blue Sea', 'Three Men in a Boat', 'Vile Booty', "The Kid's Treasure", "The Whale's Eye", "Gale's a-Blowin'", 'Dig, Dogs, Dig', 'The Mysterious M', 'Treasure Again']
COVER = 'assets/images/cover.jpg'
SCENES = json.load(open('tmp/book4_qa/scenes.json'))  # {chapter_str: [3 scenes: title/desc/prompt]}

def norm_match(w): return re.sub(r'[^a-z]', '', w.lower())

def normalize_rebuild(t):
    t = t.replace('…', '...')
    for a, b in [('Anato- sauruses', 'Anatosauruses'), ('Pteran odon', 'Pteranodon')]:
        t = t.replace(a, b)
    t = re.sub(r'([A-Za-z])-\n([a-z])', r'\1-\2', t)
    return t

def strip_title(text, ci):
    out, dropping = [], True
    for ln in text.split('\n'):
        s = ln.strip()
        if dropping:
            k = norm_match(s)
            if not k:
                continue
            if k == 'chapter' or re.match(r'^chapter\d+$', k) or k == norm_match(TITLES[ci]) or k == 'chapter' + norm_match(TITLES[ci]):
                continue  # k=='chapter' catches "Chapter N" (norm_match strips the digit)
            dropping = False
        out.append(ln)
    return '\n'.join(out)

def tokenize_paragraph(para):
    toks = list(re.finditer(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", para))
    words, pos = [], 0
    for m in toks:
        s, e = m.start(), m.end()
        before = para[pos:s]
        j = e
        while j < len(para) and not para[j].isspace() and not para[j].isalnum():
            j += 1
        words.append({'word': m.group(), 'before': before, 'after': para[e:j]})
        pos = j
    return words

def build_ocr_words(ci, pages):
    text = strip_title(normalize_rebuild(ocr_chapter_text(BOOK, ci, pages)), ci)
    paras = [ln for ln in text.split('\n') if ln.strip()]
    words = []
    for pi, para in enumerate(paras):
        for w in tokenize_paragraph(para):
            w['para'] = pi
            words.append(w)
    return words, len(paras)

def assign_timestamps(ocr_words, asr_words):
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
    n = len(ocr_words)
    anchored = [i for i in range(n) if ocr_words[i]['start'] is not None]
    if not anchored:
        raise RuntimeError('no alignment anchors!')
    first, last = anchored[0], anchored[-1]
    for i in range(first):
        ocr_words[i]['start'] = max(0.0, ocr_words[first]['start'] - (first - i) * 0.28)
        ocr_words[i]['end'] = ocr_words[i]['start'] + 0.26
    for i in range(last + 1, n):
        ocr_words[i]['start'] = ocr_words[last]['end'] + (i - last - 1) * 0.30
        ocr_words[i]['end'] = ocr_words[i]['start'] + 0.28
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
    for i in range(1, n):
        if ocr_words[i]['start'] < ocr_words[i-1]['start']:
            ocr_words[i]['start'] = ocr_words[i-1]['start']
            if ocr_words[i]['end'] < ocr_words[i]['start']:
                ocr_words[i]['end'] = ocr_words[i]['start'] + 0.1
    for w in ocr_words:
        w['start'] = round(w['start'], 3); w['end'] = round(w['end'], 3)

def apply_keywords(ocr_words, ci, pages):
    kb, tz = chapter_vocab(BOOK, ci, pages)
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
    asr = json.load(open(f'tmp/asr/book4-ch{ci+1:02d}.json'))
    assign_timestamps(ocr_words, asr['words'])
    apply_keywords(ocr_words, ci, pages)
    NP = 3  # three scenes/pages per chapter, matching Book1/Book2
    for w in ocr_words:
        w['page'] = min(NP - 1, w['para'] * NP // max(1, num_paras))
    flat = [{'i': i, 'word': w['word'], 'before': w['before'], 'after': w['after'],
             'start': w['start'], 'end': w['end'], 'key': w['key'], 'page': w['page']}
            for i, w in enumerate(ocr_words)]
    pages_out = []
    for pg in range(NP):
        by_para = {}
        for i, w in enumerate(ocr_words):
            if w['page'] == pg:
                by_para.setdefault(w['para'], []).append(flat[i])
        pages_out.append([{'words': by_para[k]} for k in sorted(by_para)])
    sc = SCENES[str(ci + 1)]
    scenes = [[s['title'], f'assets/images/book-04-scenes/chapter-{ci+1:02d}-scene-{k+1:02d}.webp', s['desc']]
              for k, s in enumerate(sc)]
    return {'chapter': ci + 1, 'scenes': scenes, 'words': flat, 'pages': pages_out}

if __name__ == '__main__':
    import os
    os.makedirs('tmp/rebuilt', exist_ok=True)
    pages = ocr_pages(BOOK)
    chapters = [int(a) - 1 for a in sys.argv[1:]] if len(sys.argv) > 1 else list(range(10))
    for ci in chapters:
        d = build_chapter(ci, pages)
        json.dump(d, open(f'tmp/rebuilt/book-04-chapter-{ci+1:02d}.json', 'w'), ensure_ascii=False, indent=1)
        keyn = sum(1 for w in d['words'] if w['key'])
        print(f'book3 ch{ci+1:02d}: {len(d["words"])} words, {keyn} keywords, span {d["words"][0]["start"]}-{d["words"][-1]["end"]}s')
