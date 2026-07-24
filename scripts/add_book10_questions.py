#!/usr/bin/env python3
"""Append the reviewed Book 10 question set from the supplied assessment DOCX."""
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / '神奇树屋1-10册_英文阅读理解选择题_能力导向版_含答案.docx'
TARGET = ROOT / 'data' / 'questions.json'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
ANSWERS = [
    list('CDCAC'), list('DBACB'), list('ACAAA'), list('ABCAC'), list('BDCCC'),
    list('ACDAB'), list('AADAC'), list('ACDDB'), list('DDADD'), list('BCDBB'),
]
META = {
    'DETAIL': ('RL.5.1', 'Explicit comprehension', 1, '基础'),
    'SEQUENCE': ('RL.5.3', 'Sequence', 2, '进阶'),
    'PLOT RELATION': ('RL.5.3', 'Character/event relationship', 2, '进阶'),
    'VOCABULARY IN CONTEXT': ('RL.5.4', 'Vocabulary in context', 1, '基础'),
    'SUMMARY': ('RL.5.2', 'Summary', 2, '进阶'),
    'INFERENCE': ('RL.5.1', 'Evidence-based inference', 2, '进阶'),
    'CAUSE / PURPOSE / RESULT': ('RL.5.3', 'Cause / purpose / result', 2, '进阶'),
}


def paragraphs():
    with ZipFile(DOCX) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
    result = []
    for paragraph in root.findall('.//w:p', NS):
        text = ''.join(node.text or '' for node in paragraph.findall('.//w:t', NS)).strip()
        if text:
            result.append(text)
    return result


def parse_options(text):
    matches = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.\s)|$)', text)
    if len(matches) != 4:
        raise RuntimeError(f'Cannot parse options: {text}')
    return dict(matches)


def evidence_for(stem, correct):
    for label in ('Sentence:', 'Evidence:'):
        if label in stem:
            return [stem.split(label, 1)[1].strip()]
    earlier = re.search(r'Earlier event:\s*(.+)$', stem)
    return ([earlier.group(1)] if earlier else []) + [correct]


def rationale_for(tag, correct):
    if tag == 'VOCABULARY IN CONTEXT':
        return f'结合原句语境，这个词在这里最接近“{correct}”。'
    if tag == 'SEQUENCE':
        return f'按照本章事件先后顺序，最先发生的是：{correct}'
    if tag == 'SUMMARY':
        return f'这个选项同时保留了本章开端与后续的关键事件：{correct}'
    if tag == 'INFERENCE':
        return f'原文细节支持这一推断：{correct}'
    if tag == 'PLOT RELATION':
        return f'在题干给出的较早事件之后，故事接着发生了：{correct}'
    if tag == 'CAUSE / PURPOSE / RESULT':
        return f'结合事件的原因、目的或结果，正确关系是：{correct}'
    return f'原文直接写到：{correct}'


def build_book():
    items = paragraphs()
    start = next(index for index, text in enumerate(items) if text == 'Book 10  |  Ghost Town at Sundown')
    stop = next(index for index in range(start + 1, len(items)) if items[index].startswith('Answer Key'))
    section = items[start:stop]
    chapters = []
    cursor = 2
    for chapter_number in range(1, 11):
        header = section[cursor]
        match = re.fullmatch(rf'Chapter {chapter_number}\s+\|\s+(.+)', header)
        if not match:
            raise RuntimeError(f'Unexpected chapter header: {header}')
        title = match.group(1)
        cursor += 1
        questions = []
        for question_number in range(1, 6):
            question_text, option_text = section[cursor], section[cursor + 1]
            cursor += 2
            match = re.fullmatch(rf'Q{question_number}\.\s+\[([^]]+)]\s+(.+)', question_text)
            if not match:
                raise RuntimeError(f'Unexpected question: {question_text}')
            tag, stem = match.groups()
            options = parse_options(option_text)
            answer = ANSWERS[chapter_number - 1][question_number - 1]
            standard, skill, dok, difficulty = META[tag]
            questions.append({
                'number': question_number, 'standard': standard, 'skill': skill, 'dok': dok,
                'stem': stem, 'options': options, 'answer': answer,
                'evidence': evidence_for(stem, options[answer]),
                'rationale': rationale_for(tag, options[answer]),
                'id': f'B10C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 10, 'chapter': chapter_number, 'chapter_title': title, 'questions': questions})
    return {'book': 10, 'book_title': 'Ghost Town at Sundown', 'book_title_cn': '孤独的牛仔', 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 10] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 10 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
