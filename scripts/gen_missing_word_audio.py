#!/usr/bin/env python3
"""Ensure every vocabulary headword (item.word, all books) has a click-to-play
word clip at assets/audio/words/<word>.mp3. Generates only the missing ones via
macOS `say -v Alex` (American), 24000 Hz mono — matching the existing word audio.
Usage: gen_missing_word_audio.py [voice] [rate]"""
import glob, os, json, subprocess, tempfile, sys
from concurrent.futures import ThreadPoolExecutor

VOICE = sys.argv[1] if len(sys.argv) > 1 else "Alex"
RATE = sys.argv[2] if len(sys.argv) > 2 else "160"
WORDS_DIR = "assets/audio/words"
AF = ("silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,areverse,"
      "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB,areverse,"
      "dynaudnorm=f=150:g=15,apad=pad_dur=0.06")

def needed():
    words = set()
    for f in glob.glob("data/vocabulary-book-0*-chapter-*.json"):
        for w in json.load(open(f, encoding="utf-8"))["words"]:
            words.add(w["word"].lower())
    return sorted(w for w in words if not os.path.exists(f"{WORDS_DIR}/{w}.mp3"))

def gen(w):
    dest = f"{WORDS_DIR}/{w}.mp3"
    fd, aiff = tempfile.mkstemp(suffix=".aiff"); os.close(fd)
    try:
        subprocess.run(["say", "-v", VOICE, "-r", RATE, "-o", aiff, w], check=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", aiff, "-af", AF,
                        "-codec:a", "libmp3lame", "-b:a", "64k", "-ar", "24000", "-ac", "1", dest], check=True)
        return (w, True)
    except Exception:
        return (w, False)
    finally:
        if os.path.exists(aiff):
            os.remove(aiff)

miss = needed()
print(f"generating {len(miss)} missing word clips with macOS {VOICE} (rate {RATE})...", flush=True)
results = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for i, r in enumerate(ex.map(gen, miss), 1):
        results.append(r)
        if i % 25 == 0:
            print(f"  {i}/{len(miss)}", flush=True)
fails = [r[0] for r in results if not r[1]]
print(f"DONE: {len(results) - len(fails)}/{len(results)} ok, {len(fails)} failed", flush=True)
if fails:
    print("  FAILS:", fails)
