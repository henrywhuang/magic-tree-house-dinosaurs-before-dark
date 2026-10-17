#!/usr/bin/env python3
"""Split a whole-book audiobook track (Books 17-24 collection: one ~37-min mp3 per
book) into 10 per-chapter mp3s + per-chapter ASR jsons.

The narrator announces each chapter ("Chapter One ...", "Chapter Two ..."), so we
ASR the whole track once (small.en), locate the ten "Chapter <ordinal>" markers in
the word stream to get chapter start times, then ffmpeg-split the audio and slice
the ASR (timestamps rebased to 0). Output matches the normal per-chapter pipeline:
assets/audio/book-NN-chapter-MM.mp3 and tmp/asr/bookNN-chMM.json.

Usage: split_wholebook_audio.py <book> <source_mp3>
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
ORDINALS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
# The narrator marks chapter starts inconsistently — a word ordinal OR a digit,
# and often SKIPS "Chapter One" (chapter 1 is simply the opening).  Accept both.
NUMWORDS = {k: {ORDINALS[k - 1], str(k)} for k in range(1, 11)}


def norm(w):
    return re.sub(r'[^a-z]', '', w.lower())


def whole_asr(book, source):
    cache = ROOT / 'tmp' / 'asr' / f'book{book}-whole.json'
    if cache.exists():
        return json.loads(cache.read_text())
    model = WhisperModel('small.en', device='cpu', compute_type='int8')
    segments, info = model.transcribe(
        str(source), language='en', word_timestamps=True,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
        beam_size=1, temperature=[0.0, 0.2, 0.4, 0.6],
        condition_on_previous_text=False, compression_ratio_threshold=2.2,
    )
    words = [{'word': w.word, 'start': round(w.start, 3), 'end': round(w.end, 3),
              'prob': round(w.probability, 3)} for s in segments for w in (s.words or [])]
    data = {'duration': round(info.duration, 2), 'words': words}
    cache.write_text(json.dumps(data, indent=1), encoding='utf-8')
    print(f'whole ASR: {len(words)} words, {info.duration:.0f}s', flush=True)
    return data


def find_chapter_starts(words):
    """Word index where each of the 10 chapters begins.  Chapter 1 starts at the
    top (the intro/first line); chapters 2-10 are located by the 'Chapter <n>'
    announcement, accepting either a word ordinal or a digit after 'chapter'."""
    low = [w['word'].strip().lower().strip('.,!?:;"“”') for w in words]
    starts = [0]  # chapter 1 = from the beginning (no "Chapter One" is announced)
    search_from = 1
    for k in range(2, 11):
        found = None
        for i in range(search_from, len(low) - 1):
            if low[i] == 'chapter' and low[i + 1] in NUMWORDS[k]:
                found = i
                break
        if found is None:
            raise RuntimeError(f'Chapter {k} marker ("chapter {k}") not found in ASR')
        starts.append(found)
        search_from = found + 1
    return starts


def main():
    book = int(sys.argv[1])
    source = Path(sys.argv[2])
    words = whole_asr(book, source)['words']
    starts = find_chapter_starts(words)
    boundaries = [round(words[i]['start'], 3) for i in starts] + [None]
    print('chapter start times:', [f'{t:.0f}s' for t in boundaries[:-1]], flush=True)
    for c in range(10):
        i0 = starts[c]
        i1 = starts[c + 1] if c + 1 < 10 else len(words)
        t0 = boundaries[c]
        t1 = boundaries[c + 1]
        # per-chapter mp3
        dst = ROOT / 'assets' / 'audio' / f'book-{book:02d}-chapter-{c + 1:02d}.mp3'
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source), '-ss', str(t0)]
        if t1 is not None:
            cmd += ['-to', str(t1)]
        cmd += ['-c', 'copy', str(dst)]
        subprocess.run(cmd, check=True)
        # per-chapter ASR json (timestamps rebased to 0)
        chunk = [{'word': w['word'], 'start': round(w['start'] - t0, 3),
                  'end': round(w['end'] - t0, 3), 'prob': w['prob']} for w in words[i0:i1]]
        dur = round((t1 if t1 is not None else words[-1]['end']) - t0, 2)
        (ROOT / 'tmp' / 'asr' / f'book{book}-ch{c + 1:02d}.json').write_text(
            json.dumps({'duration': dur, 'words': chunk}, indent=1), encoding='utf-8')
        print(f'  ch{c + 1:02d}: {t0:.0f}s-{t1 if t1 else "end"} ({len(chunk)} words)', flush=True)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
