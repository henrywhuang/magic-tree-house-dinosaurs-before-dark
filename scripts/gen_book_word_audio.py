#!/usr/bin/env python3
"""Fill in click-to-play word clips for whole books: every story token, every
vocabulary headword and each token's dictionary lemma (data/words.js) that has
no assets/audio/words/<word>.mp3 yet.  The Qwen3 TTS weights are not kept in
the repo, so — like gen_missing_word_audio.py — this uses macOS `say -v Alex`
(American), 24000 Hz mono 64 kbps.
Usage: gen_book_word_audio.py <book> [<book> ...]"""
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS_DIR = ROOT / 'assets' / 'audio' / 'words'
AF = ('silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,areverse,'
      'silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB,areverse,'
      'dynaudnorm=f=150:g=15,apad=pad_dur=0.06')
VALID = re.compile(r"[a-z]+(?:['-][a-z]+)*")


def key(word):
    return re.sub(r"[^a-z'-]", '', str(word).lower().replace('’', "'").replace('‘', "'"))


def book_words(book):
    raw = (ROOT / 'data' / 'words.js').read_text(encoding='utf-8')
    dictionary = json.loads(re.fullmatch(r'\s*window\.WORDS=(.*);\s*', raw, re.S).group(1))
    words = set()
    for path in sorted((ROOT / 'data').glob(f'book-{book:02d}-chapter-*.json')):
        words.update(key(w['word']) for w in json.loads(path.read_text(encoding='utf-8'))['words'])
    for path in sorted((ROOT / 'data').glob(f'vocabulary-book-{book:02d}-chapter-*.json')):
        words.update(key(w['word']) for w in json.loads(path.read_text(encoding='utf-8'))['words'])
    words.update(key(dictionary.get(w, {}).get('lemma', '')) for w in list(words))
    return {w for w in words if VALID.fullmatch(w)}


def generate(word):
    dest = WORDS_DIR / f'{word}.mp3'
    fd, aiff = tempfile.mkstemp(suffix='.aiff')
    os.close(fd)
    try:
        subprocess.run(['say', '-v', 'Alex', '-r', '160', '-o', aiff, word], check=True)
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', aiff, '-af', AF,
                        '-codec:a', 'libmp3lame', '-b:a', '64k', '-ar', '24000', '-ac', '1', str(dest)], check=True)
        return word, True
    except Exception:
        return word, False
    finally:
        if os.path.exists(aiff):
            os.remove(aiff)


def main():
    books = [int(b) for b in sys.argv[1:]]
    if not books:
        raise SystemExit(__doc__)
    wanted = set().union(*(book_words(b) for b in books))
    missing = sorted(w for w in wanted if not (WORDS_DIR / f'{w}.mp3').exists())
    print(f'books {books}: {len(wanted)} words, generating {len(missing)} missing clips...', flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(generate, missing))
    failed = [w for w, ok in results if not ok]
    print(f'DONE {len(results) - len(failed)}/{len(results)}')
    if failed:
        raise SystemExit('failed: ' + ' '.join(failed[:30]))


if __name__ == '__main__':
    main()
