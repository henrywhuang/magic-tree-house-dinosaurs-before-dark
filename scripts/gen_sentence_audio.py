#!/usr/bin/env python3
"""Generate vocabulary sentence clips for one book with macOS `say`.
Usage: gen_sentence_audio.py <book>"""
import glob, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
book = int(sys.argv[1])
FILTER = ('silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,areverse,'
          'silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB,areverse,'
          'dynaudnorm=f=150:g=15,apad=pad_dur=0.08')
def collect():
    r=[]
    for f in sorted(glob.glob(f'data/vocabulary-book-{book:02d}-chapter-*.json')):
        for w in json.load(open(f,encoding='utf-8'))['words']:
            r.append((w['sentence'], w['sentenceAudio']))
    return r
def gen(item):
    sent,dest=item; os.makedirs(os.path.dirname(dest),exist_ok=True)
    fd,aiff=tempfile.mkstemp(suffix='.aiff'); os.close(fd)
    try:
        subprocess.run(['say','-v','Alex','-r','175','-o',aiff,sent],check=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',aiff,'-af',FILTER,
                        '-codec:a','libmp3lame','-b:a','64k','-ar','22050','-ac','1',dest],check=True)
        return True
    except Exception: return False
    finally:
        if os.path.exists(aiff): os.remove(aiff)
items=collect(); print(f'book{book}: {len(items)} sentence clips...',flush=True)
with ThreadPoolExecutor(max_workers=6) as ex: res=list(ex.map(gen,items))
print(f'DONE {sum(res)}/{len(res)}')
