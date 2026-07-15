#!/usr/bin/env python3
"""Rebuild data/words.js to cover EVERY word in all available books' reading text
(not just Book1), so tapping any word shows a real meaning + phonetic — and the
"add to vocabulary" feature captures a usable definition. Source: ECDICT
(surface first, lemma fallback) + manual names. Existing entries are preserved.
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
}

def norm(w):
    return re.sub(r"[^a-z'-]", '', w.lower())

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

# 1) all reading-text words across 4 books
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
    need.update(base_forms(w))
    need.add(w)
rows = {}
with open(ROOT / '.ecdict/ecdict.csv', encoding='utf-8', newline='') as fh:
    for row in csv.DictReader(fh):
        lw = row['word'].strip().lower()
        if lw in need and lw not in rows:
            rows[lw] = row

def lookup(w):
    forms = base_forms(w)
    cands = [(b, rows[b]) for b in forms if b in rows and (rows[b].get('translation') or '').strip()]
    if not cands:
        return None
    # prefer a real definition over an abbreviation (gets->GETS), then the shortest
    # base form (boots->boot 靴子, happened->happen 发生) for a clean learner meaning
    cands.sort(key=lambda br: (1 if re.match(r'^\s*abbr', br[1].get('translation', ''), re.I) else 0, len(br[0])))
    row = cands[0][1]
    surf = rows.get(forms[0])          # phonetic from the surface form when available
    ph = ((surf and surf.get('phonetic')) or row.get('phonetic') or w).strip()
    return f'/{ph}/', clean_meaning(row['translation'])

# 3) build entries fresh from every reading-text word (+ manual names)
entries = {}
covered = 0
for w in sorted(words):
    res = lookup(w)
    if res:
        entries[w] = {'phonetic': res[0], 'meaning': res[1]}
        covered += 1
for w, (ph, meaning) in MANUAL.items():
    entries[w] = {'phonetic': ph, 'meaning': meaning}

# normalize meanings across ALL entries (incl. preserved legacy) — no literal \n / \r
for e in entries.values():
    e['meaning'] = re.sub(r'\s*(\\r\\n|\\n|\\r|[\r\n])\s*', ' / ', e['meaning']).strip(' /')

(ROOT / 'data' / 'words.js').write_text(
    'window.WORDS=' + json.dumps(entries, ensure_ascii=False, separators=(',', ':')) + ';', 'utf-8')
print(f'reading-text words={len(words)} | ECDICT covered={covered} ({covered * 100 // len(words)}%) | total dict entries={len(entries)}')
