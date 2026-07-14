#!/usr/bin/env python3
"""Transcribe a Book1 chapter mp3 with faster-whisper large-v3 -> word-level JSON."""
import sys, json
from faster_whisper import WhisperModel
mp3, out = sys.argv[1], sys.argv[2]
model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    mp3, language="en", word_timestamps=True,
    vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
    beam_size=5, temperature=0.0,
    condition_on_previous_text=True,
    initial_prompt="A chapter from the Magic Tree House children's book, American English narration.",
)
words=[]
for seg in segments:
    for w in (seg.words or []):
        words.append({"word": w.word, "start": round(w.start,3), "end": round(w.end,3), "prob": round(w.probability,3)})
json.dump({"language":info.language,"duration":round(info.duration,2),"words":words}, open(out,"w"), ensure_ascii=False, indent=1)
print(f"{out}: {len(words)} words, dur {info.duration:.1f}s")
