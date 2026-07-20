#!/usr/bin/env python3
"""Generate Book 9 vocabulary sentence clips with local TTS."""
import glob
import json
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

FILTER = ('silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,areverse,'
          'silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB,areverse,'
          'dynaudnorm=f=150:g=15,apad=pad_dur=0.08')


def collect():
    result = []
    for filename in sorted(glob.glob('data/vocabulary-book-09-chapter-*.json')):
        data = json.load(open(filename, encoding='utf-8'))
        result.extend((word['sentence'], word['sentenceAudio']) for word in data['words'])
    return result


def generate(item):
    sentence, destination = item
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    descriptor, aiff = tempfile.mkstemp(suffix='.aiff')
    os.close(descriptor)
    try:
        subprocess.run(['say', '-v', 'Alex', '-r', '175', '-o', aiff, sentence], check=True)
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', aiff, '-af', FILTER,
            '-codec:a', 'libmp3lame', '-b:a', '64k', '-ar', '22050', '-ac', '1', destination,
        ], check=True)
        return destination, True
    except Exception:
        return destination, False
    finally:
        if os.path.exists(aiff):
            os.remove(aiff)


def main():
    items = collect()
    print(f'Generating {len(items)} Book 9 sentence clips...', flush=True)
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(generate, items))
    failures = [destination for destination, success in results if not success]
    print(f'DONE: {len(results) - len(failures)}/{len(results)} ok')
    if failures:
        raise SystemExit('\n'.join(failures[:20]))


if __name__ == '__main__':
    main()
