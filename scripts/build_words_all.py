#!/usr/bin/env python3
"""Rebuild data/words.js to cover EVERY word in all available books' reading text
(not just Book1), so tapping any word shows a real meaning + phonetic — and the
"add to vocabulary" feature captures a usable definition and dictionary lemma.
Source: ECDICT (including its ``exchange`` lemma mapping) + manual names.
"""
import csv, glob, json, re, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from gen_vocab_book4 import base_forms
csv.field_size_limit(10 ** 7)
ROOT = Path(__file__).resolve().parents[1]

MANUAL = {
    'jack': ('/dʒæk/', '杰克（人名）'), 'annie': ('/ˈæni/', '安妮（人名）'),
    'frog': ('/frɒɡ/', 'n. 青蛙'), 'creek': ('/kriːk/', 'n. 小溪'),
    'pennsylvania': ('/ˌpensəlˈveɪniə/', 'n. 宾夕法尼亚州'),
    'pteranodon': ('/təˈrænədɒn/', 'n. 无齿翼龙'), 'tyrannosaurus': ('/tɪˌrænəˈsɔːrəs/', 'n. 霸王龙'),
    'triceratops': ('/traɪˈserətɒps/', 'n. 三角龙'), 'anatosaurus': ('/əˌnætəˈsɔːrəs/', 'n. 鸭嘴龙'),
    'henry': ('/ˈhenri/', '亨利（小狗的名字）'), 'medallion': ('/məˈdæliən/', 'n. 圆形大奖章；圆形饰品'),
    'morgan': ('/ˈmɔːrɡən/', '摩根（人名）'), 'camelot': ('/ˈkæməlɒt/', 'n. 卡默洛特（亚瑟王传说中的宫廷）'),
    'kidd': ('/kɪd/', '基德（海盗船长名）'), 'polly': ('/ˈpɒli/', '波莉（鹦鹉名）'),
    'caribbean': ('/ˌkærɪˈbiːən/', 'a. 加勒比海的'),
    'peanut': ('/ˈpiːnʌt/', '花生米（小老鼠的名字）'),
    'ninja': ('/ˈnɪndʒə/', 'n. 忍者'), 'ninjas': ('/ˈnɪndʒəz/', 'n. 忍者（复数）'),
    'samurai': ('/ˈsæmuraɪ/', 'n. 日本武士'), 'japan': ('/dʒəˈpæn/', 'n. 日本'),
    'amazon': ('/ˈæməzən/', 'n. 亚马孙河；亚马孙雨林'),
    'piranha': ('/pɪˈrɑːnə/', 'n. 食人鱼；水虎鱼'), 'piranhas': ('/pɪˈrɑːnəz/', 'n. 食人鱼；水虎鱼（复数）'),
    'jaguar': ('/ˈdʒæɡwɑːr/', 'n. 美洲虎'), 'caiman': ('/ˈkeɪmən/', 'n. 凯门鳄'),
    'capuchin': ('/ˈkæpjʊtʃɪn/', 'n. 卷尾猴'), 'mango': ('/ˈmæŋɡəʊ/', 'n. 芒果'),
    'canoe': ('/kəˈnuː/', 'n. 独木舟；小划艇'), 'moonstone': ('/ˈmuːnstəʊn/', 'n. 月光石'),
    'sabertooth': ('/ˈseɪbərtuːθ/', 'n. 剑齿虎'),
    'cro-magnon': ('/ˌkroʊ mæɡˈnɒn/', 'n. 克罗马农人'),
    'mammoth': ('/ˈmæməθ/', 'n. 猛犸象'), 'lulu': ('/ˈluːluː/', '露露（猛犸象的名字）'),
    'sorcerer': ('/ˈsɔːrsərər/', 'n. 巫师；术士'),
    'reindeer': ('/ˈreɪndɪər/', 'n. 驯鹿'), 'bison': ('/ˈbaɪsən/', 'n. 野牛'),
    "that'll": ('/ðætəl/', '那将会（that will 的缩写）'),
    "there're": ('/ðeərər/', '有（there are 的缩写）'),
}

# ECDICT occasionally chooses an unrelated homograph or an obsolete spelling
# for a valid story word.  These overrides are intentionally small and audited.
LEMMA_OVERRIDES = {
    'does': 'do',
    'ragged': 'ragged',
    'sled': 'sled',
    'untied': 'untie',
    'yikes': 'yikes',
}

def norm(w):
    return re.sub(r"[^a-z'-]", '', w.lower().replace('’', "'").replace('‘', "'"))

def candidate_forms(w):
    forms = list(base_forms(w))
    # Possessives are surface forms, not separate dictionary headwords.
    if w.endswith("'s") and len(w) > 2:
        forms.append(w[:-2])
    return list(dict.fromkeys(forms))

POS_LINE = re.compile(r'^\s*(n|vt|vi|v|adj|adv|a|ad|prep|conj|pron|int|num|art|aux|pl)\b\.?', re.I)

def clean_meaning(translation):
    t = (translation or '').replace('\\r', '').replace('\r', '')
    lines = [re.sub(r'\[[^\]]*\]\s*', '', p).strip() for p in re.split(r'\\n|\n', t) if p.strip()]
    kept = [l for l in lines if POS_LINE.match(l)] or lines[:1]   # keep pos-tagged senses, drop cruft (DOS/程序…)
    out = []
    for line in kept[:2]:                                          # at most two part-of-speech groups
        senses = [s.strip(' .') for s in re.split(r'[,，;；]\s*', line) if s.strip(' .')]
        uniq = list(dict.fromkeys(senses))                         # drop duplicate senses
        if uniq:
            out.append('；'.join(uniq[:3]))                        # up to three senses each
    return ' / '.join(out)

# 1) all reading-text words across every available book
words = set()
for f in glob.glob(str(ROOT / 'data' / '*chapter-*.json')):
    if 'vocabulary' in f:
        continue
    for w in json.loads(Path(f).read_text('utf-8')).get('words', []):
        n = norm(w['word'])
        if n:
            words.add(n)

# 2) load ECDICT rows for surfaces + lemma candidates in one scan
need = set()
for w in words:
    need.update(candidate_forms(w))
    need.add(w)
rows = {}
with open(ROOT / '.ecdict/ecdict.csv', encoding='utf-8', newline='') as fh:
    for row in csv.DictReader(fh):
        lw = row['word'].strip().lower()
        if lw in need and lw not in rows:
            rows[lw] = row

# A surface row can point to an irregular lemma (went -> go, mice -> mouse)
# which simple suffix rules cannot predict. Fetch those headwords in one extra scan.
exchange_need = set()
for row in rows.values():
    match = re.search(r'(?:^|/)0:([^/]+)', row.get('exchange') or '')
    if match:
        lemma = norm(match.group(1))
        if lemma and lemma not in rows:
            exchange_need.add(lemma)
if exchange_need:
    with open(ROOT / '.ecdict/ecdict.csv', encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh):
            lw = row['word'].strip().lower()
            if lw in exchange_need and lw not in rows:
                rows[lw] = row

def exchange_lemma(row):
    """ECDICT stores the dictionary headword as ``0:lemma`` for inflections."""
    match = re.search(r'(?:^|/)0:([^/]+)', (row or {}).get('exchange') or '')
    return norm(match.group(1)) if match else ''

def lookup(w):
    surface = rows.get(w)
    mapped = LEMMA_OVERRIDES.get(w) or exchange_lemma(surface)
    forms = list(dict.fromkeys(([mapped] if mapped else []) + candidate_forms(w)))
    possessive_base = w[:-2] if w.endswith("'s") else ''
    if possessive_base in MANUAL:
        phonetic, meaning = MANUAL[possessive_base]
        return phonetic, meaning, possessive_base
    cands = [(b, rows[b]) for b in forms if b in rows and (rows[b].get('translation') or '').strip()]
    if not cands:
        return None
    # Prefer ECDICT's explicit inflection mapping.  Without such a mapping, keep
    # the exact headword before trying suffix guesses; otherwise ordinary words
    # such as water/wave could be shortened to unrelated entries (wat/wav).
    cands.sort(key=lambda br: (0 if mapped and br[0] == mapped else 1,
                               0 if not mapped and br[0] == w else 1,
                               1 if re.match(r'^\s*abbr', br[1].get('translation', ''), re.I) else 0,
                               len(br[0])))
    lemma, row = cands[0]
    ph = ((surface and surface.get('phonetic')) or row.get('phonetic') or w).strip()
    return f'/{ph}/', clean_meaning(row['translation']), lemma

# 3) build entries fresh from every reading-text word (+ manual names)
entries = {}
covered = 0
for w in sorted(words):
    res = lookup(w)
    if res:
        entries[w] = {'phonetic': res[0], 'meaning': res[1], 'lemma': res[2]}
        covered += 1
for w, (ph, meaning) in MANUAL.items():
    entries[w] = {'phonetic': ph, 'meaning': meaning, 'lemma': w}

# normalize meanings across ALL entries (incl. preserved legacy) — no literal \n / \r
for e in entries.values():
    e['meaning'] = re.sub(r'\s*(\\r\\n|\\n|\\r|[\r\n])\s*', ' / ', e['meaning']).strip(' /')

(ROOT / 'data' / 'words.js').write_text(
    'window.WORDS=' + json.dumps(entries, ensure_ascii=False, separators=(',', ':')) + ';', 'utf-8')
print(f'reading-text words={len(words)} | ECDICT covered={covered} ({covered * 100 // len(words)}%) | total dict entries={len(entries)}')
