# Step 06d — Narrative Assembly (Screenwriter Step)

## Mục tiêu
Dùng output từ Steps 06, 06b, 06c để tạo `novel_script.md` hoàn chỉnh — một bản kịch bản mà mỗi chapter đều:
1. Advance main quest đúng 1 bước
2. Chứa companion scenes đúng thứ tự prerequisite
3. Có mật độ R18 hợp lý (không quá dày, không quá thưa)
4. Escalate emotional intensity từ nhẹ → nặng theo từng arc

---

## Quy tắc Assembly (Bắt buộc tuân thủ)

### Rule 1: Chapter = Main Quest Beat
Mỗi chapter tương ứng với 1 sự kiện trong main quest backbone.
Nội dung phụ (companion scenes, side quests) được nhét vào xung quanh, không thay thế main beat.

### Rule 2: Companion Scenes KHÔNG xuất hiện trước JOIN EVENT
```
❌ SAI: Yarizo R18 scene ở Ch.6 khi Yarizo chưa join
✅ ĐÚNG: Yarizo join ở Ch.7 → Yarizo R18 scenes chỉ từ Ch.7 trở đi
```

### Rule 3: Bond-gated Scenes tuân thủ thứ tự bond
```
❌ SAI: EV005 (bond=3) trước EV001 (bond=1)
✅ ĐÚNG: EV001 → EV002 → EV003 → EV005 (theo bond level tăng dần)
```

### Rule 4: Scene Type xác định cách insert vào novel
| Scene Type | Insert method |
|-----------|--------------|
| MAIN | Direct prose — xảy ra đúng timeline |
| BOND | Direct prose — xảy ra trong chapter tương ứng |
| BATTLE_LOSS | Nightmare / what-if / Kohaku's internal vision |
| RECOLLECTION | Flashback / memory / déjà vu |
| LOCKED/DLC | Appendix chapter hoặc post-epilogue |

### Rule 5: Max R18 Density per Chapter
- **Early chapters (Ch.1-6)**: 1-2 scenes max, nhẹ (Goblin, solo, mild)
- **Mid chapters (Ch.7-12)**: 2-3 scenes per chapter, escalating
- **Late chapters (Ch.13-19)**: 3-4 scenes, peak intensity
- Không đặt 2 heavy vaginal scenes liên tiếp trong cùng 1 chapter

### Rule 6: Emotional Escalation Arc
Mỗi companion có arc riêng: **Unknowing → Aware → Complicit → Addicted**
- Kohaku: Unknowing (Ch.1) → Aware (Ch.5) → Complicit (Ch.9) → Addicted (Ch.14+)
- Jimmy: Denial (Ch.1) → Curious (Ch.4) → Cuckold (Ch.7) → Embracing (Ch.12+)
- Yarizo: Predator từ đầu, escalate từ verbal → physical → possessive

---

## Template: Chapter Assembly Block

```markdown
## Ch.[N] — [Chapter Title]

**Main Quest Beat:** [main_progress SET=X event, location]
**Chapter Location:** [map/area name]

### Scene List (in order)
| # | Scene ID | EV | Type | Companion | Notes |
|---|---------|-----|------|---------|-------|
| 1 | [id] | [EV#] | MAIN | — | [brief] |
| 2 | [id] | [EV#] | BOND | [companion] | [bond level] |
| 3 | [id] | [EV#] | BATTLE_LOSS | — | insert as: nightmare |

### Narrative Beats
1. [beat 1 — setup/arrival]
2. [beat 2 — main quest event]
3. [beat 3 — companion scene / R18]
4. [beat 4 — consequence / emotional fallout]

### R18 Scene Checklist
- [ ] Scene written (800+ words)
- [ ] Sensory density: smell / sound / texture / temperature
- [ ] Character voice rules followed (Kohaku: "âm hộ" not "lồn")
- [ ] Emotional subtext present (Jimmy's internal cuckold spiral, Kohaku's faith vs desire)
- [ ] SFX tags formatted correctly
```

---

## Nymphomania Priestess — Corrected Chapter Map

### Phase 1: RỪNG (Ch.1-6) — Goblin Arc, No Main Companions Yet

| Chapter | Main Quest | Location | R18 Scenes |
|---------|-----------|----------|-----------|
| Ch.1 | Setup, accept quest | Vương Đô → Rừng | — |
| Ch.2 | Goblin infestation discovered | Rừng | S01: Goblin aphrodisiac first fall |
| Ch.3 | Goblin village | Rừng | S02: Hidden goblin in robe; BL01: Nightmare (battle loss) |
| Ch.4 | First voyeur revelation | Nhà trọ rừng | S03: Kohaku sees cock for first time; S04: Jimmy voyeur awakening |
| Ch.5 | Cuckold agreement | Nhà trọ | S05: Mutual masturbation; S06: Ring exchange + cuckold oath |
| Ch.6 | Journey to capital | Đường đến Vương Đô | S07: Goblin followers sexual service (walking); [No named companions yet] |

### Phase 2: VƯƠNG ĐÔ (Ch.7-11) — All 3 Companions Join

| Chapter | Main Quest (Progress) | Companions Active | Key R18 Scenes |
|---------|----------------------|-----------------|---------------|
| Ch.7 | Arrive capital, slum quest briefing (→SET=1) | **Yarizo JOINS, PM JOINS** | S08: 初遇PM (ice cream, nonverbal); S09: Yarizo tavern intro (EV001 sniff); S10-11: Unicorn Tavern BJ under table |
| Ch.8 | Slum investigation | Yarizo(bond1), PM(bond1) | **Lilith JOINS** (bathhouse); S12: PM alchemist workshop; S13: Yarizo debt threat (EV002); S14: EV003 peep ass |
| Ch.9 | Sewer investigation | Yarizo(bond2), PM(bond2), Lilith(bond1) | S15: Cohaku wet panties (EV036); S16: Yarizo debt repayment (EV005); S17: PM thighjob (EV012); S18: Homeless sewer (EV060); S19: Slime anal (EV061) |
| Ch.10 | Sewer deeper, drug discovery | Yarizo(bond3), PM(bond4), Lilith(bond2) | S20: Onahole→manga scene; S21: Crab dance (EV076 Yarizo orders); S22: Anemone trap (EV034); S23: Lilith watches (EV020) |
| Ch.11 | Underground lab, SET=2 + **Lilith BJ** | Yarizo(bond5), PM(bond5), Lilith(bond3) | S24: Lilith BJ main quest; S25: Yarizo inn (EV049+EV166 animated); S26: Yarizo ED 3P (EV048); S27: Jimmy caught watching (EV052) |

### Phase 3: CỐNG NGẦM SÂU + MA TÚY (Ch.12-15)

| Chapter | Main Quest (Progress) | Key R18 Scenes |
|---------|----------------------|---------------|
| Ch.12 | Guild report SET=3 | S28: Yarizo evicts Jimmy (EV051); S29: Public masturbation order (EV076→ implement); S30: Jimmy+Kohaku sex in front of PM (EV032) |
| Ch.13 | Alice+Leon news SET=4 | S31: Jimmy licks PM ass (EV033); S32: Yarizo praises pussy (EV080); S33: Condom counting (EV040) |
| Ch.14 | Monastery SET=5 | S34: Lilith big cock (EV021); S35: Drug dealer encounter (EV056); S36: Monster loss scenes woven as Kohaku nightmares |
| Ch.15 | Tower sage SET=7 | S37: Jimmy×PM footjob/rimjob series; S38: Yarizo prostitute role (EV090); S39: Yarizo camp PM vs Yarizo (EV077) |

### Phase 4: ÁC CHI THÀNH (Ch.16-19)

| Chapter | Main Quest (Progress) | Key R18 Scenes |
|---------|----------------------|---------------|
| Ch.16 | Arrive Evil City SET=8 | S40: Lust Priestess form (EV118); S41: Alice first corruption |
| Ch.17 | Alice corruption arc SET=9 | S42-46: Alice × thugs/minotaur/orc series |
| Ch.18 | Final boss area SET=10 | S47-51: Alice church series; S52: Yarizo×Alice; S53: Medusa mind control |
| Ch.19 | Ending | S54: Ending CG; S55: Kohaku mother flashback reveal |

---

## Validation Checklist Before Handing to Suki

- [ ] Every companion R18 scene is AFTER their JOIN chapter
- [ ] Bond-level scenes are in ascending bond order
- [ ] No chapter has >4 R18 scenes
- [ ] Battle loss scenes marked as NIGHTMARE/WHAT-IF
- [ ] Recollection Room scenes mapped to source, not used as timeline order
- [ ] Main quest beats present in every chapter
- [ ] Emotional arc shows clear progression per character
