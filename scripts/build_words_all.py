#!/usr/bin/env python3
"""Rebuild data/words.js to cover EVERY word in all available books' reading text
(not just Book1), so tapping any word shows a real meaning + phonetic — and the
"add to vocabulary" feature captures a usable definition and dictionary lemma.
Source: ECDICT (including its ``exchange`` lemma mapping) + manual names.
"""
import argparse, csv, glob, json, re, sys
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
    'moondust': ('/ˈmuːndʌst/', 'n. 月尘；月球表面的细尘'),
    'mini-spaceship': ('/ˈmɪni ˈspeɪsʃɪp/', 'n. 小型宇宙飞船'),
    'mini-sub': ('/ˈmɪni sʌb/', 'n. 迷你潜艇；小型潜水器'),
    'sukie': ('/ˈsuːki/', '苏琪（海豚的名字）'), 'sam': ('/sæm/', '山姆（海豚的名字）'),
    'oceanographer': ('/ˌoʊʃəˈnɑːɡrəfər/', 'n. 海洋学家'),
    'submersible': ('/səbˈmɜːrsəbəl/', 'n. 潜水器；可潜水的船只'),
    'hammerhead': ('/ˈhæmərhed/', 'n. 双髻鲨；锤头鲨'),
    'cooley': ('/ˈkuːli/', '库利（牛仔斯利姆的姓）'),
    'dusty': ('/ˈdʌsti/', 'a. 布满灰尘的；达斯蒂（马名）'),
    'sunset': ('/ˈsʌnset/', 'n. 日落；Sunset（小马名）'),
    'luke': ('/luːk/', '卢克（人名）'), 'laramie': ('/ˈlærəmi/', 'n. 拉勒米（美国地名）'),
    'smiley': ('/ˈsmaɪli/', 'n. 笑脸；斯迈利（绰号）'),
    'shorty': ('/ˈʃɔːrti/', 'n. 矮个子；肖蒂（绰号）'),
    'owww': ('/aʊ/', 'int. 哎哟（表示疼痛）'),
    "young'uns": ('/ˈjʌŋənz/', 'n. 小家伙；幼崽'),
    "she'll": ('/ʃiːl/', '她将会（she will 的缩写）'),
    "that'll": ('/ðætəl/', '那将会（that will 的缩写）'),
    "there're": ('/ðeərər/', '有（there are 的缩写）'),
    'africa': ('/ˈæfrɪkə/', 'n. 非洲'),
    'african': ('/ˈæfrɪkən/', 'adj. 非洲的；n. 非洲人'),
    'kenya': ('/ˈkenjə/', 'n. 肯尼亚'),
    'tanzania': ('/ˌtænzəˈniːə/', 'n. 坦桑尼亚'),
    'mara': ('/ˈmɑːrə/', 'n. 马拉河（非洲地名）'),
    'masai': ('/məˈsaɪ/', 'n. 马赛人'),
    'thomson': ('/ˈtɒmsən/', '汤姆森（人名；汤氏瞪羚名称的一部分）'),
    'gazelle': ('/ɡəˈzel/', 'n. 瞪羚'),
    'wildebeest': ('/ˈwɪldəbiːst/', 'n. 角马'),
    'honeyguide': ('/ˈhʌniɡaɪd/', 'n. 响蜜鴞；导蜜鸟'),
    'will-dubbeests': ('/ˈwɪldəbiːsts/', '角马 wildebeests 的读音提示'),
    'hi-ee-nuh': ('/haɪˈiːnə/', '鬣狗 hyena 的读音提示'),
    'muh-sy': ('/məˈsaɪ/', '马赛 Masai 的读音提示'),
    'tribesperson': ('/ˈtraɪbzpɜːrsən/', 'n. 部落成员'),
    'argggghh': ('/ɑːrɡ/', 'int. 啊（大声喊叫）'),
    'ta-da': ('/təˈdɑː/', 'int. 铛铛（展示成果时的欢呼）'),
    'c-c-calm': ('/kɑːm/', '结巴说出的 calm：冷静的'),
    'fi-fr-freezing': ('/ˈfriːzɪŋ/', '结巴说出的 freezing：极冷的；冰冻的'),
    'fur-covered': ('/ˈfɜːr ˌkʌvərd/', 'adj. 覆盖着毛皮的'),
    'fur-trimmed': ('/ˈfɜːr trɪmd/', 'adj. 镶有毛皮边的'),
    'l-a-t-l-t': ('/el eɪ tiː el tiː/', '字母序列 L-A-T-L-T'),
    'm-m-maybe': ('/ˈmeɪbi/', '结巴说出的 maybe：也许'),
    'hemo': ('/ˈhiːmoʊ/', '未组成正确单词的字母组合'),
    'meho': ('/ˈmiːhoʊ/', '未组成正确单词的字母组合'),
    'o-e-h-m': ('/oʊ iː eɪtʃ em/', '字母序列 O-E-H-M，可重排为 HOME'),
    'r-r-read': ('/riːd/', '结巴说出的 read：阅读'),
    'th-th-thanks': ('/θæŋks/', '结巴说出的 thanks：谢谢'),
    'th-th-that': ('/ðæt/', '结巴说出的 that：那个'),
    "w-w-we're": ('/wɪr/', '结巴说出的 we’re：我们是'),
    'wait-listen': ('/weɪt ˈlɪsən/', '等一下，听'),
    'wait-wait': ('/weɪt/', '重复说出的 wait：等等'),
    "wh-wh-what's": ('/wʌts/', '结巴说出的 what’s：是什么'),
    "where'd": ('/wɛrd/', 'where did 的缩写：在哪里'),
    'whoo': ('/huː/', 'int. 猫头鹰的呼叫声'),
    'pompeii': ('/pɒmˈpeɪiː/', 'n. 庞贝（古罗马城市）'),
    'vesuvius': ('/vəˈsuːviəs/', 'n. 维苏威火山'),
    'brutus': ('/ˈbruːtəs/', '布鲁图斯（古罗马人名）'),
    'jupiter': ('/ˈdʒuːpɪtər/', 'n. 朱庇特（古罗马主神）'),
    'hercules': ('/ˈhɜːrkjuliːz/', 'n. 赫拉克勒斯；大力神'),
    'apollo': ('/əˈpɒloʊ/', 'n. 阿波罗（古希腊罗马神话人物）'),
    'venus': ('/ˈviːnəs/', 'n. 维纳斯（古罗马神话人物）'),
    'medusa': ('/mɪˈduːsə/', 'n. 美杜莎（古希腊神话人物）'),
    'ml': ('/em el/', '字母 M–L，代表 Master Librarian'),
    'vir': ('/vɪr/', '拉丁语：男人；英雄'),
    'fortissimus': ('/fɔːrˈtɪsɪmʊs/', '拉丁语：最强大的'),
    'mundo': ('/ˈmʊndoʊ/', '拉丁语：世界之中'),
    'pom-pay': ('/pɒmˈpeɪ/', 'Pompeii 的读音提示'),
    'vuh-soo-vee-us': ('/vəˈsuːviəs/', 'Vesuvius 的读音提示'),
    'am-fuh-thee-uh-ter': ('/ˌæmfɪˈθiːətər/', 'amphitheater 的读音提示：圆形露天竞技场'),
    'puh-pi-rus': ('/pəˈpaɪrəs/', 'papyrus 的读音提示：纸莎草纸'),
    'pum-iss': ('/ˈpʌmɪs/', 'pumice 的读音提示：浮石'),
    'gentle-looking': ('/ˈdʒentəl ˌlʊkɪŋ/', 'adj. 相貌温和的'),
    'v-v-volcano': ('/vɒlˈkeɪnoʊ/', '结巴说出的 volcano：火山'),
    "it's-it's": ('/ɪts/', '结巴说出的 it’s：它是'),
}

# ECDICT occasionally chooses an unrelated homograph or an obsolete spelling
# for a valid story word.  These overrides are intentionally small and audited.
LEMMA_OVERRIDES = {
    'does': 'do',
    'ragged': 'ragged',
    'sled': 'sled',
    'untied': 'untie',
    'yikes': 'yikes',
    'fo-fourth': 'fourth',
    'sl-slow': 'slow',
    'd-down': 'down',
    'b-brake': 'brake',
    'f-floor': 'floor',
    'ja-ack': 'jack',
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

# 1) all reading-text words across every available book (or through --max-book)
parser = argparse.ArgumentParser()
parser.add_argument('--max-book', type=int, default=0,
                    help='Only include reader data through this book number')
args = parser.parse_args()
words = set()
for f in glob.glob(str(ROOT / 'data' / '*chapter-*.json')):
    if 'vocabulary' in f:
        continue
    name = Path(f).name
    match = re.match(r'book-(\d+)-chapter-', name)
    book = int(match.group(1)) if match else 1
    if args.max_book and book > args.max_book:
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
