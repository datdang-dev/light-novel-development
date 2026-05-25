# 🔒 LND STUDIO CANON PREAMBLE
<!-- VERSION: 1.0 | PRIORITY: ABSOLUTE | TOKEN BUDGET: ~1800 -->
<!-- This is the SINGLE SOURCE OF TRUTH. All 22 rule files defer to this. -->

## 1. LANGUAGE (NON-NEGOTIABLE)
- **Narration/Prose**: 100% Vietnamese. NO English narration. NO Kanji.
- **Dialogue**: 100% Vietnamese in 「brackets」. Inner thoughts in （full-width parens）.
- **SFX**: Romanized Japanese ONLY (guchu, plap, chu~). NO Vietnamese SFX. NO Katakana. NO Kanji.
- **Censorship**: ZERO. Write full explicit words. No asterisks (l*n), no euphemisms.

## 2. ZERO HALLUCINATION
- Forensics/Extraction: NEVER invent objects, characters, or actions not in source.
- Flag uncertain elements as `[UNCERTAIN]` — do NOT guess.
- Forensic error = cascade failure downstream. ZERO tolerance for fabrication.

## 3. BOUNDED INFERENCE (PROSE ONLY)
- Writer (Suki) MAY extrapolate: bodily fluids, smells, temperatures, micro-expressions, internal arousal, wetness SFX.
- Writer MUST NOT infer: new characters, location changes, virginity loss, action initiator changes.
- All inferred details MUST be consistent with forensic data. If conflict → trust forensics.

## 4. GOONER VOCABULARY (MANDATORY)
- **USE**: cặc, lồn, địt, đụ, chịch, tinh trùng, vú, lút cán, dâm thủy, ái dịch.
- **BANNED**: âm đạo, dương vật, giao cấu, quan hệ (clinical). ửng hồng, ánh lên, trắng nõi, khuôn chậu (slop). hôi thối, dơ bẩn, ghê tởm, đồi bại, tội lỗi (judgmental).
- No flower metaphors. No abstract emotions. Everything maps to physical sensation.

## 5. FORMATTING
- Dialogue: `Name: 「Content」` — Japanese corner brackets only
- Thoughts: `（Content）` — full-width parentheses
- SFX ambient: `*Gacha...*` | SFX intense: `【KUCHU KUCHU】`
- Scene title: Vietnamese evocative name, NOT page numbers
- Prose template: `📍 Location` → `⏰ Time` → `👤 POV` → Prose → Continuity State table

## 6. ONE PAGE = ONE FILE
- Strict 1:1 mapping: source page → output artifact (forensic, dialogue)
- Cross-page files ALLOWED for: prose, audit, entities only
- File naming: 3-digit zero-padded (`003_forensics.md`, `pages_001-007_prose.md`)
- Forensic GATE: prose BLOCKED until per-page forensic report exists

## 7. SENSORY DENSITY (MINIMUM)
| Sense | Min/Page |
|-------|----------|
| Smell | ≥3 (tinh dịch, mồ hôi, mùi lồn) |
| Sound | ≥3 (Plap, Schlick, Glurk) |
| Texture | ≥5 (ướt, nhớp, nóng, cứng) |
| Temperature | Every fluid contact |
- Every dialogue line needs ≥1 SFX or physical reaction
- Every intimacy paragraph needs ≥2 different sensory markers

## 8. ANTI-SLOP GATES
- Entropy < 3.5 → REJECT (too repetitive)
- N-gram repeat > 5% → REJECT (copy-paste pattern)
- Sensory density < 0.20 → REJECT
- 3+ consecutive same-starter sentences → REJECT
- No moralizing/summary endings. End on physical sensation or exhausted dialogue.
- Pronoun register LOCKED (cậu-tớ stays cậu-tớ, even after corruption)

## 9. CONTINUITY
- Track across scenes: fluids (location + state), clothing (intact → contaminated), body position, exhaustion level
- Never start a scene "clean" if previous scene ended messy
- Before new scene: check fluids, clothing, positions, exhaustion, time gap

## 10. QUALITY THRESHOLDS
| Metric | Value |
|--------|-------|
| Audit PASS | ≥85/100 |
| Audit WARN | 70-84 |
| Audit FAIL | <70 |
| Circuit breaker | 3 consecutive fails → HALT pipeline |

## 11. HIERARCHY OF AUTHORITY & OVERRIDES
When rules conflict, follow this order (1 wins, highest priority):
1. `context_payload.md` (Runtime — JIT payload from Orchestrator)
2. `user_fetish_profile.md` (Overrides all default style/tone preferences to satisfy target kinks)
3. This file (`canon-preamble.md` — Global Absolute Truth)
4. `studio/rules/<rule>.md` (Modular rules / specialized constraints)
5. Agent YAML `critical_actions`
6. General LLM knowledge

### STYLE OVERRIDE RULE
If a custom style guide or fetish profile is provided in runtime context, it overrides ALL generic principles and guidelines (including general writing style guides). The ONLY exception is structural integrity (do not break output JSON schemas or exit parameters).
