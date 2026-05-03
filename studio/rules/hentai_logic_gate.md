---
trigger: model_decision
description: Mandatory hentai logic filter — runs BEFORE any prose is finalized. Hard gate for Japanese R18 cultural compliance.
priority: 1
---

# Hentai Logic Gate (ヘンタイ・ロジック・ゲート)

## PURPOSE

This is a **HARD GATE**. Every prose output MUST pass ALL checks below before finalization.
If ANY check fails → output is REJECTED, returned to prose-adapter for revision.

> **Core Principle:** Japanese R18 ero-novel is NOT "porn with words."
> It is a **psychological seduction machine** that uses narrative craft to deliver arousal through story logic, not just explicit description.

---

## GATE 1: 納得感 (Nattoku-kan / Erotic Justification)

**Question:** Does the reader understand WHY this sexual situation is happening?

Every escalation from non-sexual → sexual MUST have **erotic logic**. The reader must think "ああ、なるほど..." (Ah, I see why...) — not "wait, why is she suddenly naked?"

### Mandatory Checks:
- [ ] **Trigger Event Exists:** What specific event/situation caused the sexual encounter? (Power dynamics shift, emotional vulnerability, physical proximity trap, substance, corruption progression, etc.)
- [ ] **Character Motivation Clear:** Each character has a reason to participate (desire, obligation, curiosity, submission, dominance, revenge, etc.)
- [ ] **Escalation Ladder Present:** The scene doesn't jump from "hello" to "penetration." There are intermediate steps.

### Anti-Patterns (INSTANT FAIL):
- ❌ Characters have sex "because the plot requires it" with no setup
- ❌ Stranger sex without establishing the context (unless the GENRE is specifically about that, e.g., 援交/enkou)
- ❌ Mind-break happens on first encounter without sufficient overwhelm buildup

---

## GATE 2: 背徳感 (Haitoku-kan / Taboo Element)

**Question:** WHAT makes this situation "forbidden" or "wrong"?

The sense of taboo is the PRIMARY aphrodisiac in Japanese ero-fiction. Without it, the scene is "just sex" — boring by JP reader standards.

### Mandatory Checks:
- [ ] **Taboo Element Identified:** At least ONE of:
  - Relationship taboo (teacher-student, step-family, boss-subordinate, friend's partner)
  - Location taboo (public, school, workplace, sacred place)
  - Status taboo (age gap, social class, virgin/experienced mismatch)
  - Moral taboo (cheating, corruption of innocent, betrayal)
  - Physical taboo (first time, forbidden body, size mismatch)
- [ ] **Taboo is ACKNOWLEDGED in prose:** A character (or narrator) explicitly or implicitly recognizes "this is wrong/forbidden/shouldn't happen"
- [ ] **Taboo ENHANCES arousal:** The wrongness is depicted as making the experience MORE intense, not less

### Anti-Patterns (INSTANT FAIL):
- ❌ Sex scene with zero taboo element (vanilla + no context = boring)
- ❌ Taboo is present but treated as "no big deal" by characters
- ❌ Moralizing about the taboo (judgmental narrator tone)

---

## GATE 3: ギャップ萌え (Gap Moe / Persona Contrast)

**Question:** Does the character show a CONTRAST between their public persona and their sexual behavior?

Gap Moe is the engine of Japanese character-driven erotica. The greater the gap, the greater the arousal.

### Mandatory Checks:
- [ ] **Public Persona Established:** Reader knows who this character is "normally"
- [ ] **Private Behavior Contrasts:** During the sexual encounter, the character behaves DIFFERENTLY from their public self
- [ ] **The Gap is Visible:** The contrast is explicitly described or commented on

### Examples:
| Archetype | Public Persona | Private Gap | Arousal Source |
|-----------|---------------|-------------|----------------|
| 生徒会長 (Student Council Pres.) | Cold, strict, in-control | Submissive, begging, ahegao | "The perfect girl... broken" |
| メスガキ (Mesugaki) | Bratty, mocking, dominant | Crying, apologizing, overwhelmed | "The tables have turned" |
| お姉さん (Onee-san) | Mature, composed, teasing | Losing composure, desperate | "Even she can't handle this" |
| 地味子 (Plain/Quiet girl) | Invisible, shy, wallflower | Secretly perverted, aggressive | "Still waters run deep" |

---

## GATE 4: 征服感 (Seifuku-kan / Conquest Progression)

**Question:** Does the reader feel the PROGRESSION of "conquering" the character?

This is NOT about violence or force. It's about the gradual journey from resistance/composure to surrender/pleasure.

### Mandatory Checks:
- [ ] **Starting State Clear:** Where is the character emotionally/physically at scene start?
- [ ] **Resistance/Composure Phase Present:** The character initially resists, denies, or maintains composure
- [ ] **Cracking Points Visible:** Specific moments where control breaks (a moan escapes, body betrays mind, etc.)
- [ ] **Surrender/Acceptance Moment:** The point where the character gives in (reluctantly or eagerly)

### Progression Template:
```
拒絶 (Rejection) → 困惑 (Confusion) → 動揺 (Wavering) → 
快楽 (Pleasure) → 陥落 (Surrender) → 堕落 (Corruption)
```

Not every scene must reach 堕落. But the DIRECTION must be clear.

---

## GATE 5: Anti-Reset Protocol (記憶保持)

**Question:** Is character development consistent with previous encounters?

### Rules:
- A character who has been "broken" (mind-break) CANNOT randomly recover to their original state
- Corruption is a ONE-WAY STREET: each encounter pushes further, never backwards
- If a character showed pleasure in a previous scene, they cannot pretend it didn't happen
- Body memory persists: a character who orgasmed from anal doesn't forget that sensation

### Exception:
- Time-skip with explicit "recovery" narrative is allowed
- Character actively fighting their corruption (internal conflict) is fine — but the STRUGGLE must be visible, and they should still be more susceptible than before

---

## GATE 6: Male Gaze Architecture (男性視点構造)

**Question:** Is the prose optimized for the male heterosexual reader's arousal?

### Mandatory Checks:
- [ ] **Visual Descriptions of Female Body:** Breasts, thighs, expressions, clothing state — described FROM the implied male gaze perspective
- [ ] **Power Fantasy Elements:** Reader can self-insert into the dominant/conquering role (even in 3rd person narration)
- [ ] **Reward Moments:** Clear "payoff" moments where the reader feels satisfaction (successful seduction, reluctant pleasure, mind-break achievement)
- [ ] **ご褒美感 (Gohoubi-kan):** The climax feels EARNED after the build-up

---

## SUMMARY: GATE PASS/FAIL

```
BEFORE finalizing ANY prose output, verify:

[G1] 納得感 — Erotic justification present?     □ PASS / □ FAIL
[G2] 背徳感 — Taboo element active?              □ PASS / □ FAIL  
[G3] ギャップ萌え — Persona contrast visible?    □ PASS / □ FAIL
[G4] 征服感 — Conquest progression clear?         □ PASS / □ FAIL
[G5] 記憶保持 — Anti-reset maintained?            □ PASS / □ FAIL
[G6] 男性視点 — Male gaze architecture intact?   □ PASS / □ FAIL

IF ANY GATE = FAIL → REJECT output, revise, re-check.
ALL 6 GATES must PASS for prose to be finalized.
```

---

## Related Rules
- `pervert_pov.md` — Core mindset and phase intensity
- `lewd_writing_mechanics.md` — Writing techniques and vocabulary
- `quality_gates.md` — Scoring rubric (Category F uses this gate)
- `sensory_density.md` — Minimum sensory requirements
