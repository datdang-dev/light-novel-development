---
trigger: model_decision
description: State tracking rules across scenes and chapters
---

# Continuity Rules

## PURPOSE
Track physical state across scenes to maintain immersion and realism.

---

## 🩸 RESIDUE TRACKING

### Fluids
Track location and state of:

| Fluid | Location Options | State Options |
|-------|------------------|---------------|
| Cum | trong lồn, trên đùi, trên ngực, trên mặt, trong miệng | ướt, khô, dính, chảy |
| Sweat | trán, ngực, đùi, toàn thân | lấp lánh, nhỏ giọt |
| Saliva | môi, cằm, ngực | ướt, dính |
| Mixed | chỗ nối, đùi trong | sủi bọt, nhớp |

### Example Tracking
```
Scene 1 END: Cum inside + on thighs
Scene 2 START: Must mention → "Tinh dịch từ lần trước vẫn còn chảy xuống đùi cô..."
```

---

## 👗 CLOTHING STATE

Track exact state:

| State | Description |
|-------|-------------|
| Intact | Worn normally |
| Disheveled | Xốc lên, kéo xuống, nút mở |
| Partially removed | Một bên tuột, vest mở |
| Removed | Nằm ở đâu? |
| Contaminated | Dính cum, mồ hôi, ướt |
| Damaged | Rách, đứt nút |

### Example
```
START: School uniform complete
DURING: Skirt lifted, panties pulled aside
END: Panties still aside, cum stain on skirt hem
NEXT SCENE: Must reference this state
```

---

## 🧍 BODY POSITION

Track where everyone is:

| Element | Track |
|---------|-------|
| Location | Room, furniture, floor |
| Position | Đứng, ngồi, nằm, quỳ |
| Orientation | Facing where, bent how |
| Limbs | Arms (tied? holding?), legs (spread? wrapped?) |

---

## 😵 PHYSICAL STATE

| State | Indicators |
|-------|------------|
| Exhaustion | Run, hổn hển, không đứng nổi |
| Arousal level | Ướt, cứng, đỏ bừng |
| Pain/soreness | Nhức, đau, tê |
| Satisfaction | Thỏa mãn, còn muốn nữa |

---

## ⏱️ TIME TRACKING

If time passes:
- How long since last action?
- Has anything dried/changed?
- Character recovery state?

---

## ✅ CONTINUITY CHECKLIST

Before starting new scene:
- [ ] Previous fluids accounted for?
- [ ] Clothing state correct?
- [ ] Body positions logical?
- [ ] Physical exhaustion considered?
- [ ] Time gap addressed?

**RULE**: Never start a scene in a "clean" state if previous scene ended messy.