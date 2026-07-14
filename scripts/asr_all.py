#!/usr/bin/env python3
"""Transcribe given Book1 chapters with faster-whisper large-v3 -> word-level JSON (model loaded once)."""
import sys, json
from faster_whisper import WhisperModel
chapters = [int(c) for c in sys.argv[1:]]
model = WhisperModel("large-v3", device="cpu", compute_type="int8")
for c in chapters:
    mp3=f"assets/audio/chapter-{c:02d}.mp3"; out=f"tmp/asr/ch{c:02d}.json"
    segments, info = model.transcribe(mp3, language="en", word_timestamps=True,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
        beam_size=5, temperature=0.0,
        initial_prompt="A chapter from the Magic Tree House children's book, American English narration.")
    words=[{"word":w.word,"start":round(w.start,3),"end":round(w.end,3),"prob":round(w.probability,3)}
           for seg in segments for w in (seg.words or [])]
    json.dump({"duration":round(info.duration,2),"words":words}, open(out,"w"), ensure_ascii=False, indent=1)
    print(f"{out}: {len(words)} words, dur {info.duration:.1f}s", flush=True)
print("ALL ASR DONE", flush=True)
