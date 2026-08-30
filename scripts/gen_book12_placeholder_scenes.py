#!/usr/bin/env python3
"""Generate 1600x900 placeholder scene art for Book 11 (savanna palette + scene
title). Mirrors the Book 4 approach: real illustrations replace these later using
the briefs in book-12-scene-prompts.md."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from book12_content import SCENES, TITLES

OUT = ROOT / 'assets' / 'images' / 'book-12-scenes'
OUT.mkdir(parents=True, exist_ok=True)
FONT = '/System/Library/Fonts/STHeiti Light.ttc'
W, H = 1600, 900


def font(size):
    return ImageFont.truetype(FONT, size)


def gradient(top, bottom):
    base = Image.new('RGB', (1, H))
    px = base.load()
    for y in range(H):
        t = y / (H - 1)
        px[0, y] = tuple(round(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
    return base.resize((W, H))


def wrap(draw, text, fnt, max_width):
    lines, line = [], ''
    for ch in text:
        trial = line + ch
        if draw.textlength(trial, font=fnt) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines


def build(chapter_index, scene_index, title):
    # Warm savanna gold fading into dusk, tinted slightly per scene for variety.
    shift = (scene_index - 1) * 10
    img = gradient((200, 224, 240 - shift), (58, 86, 140))
    draw = ImageDraw.Draw(img)
    draw.rectangle([48, 48, W - 48, H - 48], outline=(235, 245, 252), width=3)
    tag = f'Book 12 · Polar Bears Past Bedtime'
    draw.text((80, 72), tag, font=font(34), fill=(20, 34, 66))
    draw.text((80, 128), f'第{chapter_index + 1}章 {TITLES[chapter_index]} · 场景 {scene_index + 1}',
              font=font(40), fill=(20, 34, 66))
    big = font(84)
    lines = wrap(draw, title, big, W - 200)
    total = len(lines) * 104
    y = (H - total) // 2 + 40
    for line in lines:
        w = draw.textlength(line, font=big)
        draw.text(((W - w) // 2, y), line, font=big, fill=(16, 28, 56))
        y += 104
    note = '插图生成中 · 占位图（真实插图见 book-12-scene-prompts.md）'
    draw.text((80, H - 96), note, font=font(30), fill=(40, 56, 92))
    dest = OUT / f'chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp'
    img.save(dest, 'WEBP', quality=82, method=6)


def main():
    for chapter_index in range(10):
        for scene_index, (title, _description) in enumerate(SCENES[chapter_index]):
            build(chapter_index, scene_index, title)
    print(f'wrote {len(list(OUT.glob("*.webp")))} placeholder scenes to {OUT}')


if __name__ == '__main__':
    main()
