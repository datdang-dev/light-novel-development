---
trigger: model_decision
description: Mandatory environmental atmosphere structure for every R18 prose scene
priority: 2
---

# Environmental Atmosphere Rules

> Every scene MUST open and close with environmental description.
> The environment is a CHARACTER — it degrades, accumulates, and tells its own story.

---

## MANDATORY STRUCTURE

### 1. Scene Opening = Environment Snapshot

Every scene file MUST begin (after metadata) with an **italicized environment paragraph** that describes the room state BEFORE the action starts. This paragraph MUST include:

| Element | Required? | Example |
|---------|-----------|---------|
| **Air quality** | ✅ ALWAYS | humidity, temperature, breathability |
| **Smell layers** | ✅ ALWAYS | named, layered (outer → inner → deepest) |
| **Surface contamination** | ✅ ALWAYS | floor state, fabric state, stain geography |
| **Debris inventory** | ✅ IF PRESENT | tissues (state: wet/dry/crusted), condoms, bottles |
| **Lighting** | ✅ ALWAYS | color, quality (harsh/dim/flickering) |
| **Ventilation** | When relevant | windows open/closed, airflow |

### 2. Mid-Scene = Contamination Tracking

At LEAST once per scene section (between `---` dividers), describe how the environment is CHANGING:

- New fluid on surfaces (where it landed, what it mixed with)
- Clothing degradation (what got wet, what shifted, what came off)
- Air quality shift (new smells layering over old ones)
- Debris creation (new tissues, displaced items, stains forming)

### 3. Scene Closing = Aftermath Geography

The continuity table at end of each scene MUST include a **Room** row with:

- Surface state (floor, bedding, furniture)
- Air quality description
- Debris count change from scene open

---

## SMELL LAYERING PROTOCOL

Smells MUST be described in LAYERS, not as single notes:

```
❌ BAD:  "Mùi tinh dịch xộc vào mũi."
✅ GOOD: "Tầng ngoài: mùi rác, mùi bao bì. Tầng giữa: mồ hôi đàn ông.
         Tầng sâu nhất: mùi tinh dịch khô — tanh, mặn, hơi ngọt."
```

### Smell Escalation Across Scenes

Smells MUST get WORSE (more layers, denser) as scenes progress:

| Scene Position | Air Description |
|----------------|-----------------|
| Opening scene | "thoảng nhẹ", "lẫn trong không khí" |
| Mid chapter | "đặc quánh", "như sương mù vô hình" |
| Late chapter | "cần dao để cắt", "như súp", "phòng xông hơi" |
| Final scene | "không còn không khí sạch", "bảo tàng mùi" |

---

## DEBRIS STATE TAXONOMY

When tissues, condoms, or fluid traces appear, describe their STATE:

### Tissues/Khăn Giấy

| State | Vietnamese | Visual |
|-------|-----------|--------|
| Fresh/wet | ướt nhũn, nặng, bán trong suốt | thấy dịch bên trong |
| Drying | nửa ướt, co lại, ố vàng rìa | |
| Dried/crusted | khô cong, giòn, cứng như giấy bồi | vỡ vụn khi chạm |
| Absorbed new fluid | bán trong, nửa cũ nửa mới | phô mai tan chảy |

### Condoms/Bao Cao Su

| State | Description |
|-------|-------------|
| Used + tied | phồng tinh, buộc gút, nặng |
| Used + leaking | rỉ dịch từ miệng bao, tạo vệt |
| Discarded | nằm góc, dính sàn, có thể bị côn trùng bò lên |

### Stains/Vệt Ố

| Type | Vietnamese |
|------|-----------|
| Fresh wet | vũng ướt bóng loáng |
| Drying | vệt ẩm, sẫm màu |
| Dried crust | quầng trắng/vàng, crust, lớp |
| Multi-layer | "bản đồ vệt ố nhiều lớp" |

---

## SURFACE CONTAMINATION TRACKING

Every scene MUST track WHERE fluids land:

```
✅ "Giọt nước bọt rơi lên tất đen — thấm qua — tạo vệt tối."
✅ "Tinh dịch trào qua môi, chảy xuống cằm, rơi lên cà vạt, thấm vào vải."
✅ "Chiếu — vệt ố mới chồng lên vệt ố cũ."
```

### Body Trail Tracking

When fluid contacts body, track the TRAIL:

```
Source → Path → Destination
Miệng → cằm → cổ → cà vạt → ngực áo
Lồn → đùi trong → tất đen → sàn
Cặc → bụng dưới nữ → chiếu
```

---

## REFERENCE DATABASE

When writing environment, CONSULT these knowledge files:

| File | What to extract |
|------|----------------|
| `hentai_lexicon.md` §5 | Aftermath debris checklist |
| `smegma_research.md` | Smell descriptions, bựa vocabulary |
| `sweat_research.md` | Mồ hôi locations, humidity |
| `blowjob_research.md` | Oral aftermath patterns |
| `creampie_research.md` | Overflow/aftermath |

---

## FAIL CONDITIONS

A scene FAILS this rule if:

- [ ] Opens without environment paragraph
- [ ] Has no smell layer description
- [ ] Fluid lands on surface with no visual description
- [ ] Clothing gets wet/stained with no tracking
- [ ] Room state doesn't escalate from previous scene
- [ ] Continuity table has no Room row
