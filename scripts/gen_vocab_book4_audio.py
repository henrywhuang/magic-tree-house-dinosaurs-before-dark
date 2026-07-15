#!/usr/bin/env python3
"""Generate Book4 vocabulary sentence audio via macOS `say -v Alex` (American),
matching the Book1-3 sentence clips (22050 Hz mono mp3). Reads sentence + dest
path straight from data/vocabulary-book-04-chapter-NN.json so paths stay in sync.
Usage: gen_vocab_book4_audio.py [voice] [rate] [--overwrite]"""
import glob, os, json, subprocess, tempfile, sys
from concurrent.futures import ThreadPoolExecutor

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
VOICE = ARGS[0] if len(ARGS) > 0 else "Alex"
RATE = ARGS[1] if len(ARGS) > 1 else "175"
OVERWRITE = '--overwrite' in sys.argv
AF = ("silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,areverse,"
      "silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB,areverse,"
      "dynaudnorm=f=150:g=15,apad=pad_dur=0.08")

def collect():
    items = []
    for f in sorted(glob.glob("data/vocabulary-book-04-chapter-*.json")):
        v = json.load(open(f, encoding="utf-8"))
        for w in v["words"]:
            items.append((w["sentence"], w["sentenceAudio"]))
    return items

def gen(item):
    sentence, dest = item
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and not OVERWRITE:
        return (dest, True)
    fd, aiff = tempfile.mkstemp(suffix=".aiff"); os.close(fd)
    try:
        subprocess.run(["say", "-v", VOICE, "-r", RATE, "-o", aiff, sentence], check=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", aiff, "-af", AF,
                        "-codec:a", "libmp3lame", "-b:a", "64k", "-ar", "22050", "-ac", "1", dest], check=True)
        return (dest, True)
    except Exception:
        return (dest, False)
    finally:
        if os.path.exists(aiff):
            os.remove(aiff)

items = collect()
print(f"generating {len(items)} sentence clips with macOS {VOICE} (rate {RATE}, overwrite={OVERWRITE})...", flush=True)
results = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for i, r in enumerate(ex.map(gen, items), 1):
        results.append(r)
        if i % 25 == 0:
            print(f"  {i}/{len(items)}", flush=True)
fails = [r[0] for r in results if not r[1]]
print(f"DONE: {len(results) - len(fails)}/{len(results)} ok, {len(fails)} failed", flush=True)
if fails:
    print("  FAILS:", fails[:20])
