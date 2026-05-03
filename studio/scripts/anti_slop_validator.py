#!/usr/bin/env python3
"""Anti-Slop Quality Validator for LND Studio."""
import re, sys, json, math
from collections import Counter

def entropy(text, window=50):
    """Char-level entropy over sliding window."""
    if len(text) < window:
        return 0
    vals = []
    for i in range(len(text)-window+1):
        chunk = text[i:i+window]
        counts = Counter(chunk)
        total = len(chunk)
        e = -sum((c/total)*math.log2(c/total) for c in counts.values())
        vals.append(e)
    return sum(vals)/len(vals) if vals else 0

def ngram_ratio(text, n=3):
    """Ratio of repeated n-grams."""
    grams = [text[i:i+n] for i in range(len(text)-n+1)]
    if not grams:
        return 0
    c = Counter(grams)
    repeats = sum(v-1 for v in c.values() if v>1)
    return repeats / len(grams)

def sensory_density(text):
    """Sensory token density per 100 chars."""
    tokens = ['濡れた','熱','汗','震え','喘ぎ','吐息','締め付け','にじみ','ぬめり',
              '疼き','疼く','熱く','火照り','冷たい','ひやひや','ゾクゾク','うずうず',
              '疼き','疼く','疼くように','甘く','切なく','じんわり','じんわり広がる',
              'むせ返る','むせる','涙','唾液','じっとり','ねっとり','べっとり','さらり',
              'とろけ','とろける','溶ける','溶け','あたたかい','熱い','冷たい','ひんやり',
              'ざらつき','つるつる','とろとろ','ねっとり','すべすべ','すべる','ひんやり']
    cnt = sum(len(re.findall(re.escape(t), text)) for t in tokens)
    return cnt / (len(text)/100) if len(text) else 0

def consecutive_starts(text, n=3):
    """Check for 3+ sentences starting with same n words."""
    sents = re.split(r'[。！？!?.]', text)
    starts = []
    for s in sents:
        ws = re.findall(r'\w+', s)
        if len(ws) >= n:
            starts.append(tuple(ws[:n]))
    if not starts:
        return False
    c = Counter(starts)
    return any(v >= 3 for v in c.values())

def validate_prose(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    results = {}
    results['entropy'] = entropy(text, 50)
    results['ngram3'] = ngram_ratio(text, 3)
    results['ngram4'] = ngram_ratio(text, 4)
    results['sensory_density'] = sensory_density(text)
    results['consecutive_starts'] = consecutive_starts(text, 3)
    
    passed = True
    issues = []
    
    if results['entropy'] < 3.5:
        passed = False; issues.append(f"entropy too low: {results['entropy']:.2f}")
    if results['ngram3'] > 0.05:
        passed = False; issues.append(f"3-gram repeat ratio: {results['ngram3']:.3f}")
    if results['sensory_density'] < 0.20:
        passed = False; issues.append(f"sensory density: {results['sensory_density']:.2f}")
    if results['consecutive_starts']:
        passed = False; issues.append("3+ sentences start with same 3 words")
    
    return passed, issues, results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: anti_slop_validator.py <prose_file.md>")
        sys.exit(1)
    ok, issues, stats = validate_prose(sys.argv[1])
    print(json.dumps({'passed': ok, 'issues': issues, 'stats': stats}, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)