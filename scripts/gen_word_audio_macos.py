#!/usr/bin/env python3
"""Generate dictionary pronunciations for every word via macOS `say`.
Usage: gen_word_audio_macos.py [voice] [rate]   (default: Alex 160, American English)"""
import glob, os, subprocess, tempfile, sys
from concurrent.futures import ThreadPoolExecutor
VOICE = sys.argv[1] if len(sys.argv) > 1 else "Alex"
RATE  = sys.argv[2] if len(sys.argv) > 2 else "160"
WORDS_DIR = "assets/audio/words"
AF = ("silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,areverse,"
      "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB,areverse,"
      "dynaudnorm=f=150:g=15,apad=pad_dur=0.06")
def gen(path):
    w = os.path.splitext(os.path.basename(path))[0]
    fd, aiff = tempfile.mkstemp(suffix=".aiff"); os.close(fd)
    try:
        subprocess.run(["say","-v",VOICE,"-r",RATE,"-o",aiff,w], check=True)
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",aiff,"-af",AF,
                        "-codec:a","libmp3lame","-b:a","64k","-ar","24000","-ac","1",path], check=True)
        return (w, True)
    except Exception as e:
        return (w, False)
    finally:
        if os.path.exists(aiff): os.remove(aiff)
files = sorted(glob.glob(f"{WORDS_DIR}/*.mp3"))
print(f"generating {len(files)} words with macOS {VOICE} (rate {RATE})...", flush=True)
results=[]
with ThreadPoolExecutor(max_workers=6) as ex:
    for i,r in enumerate(ex.map(gen, files),1):
        results.append(r)
        if i%300==0: print(f"  {i}/{len(files)}", flush=True)
fails=[r[0] for r in results if not r[1]]
print(f"DONE: {len(results)-len(fails)}/{len(results)} ok, {len(fails)} failed", flush=True)
if fails: print("  FAILS:", fails[:20])
