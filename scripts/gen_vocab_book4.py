#!/usr/bin/env python3
"""Generate Book4 vocabulary JSON (data/vocabulary-book-04-chapter-NN.json) for every
underlined key word, matching the Book1-3 schema.

Word list = the chapter's `key` words (103 total). Per word:
  - phonetic / partOfSpeech / meaning  <- ECDICT (.ecdict/ecdict.csv), lemma fallback
  - sentence                           <- reconstructed chapter text (position-based)
  - tier core/recognition              <- content words (<=10/ch) = core, rest = recognition
  - phonics (core only)                <- rule-based grapheme segmentation
  - options (core only)                <- correct meaning + 2 distractors from same-chapter core
Audio is generated separately by gen_vocab_book4_audio.py (macOS `say -v Alex`).
"""
import json, re, csv
from pathlib import Path
csv.field_size_limit(10 ** 7)

ROOT = Path(__file__).resolve().parents[1]
TITLES = ['Too Late!', 'The Bright Blue Sea', 'Three Men in a Boat', 'Vile Booty',
          "The Kid's Treasure", "The Whale's Eye", "Gale's a-Blowin'", 'Dig, Dogs, Dig',
          'The Mysterious M', 'Treasure Again']
PROPER = {'spanish', 'jolly', 'roger'}
FUNCTION = {'the', 'a', 'an', 'and', 'or', 'but', 'with', 'of', 'to', 'in', 'on', 'at',
            'it', 'is', 'was', 'be', 'as', 'so', 'if', 'about', 'also', 'new', 'this',
            'that', 'these', 'those', 'here', 'there', 'run', 'rest', 'man', 'row'}

# ---------- ECDICT ----------
def base_forms(w):
    w = w.lower(); f = [w]
    if w.endswith('ies') and len(w) > 4: f.append(w[:-3] + 'y')
    if w.endswith('es') and len(w) > 3: f.append(w[:-2])
    if w.endswith('s') and len(w) > 2: f.append(w[:-1])
    if w.endswith('ed') and len(w) > 3:
        f += [w[:-1], w[:-2]]
        if len(w) > 4 and w[-3] == w[-4]: f.append(w[:-3])
    if w.endswith('ing') and len(w) > 4:
        f += [w[:-3], w[:-3] + 'e']
        if len(w) > 5 and w[-4] == w[-5]: f.append(w[:-4])
    if w.endswith('est') and len(w) > 4: f += [w[:-3], w[:-2]]
    if w.endswith('er') and len(w) > 3: f += [w[:-2], w[:-1]]
    if w.endswith('ly') and len(w) > 3: f.append(w[:-2])
    seen = []; [seen.append(x) for x in f if x not in seen]
    return seen

def load_ecdict(needed):
    need = set()
    for w in needed:
        need.update(base_forms(w))
    d = {}
    with open(ROOT / '.ecdict/ecdict.csv', newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            w = row['word'].strip().lower()
            if w in need and w not in d:
                d[w] = row
    return d

POS_MAP = {'n': 'n.', 'v': 'v.', 'vt': 'v.', 'vi': 'v.', 'a': 'adj.', 'adj': 'adj.',
           'ad': 'adv.', 'adv': 'adv.', 'prep': 'prep.', 'conj': 'conj.', 'pron': 'pron.',
           'int': 'int.', 'num': 'num.', 'art': 'art.'}

# context-specific overrides for possessives / proper nouns ECDICT can't place
# key = word.lower(); value = (phonetic_or_None, pos, meaning)
OVERRIDES = {
    "kid's": ('/kɪdz/', '', '小孩的；（此处指海盗基德 Kidd 的）'),
    "gale's": ('/geɪlz/', '', '大风的；狂风的'),
    'roger': (None, 'n.', '（Jolly Roger）海盗旗'),
}

def _rows_shortest(word, ec):
    """ECDICT rows for the word's forms, shortest headword first (avoids inflected
    entries whose primary sense drifted, e.g. boots->擦靴的仆役 vs boot->靴子)."""
    forms = sorted({b for b in base_forms(word) if b in ec}, key=len)
    return [ec[b] for b in forms]

def get_phonetic(word, ec):
    for b in base_forms(word):            # surface form first: keeps plural/past phonetics
        row = ec.get(b)
        if row and (row.get('phonetic') or '').strip():
            return '/%s/' % row['phonetic'].strip()
    return ''

def get_pos(word, ec):
    for row in _rows_shortest(word, ec):
        t = (row.get('translation') or '').replace('\\n', '\n').strip()
        if re.match(r'^\s*pl\b\.?', t):
            return 'n.'
        m = re.match(r'^\s*(vt|vi|adj|adv|prep|conj|pron|int|num|art|n|v|a|ad)\b\.?', t)
        if m:
            return POS_MAP.get(m.group(1), '')
    return ''

def get_meaning(word, ec):
    for row in _rows_shortest(word, ec):
        t = (row.get('translation') or '').replace('\\n', '\n').strip()
        if not t:
            continue
        line = t.split('\n')[0].strip()
        line = re.sub(r'^\s*(pl|abbr|vt|vi|adj|adv|prep|conj|pron|int|num|art|n|v|a|ad)\b\.?\s*', '', line)
        line = re.sub(r'[\(（][^)）]*[\)）]', '', line)   # drop half/full-width parentheticals
        parts = [p.strip(' .') for p in re.split(r'[,，;；]\s*', line) if p.strip(' .')]
        if parts:
            return '；'.join(parts[:2])
    return ''

# ---------- sentence extraction ----------
def build_text(words):
    text = ''; spans = []
    for w in words:
        text += w.get('before', '')
        s = len(text); text += w['word']; e = len(text)
        text += w.get('after', '')
        spans.append((s, e))
    return text, spans

def sentence_spans(text):
    n = len(text); i = 0; start = 0; out = []
    while i < n:
        if text[i] in '.!?':
            j = i + 1
            while j < n and text[j] in '”"\'’)':
                j += 1
            out.append((start, j))
            while j < n and text[j] in ' \n\t':
                j += 1
            start = j; i = j
        else:
            i += 1
    if start < n:
        out.append((start, n))
    return out

def find_sentence(text, sents, span):
    ts, te = span
    for ss, se in sents:
        if ss <= ts < se:
            return re.sub(r'\s+', ' ', text[ss:se]).strip()
    return re.sub(r'\s+', ' ', text[max(0, ts - 40):te + 40]).strip()

# ---------- phonics (rule-based grapheme segmentation) ----------
VOWEL_DIGRAPHS = {'igh': '/aɪ/', 'ai': '/eɪ/', 'ay': '/eɪ/', 'ea': '/iː/', 'ee': '/iː/',
                  'ei': '/eɪ/', 'ey': '/eɪ/', 'oa': '/oʊ/', 'oe': '/oʊ/', 'oo': '/uː/',
                  'ou': '/aʊ/', 'ow': '/oʊ/', 'oi': '/ɔɪ/', 'oy': '/ɔɪ/', 'au': '/ɔː/',
                  'aw': '/ɔː/', 'ie': '/aɪ/', 'ue': '/uː/', 'ui': '/uː/', 'ew': '/uː/'}
R_CTRL = {'ar': '/ɑːr/', 'er': '/ər/', 'ir': '/ɜːr/', 'or': '/ɔːr/', 'ur': '/ɜːr/'}
CONS_DIGRAPHS = {'tch': '/tʃ/', 'dge': '/dʒ/', 'ch': '/tʃ/', 'sh': '/ʃ/', 'th': '/θ/',
                 'wh': '/w/', 'ph': '/f/', 'ng': '/ŋ/', 'ck': '/k/', 'gh': '/g/', 'qu': '/kw/'}
BLENDS = {'str', 'spr', 'spl', 'scr', 'thr', 'shr', 'squ',
          'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sk',
          'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'tr', 'tw', 'dw', 'nd', 'nt', 'nk', 'mp',
          'st', 'ld', 'lt', 'ft', 'ct', 'pt', 'lf', 'sk'}
BLEND_SOUND = {'str': '/str/', 'spr': '/spr/', 'spl': '/spl/', 'scr': '/skr/', 'thr': '/θr/',
               'squ': '/skw/', 'bl': '/bl/', 'br': '/br/', 'cl': '/kl/', 'cr': '/kr/',
               'dr': '/dr/', 'fl': '/fl/', 'fr': '/fr/', 'gl': '/gl/', 'gr': '/gr/',
               'pl': '/pl/', 'pr': '/pr/', 'sc': '/sk/', 'sk': '/sk/', 'sl': '/sl/',
               'sm': '/sm/', 'sn': '/sn/', 'sp': '/sp/', 'st': '/st/', 'sw': '/sw/',
               'tr': '/tr/', 'tw': '/tw/', 'dw': '/dw/', 'nd': '/nd/', 'nt': '/nt/',
               'nk': '/ŋk/', 'mp': '/mp/', 'ld': '/ld/', 'lt': '/lt/', 'ft': '/ft/'}
SUFFIXES = [('tion', '/ʃən/'), ('sion', '/ʒən/'), ('ture', '/tʃər/'), ('ing', '/ɪŋ/'),
            ('ely', '/li/'), ('ly', '/li/'), ('est', '/ɪst/'), ('ers', '/ərz/'),
            (' full', '/fʊl/'), ('ful', '/fʊl/'), ('ness', '/nəs/'), ('ed', '/d/')]
SHORT_VOWEL = {'a': '/æ/', 'e': '/ɛ/', 'i': '/ɪ/', 'o': '/ɒ/', 'u': '/ʌ/', 'y': '/i/'}
CONS = {'b': '/b/', 'c': '/k/', 'd': '/d/', 'f': '/f/', 'g': '/g/', 'h': '/h/', 'j': '/dʒ/',
        'k': '/k/', 'l': '/l/', 'm': '/m/', 'n': '/n/', 'p': '/p/', 'q': '/k/', 'r': '/r/',
        's': '/s/', 't': '/t/', 'v': '/v/', 'w': '/w/', 'x': '/ks/', 'z': '/z/'}
VOWELS = set('aeiou')

def phonics(word):
    w = re.sub(r"[^a-zA-Z]", '', word).lower()
    if not w:
        return []
    pieces = []
    suffix = None
    for suf, snd in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            suffix = (suf, snd); w = w[:-len(suf)]; break
    i = 0; n = len(w)
    while i < n:
        chunk = None
        three = w[i:i + 3]; two = w[i:i + 2]
        if three in CONS_DIGRAPHS:
            chunk = (three, CONS_DIGRAPHS[three], '辅音组合'); i += 3
        elif three in BLENDS:
            chunk = (three, BLEND_SOUND.get(three, '/%s/' % three), '辅音连缀'); i += 3
        elif two in CONS_DIGRAPHS:
            chunk = (two, CONS_DIGRAPHS[two], '辅音组合'); i += 2
        elif two in VOWEL_DIGRAPHS:
            chunk = (two, VOWEL_DIGRAPHS[two], '元音组合'); i += 2
        elif two in R_CTRL:
            chunk = (two, R_CTRL[two], '元音组合'); i += 2
        elif two in BLENDS and not (w[i] in VOWELS or w[i + 1] in VOWELS):
            chunk = (two, BLEND_SOUND.get(two, '/%s/' % two), '辅音连缀'); i += 2
        else:
            ch = w[i]
            if ch in VOWELS:
                chunk = (ch, SHORT_VOWEL.get(ch, '/%s/' % ch), '字母音')
            else:
                chunk = (ch, CONS.get(ch, '/%s/' % ch), '字母音')
            i += 1
        pieces.append({'letters': chunk[0], 'sound': chunk[1], 'rule': chunk[2]})
    if suffix:
        pieces.append({'letters': suffix[0], 'sound': suffix[1], 'rule': '常见词尾'})
    return pieces

# ---------- classification ----------
def rarity(word, ec):
    best = 0
    for row in _rows_shortest(word, ec):
        try:
            bnc = int(row.get('bnc') or 0); frq = int(row.get('frq') or 0)
        except ValueError:
            bnc = frq = 0
        rank = bnc or frq
        best = max(best, rank if rank else 40000)
    return best or 40000

def eligible_core(word):
    lw = re.sub(r"[^a-z]", '', word.lower())
    if "'" in word or '’' in word:
        return False
    if lw in PROPER or lw in FUNCTION:
        return False
    if len(lw) <= 3:
        return False
    return True

def stable_pick(pool, k, seed):
    if len(pool) <= k:
        return list(pool)
    h = [(int(__import__('hashlib').md5((seed + '|' + p).encode()).hexdigest(), 16), p) for p in pool]
    h.sort()
    return [p for _, p in h[:k]]

# ---------- build ----------
def build_chapter(ci):
    data = json.loads((ROOT / f'data/book-04-chapter-{ci:02d}.json').read_text('utf-8'))
    words = data['words']
    text, spans = build_text(words)
    sents = sentence_spans(text)
    keys = [(w['word'], spans[k]) for k, w in enumerate(words) if w.get('key')]
    # dedupe by surface form (keep first occurrence + its sentence)
    seen = {}; order = []
    for surface, span in keys:
        if surface not in seen:
            seen[surface] = span; order.append(surface)
    ec = load_ecdict(order)

    def resolve(surface):
        ov = OVERRIDES.get(surface.lower())
        ph, pos, mean = get_phonetic(surface, ec), get_pos(surface, ec), (get_meaning(surface, ec) or surface)
        if ov:
            ph = ov[0] if ov[0] is not None else ph
            pos = ov[1] if ov[1] else pos
            mean = ov[2] if ov[2] else mean
        return ph, pos, mean

    # tier split: core = up to 10 highest-rarity eligible words
    elig = [w for w in order if eligible_core(w)]
    elig.sort(key=lambda w: (-rarity(w, ec), w.lower()))
    core_set = set(elig[:10])
    # assemble core first (for distractor pool), then recognition
    entries = []; used_ids = set()
    core_meanings = {}
    for surface in order:
        if surface in core_set:
            core_meanings[surface] = resolve(surface)[2]
    for surface in order:
        wid = re.sub(r"[^a-z0-9]", '', surface.lower()) or 'w'
        base = wid; c = 2
        while wid in used_ids:
            wid = f'{base}{c}'; c += 1
        used_ids.add(wid)
        phonetic, pos, meaning = resolve(surface)
        entry = {
            'id': wid, 'word': surface, 'forms': [surface],
            'tier': 'core' if surface in core_set else 'recognition',
            'phonetic': phonetic, 'partOfSpeech': pos,
            'meaning': meaning, 'wordForms': f'原文词形：{surface}',
            'sentence': find_sentence(text, sents, seen[surface]),
            'sentenceAudio': f'assets/audio/sentences/book-04-chapter-{ci:02d}/{wid}.mp3',
        }
        if surface in core_set:
            entry['phonics'] = phonics(surface)
            others = [m for s, m in core_meanings.items() if s != surface and m != meaning]
            distract = stable_pick(sorted(set(others)), 2, surface)
            entry['options'] = [meaning] + distract
        entries.append(entry)
    return {'book': 4, 'chapter': ci, 'title': TITLES[ci - 1], 'words': entries}

def main():
    for ci in range(1, 11):
        obj = build_chapter(ci)
        out = ROOT / f'data/vocabulary-book-04-chapter-{ci:02d}.json'
        out.write_text(json.dumps(obj, ensure_ascii=False, indent=2), 'utf-8')
        nc = sum(1 for w in obj['words'] if w['tier'] == 'core')
        print(f'ch{ci:02d}: {len(obj["words"])} words ({nc} core / {len(obj["words"]) - nc} rec) -> {out.name}')

if __name__ == '__main__':
    main()
