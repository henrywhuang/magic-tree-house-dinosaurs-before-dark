#!/usr/bin/env python3
"""将 MLX Whisper 逐词输出整理为阅读器章节 JSON，并从 ECDICT 提取项目内词条。"""
import csv, glob, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)
KEYS=set('monster woods treehouse dinosaur pteranodon tyrannosaurus triceratops valley crest fossil ancient magnolia medallion mysterious adventure'.split())
FIX={
 'taranodon':'Pteranodon','tyrannidon':'Pteranodon','taranodons':'Pteranodons',
 'tyranodon':'Pteranodon','tyrannodon':'Pteranodon','tyrannodons':'Pteranodons','terenidon':'Pteranodon','terenidons':'Pteranodons',
 'tauranodon':'Pteranodon','tauranodons':'Pteranodons','tarranodon':'Pteranodon','tarranodons':'Pteranodons',
 'tyrannidon':'Pteranodon','taranosaurus':'Tyrannosaurus','netisauruses':'Anatosauruses',
 'tyranosaurus':'Tyrannosaurus','renoceros':'rhinoceros','peeked':'peeked','peaked':'peeked',
 'stedied':'steadied','teedered':'teetered','blighted':'glided','shotted':'shouted',
 'madalian':'medallion','shattered':'shouted','quintit':'Quit it','duck-build':'duck-billed','raise':'race','yell':'Yelled',
}
MANUAL={
 'jack':('/dʒæk/','杰克（人名）'),'annie':('/ˈæni/','安妮（人名）'),
 'frog':('/frɒɡ/','n. 青蛙'),'creek':('/kriːk/','n. 小溪'),'pennsylvania':('/ˌpensəlˈveɪniə/','n. 宾夕法尼亚州'),
 'pteranodon':('/təˈrænədɒn/','n. 无齿翼龙'),'tyrannosaurus':('/tɪˌrænəˈsɔːrəs/','n. 霸王龙'),
 'triceratops':('/traɪˈserətɒps/','n. 三角龙'),'anatosaurus':('/əˌnætəˈsɔːrəs/','n. 鸭嘴龙'),
 'henry':('/ˈhenri/','亨利（小狗的名字）'),'medallion':('/məˈdæliən/','n. 圆形大奖章；圆形饰品')
}

def clean_word(raw):
    m=re.search(r"[A-Za-z]+(?:[-'][A-Za-z]+)*",raw)
    if not m:return None
    lead=raw[:m.start()]; core=m.group(); tail=raw[m.end():]
    fixed=FIX.get(core.lower(),core)
    if core[:1].isupper() and fixed[:1].islower():fixed=fixed.capitalize()
    return lead,fixed,tail

all_vocab=set()
for n in range(1,11):
    src=ROOT/'transcript-base'/f'chapter-{n:02d}.json'
    d=json.loads(src.read_text())
    flat=[]; paragraphs=[]; current=[]; count=0
    for seg in d['segments']:
        if n==1 and seg['end']<37: continue # 按需求从 Chapter 1 / Into the Woods 开始
        if n==10 and seg['start']>300: continue # 排除有声书版权/制作人员片尾
        pwords=[]
        items=seg.get('words',[])
        for wi,item in enumerate(items):
            c=clean_word(item['word'])
            if not c:
                if flat and re.search(r'\d',item['word']): flat[-1]['after']+=item['word']
                continue
            before,word,after=c; idx=len(flat); low=word.lower()
            if low=='by' and wi+1<len(items) and re.search(r'henry',items[wi+1]['word'],re.I): word='Bye';low='bye'
            if low=='yelled': after=after.replace(',','')
            obj={'i':idx,'word':word,'before':before,'after':after,'start':round(item['start'],2),'end':round(item['end'],2),'key':low in KEYS}
            flat.append(obj);pwords.append(obj);all_vocab.add(low)
        if pwords:
            current.extend(pwords);count+=len(pwords)
            # 约 45–85 词一段，尽量在句号后断段
            last=pwords[-1].get('after','')
            if count>=55 and ('.' in last or '?' in last or '!' in last):
                paragraphs.append(current);current=[];count=0
    if current:paragraphs.append(current)
    pages=[]; page=[]; page_count=0
    for para in paragraphs:
        if page and page_count+len(para)>175:
            pages.append(page);page=[];page_count=0
        page.append({'words':para});page_count+=len(para)
    if page:pages.append(page)
    for pi,page in enumerate(pages):
        for para in page:
            for w in para['words']: w['page']=pi; flat[w['i']]['page']=pi
    (OUT/f'chapter-{n:02d}.json').write_text(json.dumps({'chapter':n,'words':flat,'pages':pages},ensure_ascii=False,separators=(',',':')))

# 只扫描实际用到的词，避免把整部词典带进 H5
entries={}
with open(ROOT/'.ecdict/ecdict.csv',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        w=row['word'].lower()
        if w not in all_vocab:continue
        trans=(row.get('translation') or '').split('\n')[0]
        if trans.startswith('[') and ']' in trans: trans=trans.split(']',1)[-1]
        if trans:entries[w]={'phonetic':f"/{row.get('phonetic') or w}/",'meaning':trans}
for w,(ph,meaning) in MANUAL.items():entries[w]={'phonetic':ph,'meaning':meaning}
(OUT/'words.js').write_text('window.WORDS='+json.dumps(entries,ensure_ascii=False,separators=(',',':'))+';')
print(f'生成 10 章，{len(all_vocab)} 个不同单词，{len(entries)} 条中文词卡。')
