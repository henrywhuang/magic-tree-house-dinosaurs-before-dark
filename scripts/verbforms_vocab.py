#!/usr/bin/env python3
"""Rewrite VERB vocabulary entries (all books) to base-form (原形) headwords and
present the verb's inflections in 常见词形. Data-only — the app already renders
`word` as the headword, shows 原文：<tapped form> when they differ, and prints
`wordForms` under the 常见词形 label.

For each entry whose partOfSpeech starts with 'v':
  word      -> base form / lemma            (ECDICT exchange 0:, else surface)
  phonetic  -> base form's phonetic
  phonics   -> re-segment the base form     (core words only)
  wordForms -> 第三人称单数 X · 过去式 Y · 现在分词 Z   (ECDICT 3:/p:/i:, rule fallback)
  forms     -> [surface, base, 3sg, past, ing]  (any inflection in the text still links)
Nouns / adjectives / adverbs are left untouched.
"""
import json, re, glob, sys
sys.path.insert(0, 'scripts')
from gen_vocab_book4 import base_forms, load_ecdict, get_phonetic, phonics

def exch(word, ec):
    row = ec.get(word.lower()); d = {}
    if row:
        for part in (row.get('exchange') or '').split('/'):
            if ':' in part:
                k, val = part.split(':', 1); d[k] = val
    return d

def rule_third(w):
    if re.search(r'(s|x|z|ch|sh)$', w): return w + 'es'
    if re.search(r'[^aeiou]y$', w): return w[:-1] + 'ies'
    return w + 's'

def rule_ing(w):
    if w.endswith('ie'): return w[:-2] + 'ying'
    if w.endswith('e') and not re.search(r'(ee|ye|oe)$', w) and len(w) > 2: return w[:-1] + 'ing'
    if re.search(r'[^aeiou][aeiou][^aeiouwxy]$', w) and len(w) <= 5: return w + w[-1] + 'ing'
    return w + 'ing'

def rule_past(w):
    if w.endswith('e'): return w + 'd'
    if re.search(r'[^aeiou]y$', w): return w[:-1] + 'ied'
    if re.search(r'[^aeiou][aeiou][^aeiouwxy]$', w) and len(w) <= 5: return w + w[-1] + 'ed'
    return w + 'ed'

def is_verb(pos):
    return pos.strip().lower().startswith('v')

def lemma_candidates(surface):
    """Possible base forms to probe, incl. doubled-consonant fix for ECDICT's
    bad lemmas (strolled->0:strol, but real headword is 'stroll')."""
    s = surface.lower(); out = []
    def add(x):
        if x and x not in out: out.append(x)
    add(s)
    for b in base_forms(s):
        add(b)
    return out

def is_base_verb(word, ec):
    ce = exch(word, ec)
    return bool(ce.get('i') or ce.get('3') or ce.get('p'))

def resolve_lemma(surface, ec):
    """True base verb for `surface`, or None if it isn't a conjugatable verb.
    Prefers a DIFFERENT, shorter base whose inflections include the surface —
    ECDICT self-references participial adjectives (interesting->0:interesting),
    so matching the surface to itself must come last."""
    s = surface.lower()
    other = []              # candidate bases that are not the surface
    e0 = exch(s, ec).get('0')
    if e0 and e0 != s:
        other.append(e0)
        if e0[-1] not in 'aeiou':
            other.append(e0 + e0[-1])          # strolled: 0:strol -> stroll
    for c in base_forms(s):
        if c != s and c not in other:
            other.append(c)
    # 1) a real base verb (≠ surface) whose inflections generate the surface
    for c in other:
        ce = exch(c, ec)
        if is_base_verb(c, ec) and s in {ce.get(k) for k in ('p', 'd', 'i', '3', 's')}:
            return c
    # 2) surface is itself a base verb (has its own inflections)
    if is_base_verb(s, ec):
        return s
    # 3) any other base verb candidate
    for c in other:
        if is_base_verb(c, ec):
            return c
    return None            # not a conjugatable verb -> leave entry unchanged

def main():
    files = sorted(glob.glob('data/vocabulary-book-0*-chapter-*.json'))
    data = {f: json.load(open(f, encoding='utf-8')) for f in files}
    entries = [w for d in data.values() for w in d['words']]
    ec = load_ecdict([w['word'] for w in entries])
    # second pass: pull in irregular/mis-lemmatized bases (threw->throw, ran->run,
    # strolled->stroll) not reachable via base_forms
    cand = set()
    for w in entries:
        if not is_verb(w['partOfSpeech']):
            continue
        s = w['word'].lower(); e0 = exch(s, ec).get('0')
        cand.add(s)
        if e0:
            cand.add(e0)
            if e0[-1] not in 'aeiou':
                cand.add(e0 + e0[-1])
        cand.update(base_forms(s))
    missing = [c for c in cand if c not in ec]
    if missing:
        ec.update(load_ecdict(missing))

    changed = 0; samples = []; skipped = []
    for f, d in data.items():
        for w in d['words']:
            if not is_verb(w['partOfSpeech']):
                continue
            surface = w['word']
            lemma = resolve_lemma(surface, ec)
            if not lemma:
                skipped.append(surface)
                continue
            le = exch(lemma, ec)
            third = le.get('3') or rule_third(lemma)
            past = le.get('p') or rule_past(lemma)
            ing = le.get('i') or rule_ing(lemma)
            w['word'] = lemma
            ph = get_phonetic(lemma, ec)
            if ph:
                w['phonetic'] = ph
            if 'phonics' in w:
                w['phonics'] = phonics(lemma)
            w['wordForms'] = f'第三人称单数 {third} · 过去式 {past} · 现在分词 {ing}'
            forms = []
            for x in [surface, lemma, third, past, ing]:
                if x and x not in forms:
                    forms.append(x)
            w['forms'] = forms
            changed += 1
            if len(samples) < 12 and surface != lemma:
                samples.append(f'{surface}->{lemma} [{third}/{past}/{ing}]')
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'transformed {changed} verb entries across {len(files)} files')
    print('samples:', '; '.join(samples))
    if skipped:
        print(f'left unchanged (not conjugatable verbs): {skipped}')

if __name__ == '__main__':
    main()
