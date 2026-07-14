import json, re, difflib
def norm(w): return re.sub(r'[^a-z]','',w.lower())
for ci in range(1,11):
    try:
        reb=json.load(open(f'tmp/rebuilt/chapter-{ci:02d}.json'))
        asr=json.load(open(f'tmp/asr/ch{ci:02d}.json'))
    except FileNotFoundError: 
        print(f'ch{ci}: 缺文件'); continue
    ow=[w['word'] for w in reb['words']]; aw=[w['word'].strip() for w in asr['words']]
    sm=difflib.SequenceMatcher(None,[norm(x) for x in ow],[norm(x) for x in aw],autojunk=False)
    diffs=[(' '.join(ow[i1:i2]),' '.join(aw[j1:j2])) for tag,i1,i2,j1,j2 in sm.get_opcodes() if tag=='replace']
    # 过滤:两边都非空、且不是纯大小写/标点差异
    diffs=[(o,a) for o,a in diffs if o.strip() and a.strip() and len(o)<60 and len(a)<60]
    print(f'=== ch{ci}: {len(reb["words"])}词, {len(diffs)}处 OCR≠ASR ===')
    for o,a in diffs[:30]: print(f'  OCR:[{o}]  ASR:[{a}]')
