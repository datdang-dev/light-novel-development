---
trigger: model_decision
description: State tracking across scenes - fluids, clothing, positions
priority: 5
---

# Continuity Rules

## CORE PRINCIPLE

**Never start a scene "clean" if the previous scene ended "messy".**

---

## FLUID TRACKING

| Fluid | Track Location | Track State |
|-------|---------------|-------------|
| Cum | trong lồn, trên đùi, trên ngực, trên mặt | ướt → khô → dính |
| Sweat | trán, ngực, đùi, toàn thân | lấp lánh, nhỏ giọt |
| Saliva | môi, cằm, ngực | ướt, dính |
| Mixed | chỗ nối, đùi trong | sủi bọt, nhớp |

### Transition Example

```text
Scene 1 END:  Cum inside + dripping on thighs
Scene 2 START: "Tinh dịch từ lần trước vẫn còn chảy xuống đùi cô..."
```

---

## CLOTHING TRACKING

| State | Description | Next Scene Must... |
|-------|-------------|-------------------|
| Intact | Worn normally | Can stay or change |
| Disheveled | Xốc lên, kéo xuống | Reference dishevelment |
| Partially removed | Một bên tuột | Specify where it is |
| Removed | Not on body | Mention location (floor? chair?) |
| Contaminated | Dính cum, mồ hôi | Track contamination |
| Damaged | Rách, đứt nút | Stay damaged |

---

## POSITION TRACKING

| Element | What to Track |
|---------|--------------|
| Location | Which room? Which furniture? |
| Posture | Đứng, ngồi, nằm, quỳ |
| Orientation | Facing where? Bent how? |
| Limbs | Arms tied? Legs spread? |

---

## PHYSICAL STATE

| State | Indicators |
|-------|------------|
| Exhaustion | Rũ, hổn hển, không đứng nổi |
| Arousal | Ướt, cứng, đỏ bừng |
| Soreness | Nhức, đau, tê |

---

## TIME GAP RULES

If time passes between scenes:

- How long since last action?
- Has anything dried/changed?
- Character recovery state?

---

## PRE-SCENE CHECKLIST

Before starting new scene:

- [ ] Previous fluids accounted for?
- [ ] Clothing state referenced?
- [ ] Body positions logical?
- [ ] Physical exhaustion shown?
- [ ] Time gap addressed?