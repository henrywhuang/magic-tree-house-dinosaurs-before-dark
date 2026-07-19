#!/usr/bin/env python3
"""Build Book 6 reader JSON from proofread OCR and ASR timestamps."""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tmp' / 'verify'))
sys.path.insert(0, str(ROOT / 'scripts'))
import rekey
from book6_content import SCENE_ANCHORS, SCENES, TITLES, VOCABULARY

SOURCE = ROOT / '6.亚马孙探险.pdf_by_PaddleOCR-VL-1.6.json'
CHAPTER_STARTS = [7, 12, 18, 25, 35, 44, 51, 58, 66, 75]
STORY_END = 88


def norm_match(word):
    return re.sub(r'[^a-z]', '', word.lower())


def clean_story(markdown):
    for marker in ('课标单词', '单词表', '常用结构', 'Directions:'):
        pos = markdown.find(marker)
        if pos >= 0:
            markdown = markdown[:pos]
    markdown = re.sub(r'<div[^>]*>.*?</div>', ' ', markdown, flags=re.S)
    markdown = re.sub(r'<img[^>]*>', ' ', markdown)
    lines = []
    for line in markdown.splitlines():
        text = line.strip()
        if not text:
            continue
        # English story pages are followed by bilingual vocabulary/example panels.
        # Once Chinese appears, the remaining page content is no longer story text.
        if re.search(r'[\u3400-\u9fff]', text):
            if re.search(r'[A-Za-z]', text):
                break
            continue
        if text.startswith('#'):
            text = text.lstrip('#').strip()
            if re.match(r'^Chapter\s+\d+', text, re.I):
                continue
            if len(text) <= 25 and not re.search(r'[.!?,"“”]', text):
                continue
        lines.append(text)
    return '\n'.join(lines)


def chapter_text(pages, chapter_index):
    lo = CHAPTER_STARTS[chapter_index]
    hi = CHAPTER_STARTS[chapter_index + 1] if chapter_index < 9 else STORY_END
    text = '\n'.join(clean_story(pages[index]['markdown']['text']) for index in range(lo, hi))
    text = text.replace('…', '...').replace('——', '—')
    # PaddleOCR sometimes keeps a printed line/page break inside one sentence.
    # Join hyphenated wraps without a space and ordinary lowercase continuations
    # with one space, while preserving real paragraph/dialogue boundaries.
    text = re.sub(r'([A-Za-z])-\n([a-z])', r'\1\2', text)
    text = re.sub(r'([A-Za-z])\n([a-z])', r'\1 \2', text)
    text = text.replace('Atlantic\nOcean', 'Atlantic Ocean')
    # Page boundaries can leave an empty line between the two halves, so make a
    # second pass over non-empty lines and merge the same lowercase continuation.
    merged = []
    for line in (part.strip() for part in text.splitlines() if part.strip()):
        if merged and line[:1].islower() and re.search(r'[A-Za-z]$', merged[-1]):
            merged[-1] += ' ' + line
        elif merged and line[:1].islower() and re.search(r'[A-Za-z]-$', merged[-1]):
            merged[-1] = merged[-1][:-1] + line
        elif merged and line[:1].islower() and merged[-1].endswith('—'):
            merged[-1] += ' ' + line
        else:
            merged.append(line)
    text = '\n'.join(merged)
    text = re.sub(r'(?m)^The� forest is in four layers\.\n?', '', text)
    return strip_title(text, chapter_index)


def strip_title(text, chapter_index):
    lines = text.splitlines()
    while lines and (not norm_match(lines[0]) or norm_match(lines[0]) in {
        norm_match(TITLES[chapter_index]), 'chapter', f'chapter{chapter_index + 1}'
    }):
        lines.pop(0)
    return '\n'.join(lines)


def tokenize_paragraph(paragraph):
    tokens = list(re.finditer(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", paragraph))
    words, position = [], 0
    for token in tokens:
        start, end = token.span()
        after_end = end
        while after_end < len(paragraph) and not paragraph[after_end].isspace() and not paragraph[after_end].isalnum():
            after_end += 1
        words.append({'word': token.group(), 'before': paragraph[position:start], 'after': paragraph[end:after_end]})
        position = after_end
    return words


def ocr_words(pages, chapter_index):
    paragraphs = [line for line in chapter_text(pages, chapter_index).splitlines() if line.strip()]
    words = []
    for paragraph_index, paragraph in enumerate(paragraphs):
        for word in tokenize_paragraph(paragraph):
            word['para'] = paragraph_index
            words.append(word)
    return words, paragraphs


def assign_timestamps(words, asr_words):
    ocr = [norm_match(word['word']) for word in words]
    asr = [norm_match(word['word']) for word in asr_words]
    for word in words:
        word['start'] = word['end'] = None
    matcher = difflib.SequenceMatcher(None, ocr, asr, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for offset in range(i2 - i1):
                words[i1 + offset]['start'] = float(asr_words[j1 + offset]['start'])
                words[i1 + offset]['end'] = float(asr_words[j1 + offset]['end'])
    anchors = [index for index, word in enumerate(words) if word['start'] is not None]
    if not anchors:
        raise RuntimeError('No OCR/ASR alignment anchors')
    first, last = anchors[0], anchors[-1]
    for index in range(first):
        words[index]['start'] = max(0.0, words[first]['start'] - (first - index) * 0.28)
        words[index]['end'] = words[index]['start'] + 0.26
    for index in range(last + 1, len(words)):
        words[index]['start'] = words[last]['end'] + (index - last - 1) * 0.30
        words[index]['end'] = words[index]['start'] + 0.28
    index = first
    while index <= last:
        if words[index]['start'] is not None:
            index += 1
            continue
        previous = index - 1
        following = index
        while following <= last and words[following]['start'] is None:
            following += 1
        t0, t1 = words[previous]['end'], words[following]['start']
        gap, count = max(0.0, t1 - t0), following - index
        for offset in range(count):
            start = t0 + gap * (offset + 1) / (count + 1)
            words[index + offset]['start'] = start
            words[index + offset]['end'] = min(t1, start + gap / (count + 1))
        index = following
    for index in range(1, len(words)):
        if words[index]['start'] < words[index - 1]['start']:
            words[index]['start'] = words[index - 1]['start']
            words[index]['end'] = max(words[index]['end'], words[index]['start'] + 0.1)
    for word in words:
        word['start'] = round(word['start'], 3)
        word['end'] = round(word['end'], 3)


def extract_vocab(pages, chapter_index):
    return VOCABULARY[chapter_index]


def extract_vocab_from_ocr(pages, chapter_index):
    """Diagnostic fallback retained for comparing OCR panels with the proofread list."""
    lo = CHAPTER_STARTS[chapter_index]
    hi = CHAPTER_STARTS[chapter_index + 1] if chapter_index < 9 else STORY_END
    standard, extension = [], []
    for index in range(lo, hi):
        markdown = pages[index]['markdown']['text']
        pos = markdown.find('课标单词')
        if pos < 0:
            continue
        region = markdown[pos + len('课标单词'):]
        end = region.find('单词表')
        if end >= 0:
            region = region[:end]
        split = region.find('拓展单词')
        common = region.find('常用结构')
        standard_region = region[:min(x for x in (split, common, len(region)) if x >= 0)]
        extension_region = region[split + len('拓展单词'):common if common >= 0 else len(region)] if split >= 0 else ''
        standard.extend(parse_vocab_entries(standard_region))
        extension.extend(parse_vocab_entries(extension_region))
    return standard, extension


def parse_vocab_entries(region):
    region = re.sub(r'<[^>]+>', ' ', region).replace('\n', '；')
    result = []
    for part in re.split(r'[；;]', region):
        match = re.match(r"\s*([A-Za-z][A-Za-z '\-]*?)(?=[\u3400-\u9fff]|$)", part)
        if match:
            word = match.group(1).strip()
            if 0 < len(word.split()) <= 3:
                result.append(word)
    return result


def apply_keywords(words, vocab):
    tokens, used = [word['word'] for word in words], set()
    for phrase in [item for item in vocab if ' ' in item]:
        used.update(rekey.find_phrase(tokens, phrase, used))
    remaining = []
    for item in [item for item in vocab if ' ' not in item]:
        found = rekey.find_first(tokens, item, used, exact_only=True)
        if found >= 0:
            used.add(found)
        else:
            remaining.append(item)
    for item in remaining:
        found = rekey.find_first(tokens, item, used, exact_only=False)
        if found >= 0:
            used.add(found)
    for index, word in enumerate(words):
        word['key'] = index in used


def scene_boundaries(paragraphs, chapter_index):
    boundaries = []
    for anchor in SCENE_ANCHORS[chapter_index]:
        boundary = next((index for index, paragraph in enumerate(paragraphs) if anchor in paragraph), None)
        if boundary is None:
            raise RuntimeError(f'Chapter {chapter_index + 1}: scene anchor not found: {anchor}')
        boundaries.append(boundary)
    return boundaries


def build_chapter(pages, chapter_index):
    words, paragraphs = ocr_words(pages, chapter_index)
    asr = json.loads((ROOT / 'tmp' / 'asr' / f'book6-ch{chapter_index + 1:02d}.json').read_text())
    assign_timestamps(words, asr['words'])
    standard, extension = extract_vocab(pages, chapter_index)
    apply_keywords(words, standard + extension)
    first, second = scene_boundaries(paragraphs, chapter_index)
    for word in words:
        word['page'] = 0 if word['para'] < first else 1 if word['para'] < second else 2
    flat = [
        {'i': index, 'word': word['word'], 'before': word['before'], 'after': word['after'],
         'start': word['start'], 'end': word['end'], 'key': word['key'], 'page': word['page']}
        for index, word in enumerate(words)
    ]
    output_pages = []
    for page in range(3):
        grouped = {}
        for index, word in enumerate(words):
            if word['page'] == page:
                grouped.setdefault(word['para'], []).append(flat[index])
        output_pages.append([{'words': grouped[key]} for key in sorted(grouped)])
    scenes = [
        [title, f'assets/images/book-06-scenes/chapter-{chapter_index + 1:02d}-scene-{scene_index + 1:02d}.webp', description]
        for scene_index, (title, description) in enumerate(SCENES[chapter_index])
    ]
    return {'chapter': chapter_index + 1, 'scenes': scenes, 'words': flat, 'pages': output_pages}


def main():
    pages = json.loads(SOURCE.read_text(encoding='utf-8'))
    for chapter_index in range(10):
        data = build_chapter(pages, chapter_index)
        target = ROOT / 'data' / f'book-06-chapter-{chapter_index + 1:02d}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        keys = sum(1 for word in data['words'] if word['key'])
        print(f'{target.name}: {len(data["words"])} words, {keys} key words, 3 scenes')


if __name__ == '__main__':
    main()
