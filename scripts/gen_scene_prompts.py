#!/usr/bin/env python3
"""Write book-NN-scene-prompts.md for a docx/audio-sourced book from its
content module's SCENES, so the 30 placeholder webps can be replaced with real
illustrations generated elsewhere.  Usage: gen_scene_prompts.py <book> [...]"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

STYLE = ('Create a polished 16:9 landscape storybook illustration in warm classic gouache and watercolor, '
         'with soft paper texture, cinematic natural light and expressive but realistic faces. Keep the '
         'recurring children consistent: Jack is an 8-year-old boy with tousled dark hair and round black '
         'glasses; Annie is a 7-year-old girl with a brown ponytail.{extra} Adventurous and suitable for '
         'children ages 7–10. No text, no letters, no captions, no logo, no watermark, no frame, no gore.')

SETTINGS = {
    15: ' Setting: a monastery island off the coast of Ireland around A.D. 800, misty cliffs and a stormy '
        'North Atlantic with Viking longships; Annie wears a long coarse woolen dress and Jack a thick wool tunic '
        'and leggings with a leather bag.',
    16: ' Setting: ancient Olympia, Greece, around 400 B.C. during the Olympic Games; Jack and Annie wear '
        'simple belted Greek tunics and sandals.',
    17: ' Setting: the R.M.S. Titanic on the night of April 14–15, 1912, in the icy North Atlantic; Jack and '
        'Annie wear rain ponchos over pajamas and later bulky white life belts; Teddy is a small scruffy brown-and-tan terrier.',
    18: ' Setting: the Great Plains of North America in the early 1800s with a Lakota camp of tepees and vast '
        'buffalo herds; Jack and Annie wear simple buckskin clothing; Teddy is a small scruffy brown-and-tan terrier. '
        'Lakota people are portrayed respectfully and accurately.',
    19: ' Setting: a forest in India at twilight and dawn, with langur monkeys, elephants, a rhinoceros, a '
        'python and a Bengal tiger; Jack and Annie wear modern T-shirts and jeans; Teddy is a small scruffy brown-and-tan terrier.',
    20: ' Setting: the Australian bush with eucalyptus trees, kangaroos, a joey, koalas and dingoes, a sweeping '
        'wildfire and then pouring rain; Jack and Annie wear modern T-shirts and jeans; Teddy is a small scruffy '
        'brown-and-tan terrier. Aboriginal culture is portrayed respectfully.',
}


def write(book):
    content = importlib.import_module(f'book{book}_content')
    lines = [f'# Book {book} 插图提示词', '',
             '## 生成方式', '',
             '- 每张图的完整提示词 = 下方「统一前缀」+ ` Scene: ` + 对应的「场景提示」。',
             '- 30 张图各自独立生成，统一转成 1600×900 WebP，按文件名覆盖 '
             f'`assets/images/book-{book:02d}-scenes/` 下的占位图即可，无需改代码。', '',
             '## 统一前缀', '', STYLE.format(extra=SETTINGS[book]), '',
             '## 30 个场景提示', '']
    n = 0
    for ci, scenes in enumerate(content.SCENES):
        lines.append(f'### 第 {ci + 1} 章 · {content.TITLES[ci]}')
        lines.append('')
        for si, (title, desc) in enumerate(scenes):
            n += 1
            lines.append(f'{n}. `chapter-{ci + 1:02d}-scene-{si + 1:02d}.webp` — **{title}**：{desc}')
        lines.append('')
    target = ROOT / f'book-{book:02d}-scene-prompts.md'
    target.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{target.name}: {n} scenes')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        write(int(arg))
