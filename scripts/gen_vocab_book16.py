#!/usr/bin/env python3
"""Book 16 vocabulary cards. OVERRIDES fix ECDICT wrong headword/pos/meaning."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gen_vocab_docx_book

OVERRIDES = {
    'sacred': {'pos': 'adj.', 'meaning': '神圣的；宗教的'},
    'soldier': {'pos': 'n.', 'meaning': '士兵；军人'},

    # ch01
    'journeys': {'word': 'journey', 'pos': 'n.', 'meaning': '旅程；旅行'},
    'rustling': {'word': 'rustle', 'pos': 'v.', 'meaning': '沙沙作响；发出沙沙声'},
    'brave': {'pos': 'adj.', 'meaning': '勇敢的；无畏的'},
    'mission': {'pos': 'n.', 'meaning': '任务；使命'},
    # ch02
    'crowds': {'word': 'crowd', 'pos': 'n.', 'meaning': '人群；群众'},
    'theater': {'pos': 'n.', 'meaning': '剧场；戏院'},
    'stage': {'pos': 'n.', 'meaning': '舞台；戏台'},
    'cape': {'pos': 'n.', 'meaning': '斗篷；披风'},
    'wig': {'pos': 'n.', 'meaning': '假发；假发套'},
    # ch03
    'puzzled': {'pos': 'adj.', 'meaning': '困惑的；迷惑不解的'},
    'brilliant': {'pos': 'adj.', 'meaning': '才华横溢的；杰出的'},
    # ch04
    'promise': {'pos': 'v.', 'meaning': '承诺；保证'},
    'bowed': {'word': 'bow', 'pos': 'v.', 'meaning': '鞠躬；弯腰'},
    'grumbled': {'word': 'grumble', 'pos': 'v.', 'meaning': '抱怨；发牢骚'},
    'sighed': {'word': 'sigh', 'pos': 'v.', 'meaning': '叹气；叹息'},
    'citizens': {'word': 'citizen', 'pos': 'n.', 'meaning': '公民；市民'},
    # ch05
    'statue': {'pos': 'n.', 'meaning': '雕像；塑像'},
    'sacred': {'pos': 'adj.', 'meaning': '神圣的；神圣不可侵犯的'},
    'athletes': {'word': 'athlete', 'pos': 'n.', 'meaning': '运动员；运动选手'},
    'temple': {'pos': 'n.', 'meaning': '神庙；庙宇'},
    # ch06
    'armor': {'pos': 'n.', 'meaning': '盔甲；铠甲'},
    'cheering': {'word': 'cheer', 'pos': 'v.', 'meaning': '欢呼；喝彩'},
    'judges': {'word': 'judge', 'pos': 'n.', 'meaning': '裁判；裁判员'},
    'boxers': {'word': 'boxer', 'pos': 'n.', 'meaning': '拳击手'},
    'wrestlers': {'word': 'wrestler', 'pos': 'n.', 'meaning': '摔跤手；摔跤选手'},
    'soldier': {'pos': 'n.', 'meaning': '士兵；军人'},
    # ch07
    'glared': {'word': 'glare', 'pos': 'v.', 'meaning': '怒视；瞪眼'},
    'pigtails': {'word': 'pigtail', 'pos': 'n.', 'meaning': '辫子；发辫'},
    'guards': {'word': 'guard', 'pos': 'n.', 'meaning': '卫兵；警卫'},
    # ch08
    'arrest': {'pos': 'v.', 'meaning': '逮捕；拘捕'},
    'galloped': {'word': 'gallop', 'pos': 'v.', 'meaning': '疾驰；飞奔'},
    'murmured': {'word': 'murmur', 'pos': 'v.', 'meaning': '低声说；私语'},
    # ch09
    'reared': {'word': 'rear', 'pos': 'v.', 'meaning': '（马）用后腿直立；腾起'},
    'wings': {'word': 'wing', 'pos': 'n.', 'meaning': '翅膀；翼'},
    'stroked': {'word': 'stroke', 'pos': 'v.', 'meaning': '抚摸；轻抚'},
    # ch10
    'serpent': {'pos': 'n.', 'meaning': '蛇；巨蛇'},
    'shimmering': {'pos': 'adj.', 'meaning': '闪着微光的；闪烁的'},
    'glowed': {'word': 'glow', 'pos': 'v.', 'meaning': '发光；发亮'},
    'trust': {'pos': 'v.', 'meaning': '信任；信赖'},
    'relief': {'pos': 'n.', 'meaning': '宽慰；如释重负'},
}

if __name__ == '__main__':
    gen_vocab_docx_book.run(16, OVERRIDES)
