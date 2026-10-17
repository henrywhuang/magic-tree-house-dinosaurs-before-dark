#!/usr/bin/env python3
"""Generate 1600x900 placeholder scene art for a docx-sourced book.
Usage: gen_placeholder_scenes.py <book_number>
Palette + book label are looked up from BOOKS below."""
import importlib
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
FONT = '/System/Library/Fonts/STHeiti Light.ttc'
W, H = 1600, 900

# book -> (english label, top RGB, bottom RGB, heading RGB, body RGB)
BOOKS = {
    13: ('Book 13 · Vacation Under the Volcano', (226, 176, 138), (120, 58, 40), (54, 24, 12), (36, 18, 10)),
    14: ('Book 14 · Day of the Dragon King', (232, 196, 120), (140, 40, 40), (60, 20, 16), (40, 14, 12)),
    15: ('Book 15 · Viking Ships at Sunrise', (196, 214, 226), (40, 74, 110), (16, 32, 54), (14, 28, 48)),
    16: ('Book 16 · Hour of the Olympics', (230, 214, 178), (150, 120, 60), (52, 40, 16), (36, 28, 12)),
    17: ('Book 17 · Tonight on the Titanic', (150, 170, 200), (24, 40, 74), (14, 24, 48), (12, 20, 44)),
    18: ('Book 18 · Buffalo Before Breakfast', (216, 196, 140), (120, 96, 50), (52, 40, 18), (38, 28, 12)),
    19: ('Book 19 · Tigers at Twilight', (170, 182, 130), (52, 70, 40), (24, 34, 16), (18, 28, 12)),
    20: ('Book 20 · Dingoes at Dinnertime', (224, 170, 120), (140, 74, 44), (60, 30, 16), (44, 22, 12)),
}


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
        if draw.textlength(line + ch, font=fnt) <= max_width or not line:
            line += ch
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines


def main():
    book = int(sys.argv[1])
    label, top, bottom, head_rgb, body_rgb = BOOKS[book]
    content = importlib.import_module(f'book{book}_content')
    out = ROOT / 'assets' / 'images' / f'book-{book:02d}-scenes'
    out.mkdir(parents=True, exist_ok=True)
    for ci in range(10):
        for si, (title, _desc) in enumerate(content.SCENES[ci]):
            shift = (si - 1) * 8
            img = gradient(tuple(min(255, c + shift) for c in top), bottom)
            draw = ImageDraw.Draw(img)
            draw.rectangle([48, 48, W - 48, H - 48], outline=(245, 245, 240), width=3)
            draw.text((80, 72), label, font=font(34), fill=head_rgb)
            draw.text((80, 128), f'第{ci + 1}章 {content.TITLES[ci]} · 场景 {si + 1}', font=font(38), fill=head_rgb)
            big = font(84)
            lines = wrap(draw, title, big, W - 200)
            y = (H - len(lines) * 104) // 2 + 40
            for line in lines:
                w = draw.textlength(line, font=big)
                draw.text(((W - w) // 2, y), line, font=big, fill=body_rgb)
                y += 104
            note = f'插图生成中 · 占位图（真实插图见 book-{book:02d}-scene-prompts.md）'
            draw.text((80, H - 96), note, font=font(30), fill=body_rgb)
            img.save(out / f'chapter-{ci + 1:02d}-scene-{si + 1:02d}.webp', 'WEBP', quality=82, method=6)
    print(f'book{book}: wrote {len(list(out.glob("*.webp")))} placeholder scenes')


if __name__ == '__main__':
    main()
