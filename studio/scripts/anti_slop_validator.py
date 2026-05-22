#!/usr/bin/env python3
"""Anti-Slop Quality Validator for LND Studio.

Dynamically audits explicit R18 Vietnamese prose against sensory and cliche lexicons.
"""
import re
import sys
import json
import math
import os
import hashlib
from collections import Counter

# Try importing PyYAML, provide a lightweight fallback parser if not installed
try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_LEXICONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../modules/gooner-audit-engine/lexicons"
)

# Hardcoded fallback values in case files are missing
FALLBACK_SENSORY = {
    "tactile": [
        "ướt", "nhơm nhớp", "trơn", "nóng", "mồ hôi", "ẩm", "tanh",
        "giật", "bóp", "khít", "co thắt", "ấm nóng", "đặc sệt", "rỉ",
        "đùi non", "nhầy nhụa", "cọ xát", "tê dại", "sền sệt"
    ],
    "explicit": [
        "cặc", "lồn", "địt", "bú lồn", "mút khấc", "lút cán", "dâm thủy",
        "tinh trùng", "quy đầu", "lỗ nhị", "nước dâm"
    ],
    "vocal": [
        "rên", "thở", "ứ hự", "rên rỉ", "thở dốc", "van xin"
    ]
}

FALLBACK_CLICHE = {
    "ai_slop_cliche": [
        "cuộc hành trình dâm dục", "sự hòa quyện tuyệt vời",
        "tình yêu thăng hoa", "thắp sáng màn đêm", "khát vọng mãnh liệt"
    ],
    "sanitized_phrases": [
        "ân ái nhẹ nhàng", "sự kết hợp thiêng liêng",
        "tình cảm đôi lứa", "giây phút ngọt ngào"
    ],
    "localization_leakage": [
        "cô giáo Thảo", "thầy giáo Hải", "bạch bạch", "nhóp nhép"
    ]
}

def get_file_checksum(filepath):
    """Compute SHA256 checksum of a file."""
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def parse_yaml_fallback(filepath):
    """Simple line-by-line YAML parser fallback if PyYAML is missing."""
    data = {}
    current_key = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.endswith(':'):
                current_key = line[:-1].strip()
                data[current_key] = []
            elif line.startswith('-') and current_key is not None:
                val = line[1:].strip().strip('"').strip("'")
                data[current_key].append(val)
    return data

def load_lexicon(filename, fallback_data):
    """Loads a lexicon YAML file using PyYAML or fallback parser."""
    filepath = os.path.join(DEFAULT_LEXICONS_DIR, filename)
    checksum = get_file_checksum(filepath)
    
    if not os.path.exists(filepath):
        return fallback_data, None

    try:
        if yaml:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    return loaded, checksum
        else:
            return parse_yaml_fallback(filepath), checksum
    except Exception as e:
        print(f"Warning loading {filename}: {e}. Using fallback.", file=sys.stderr)
        
    return fallback_data, checksum

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
    """Ratio of repeated n-grams. Uses word-level for space-separated languages."""
    words = re.findall(r'\w+', text.lower())
    if len(words) >= 10:
        grams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
    else:
        grams = [text[i:i+n] for i in range(len(text)-n+1)]
        
    if not grams:
        return 0
    c = Counter(grams)
    repeats = sum(v-1 for v in c.values() if v>1)
    return repeats / len(grams)

def find_evidence_lines(text, phrase):
    """Find line numbers containing the specified phrase (1-indexed)."""
    lines = text.split('\n')
    evidence = []
    phrase_lower = phrase.lower()
    for idx, line in enumerate(lines):
        if phrase_lower in line.lower():
            evidence.append({"line": idx + 1, "text": line.strip()})
    return evidence

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
    """Validates prose text file against structured criteria."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Load dynamic lexicons
    sensory_lexicon, sensory_hash = load_lexicon("vi_sensory.yaml", FALLBACK_SENSORY)
    cliche_lexicon, cliche_hash = load_lexicon("vi_cliche.yaml", FALLBACK_CLICHE)

    # Flatten sensory tokens for count
    sensory_tokens = []
    for cat, tokens in sensory_lexicon.items():
        if isinstance(tokens, list):
            sensory_tokens.extend(tokens)
    sensory_tokens = list(set(sensory_tokens)) # remove duplicates

    # Compute stats
    ent = entropy(text, 50)
    ng3 = ngram_ratio(text, 3)
    ng4 = ngram_ratio(text, 4)
    
    sensory_cnt = sum(len(re.findall(re.escape(t), text.lower())) for t in sensory_tokens)
    sensory_density_val = sensory_cnt / (len(text)/100) if len(text) else 0

    results = {
        'entropy': ent,
        'ngram3': ng3,
        'ngram4': ng4,
        'sensory_density': sensory_density_val,
        'consecutive_starts': consecutive_starts(text, 3),
        'lexicon_checksums': {
            'vi_sensory': sensory_hash,
            'vi_cliche': cliche_hash
        }
    }
    
    passed = True
    issues = []

    # 1. Density & Repetitive metrics
    words = re.findall(r'\w+', text.lower())
    is_word_segmented = len(words) >= 10
    ngram3_limit = 0.12 if is_word_segmented else 0.05
    
    if ent < 3.5:
        passed = False
        issues.append({
            "category": "entropy",
            "message": f"Entropy too low: {ent:.2f} (limit: >=3.5)"
        })
    if ng3 > ngram3_limit:
        passed = False
        issues.append({
            "category": "ngram_repetition",
            "message": f"3-gram repeat ratio: {ng3:.3f} (limit: <= {ngram3_limit})"
        })
    if sensory_density_val < 0.20:
        passed = False
        issues.append({
            "category": "sensory_density",
            "message": f"Sensory density below threshold: {sensory_density_val:.2f} (limit: >=0.20)"
        })
    if results['consecutive_starts']:
        passed = False
        issues.append({
            "category": "consecutive_sentences",
            "message": "3+ sentences start with the same 3 words (repetitive style)"
        })

    # 2. Cliche & Localization scan
    for category, cliches in cliche_lexicon.items():
        if not isinstance(cliches, list):
            continue
        for cliche in cliches:
            escaped = re.escape(cliche)
            matches = re.findall(escaped, text.lower())
            if matches:
                passed = False
                evidences = find_evidence_lines(text, cliche)
                issues.append({
                    "category": category,
                    "message": f"Forbidden phrase found: '{cliche}' (matches: {len(matches)})",
                    "evidence": evidences
                })

    return passed, issues, results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: anti_slop_validator.py <prose_file.md>")
        sys.exit(1)
        
    ok, issues, stats = validate_prose(sys.argv[1])
    print(json.dumps({'passed': ok, 'issues': issues, 'stats': stats}, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)