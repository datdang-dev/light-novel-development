---
trigger: model_decision
description: "CANONICAL banned vocabulary list. ALL pipelines and manifests reference this file."
priority: 0
---

# 🚫 Banned Vocabulary (Canonical List)

> **SINGLE SOURCE OF TRUTH.** All manifests (EC, RP, MA) inherit from this file.
> Violation in narrator voice = HARD REJECT.
> Characters MAY use some terms in dialogue if it fits their persona.

---

## Category A: Moral Judgment / Editorial (Narrator Voice)

These words inject narrator opinion. Replace with physical description.

| ❌ Banned | Category | ✅ Replace With |
|-----------|----------|----------------|
| bệnh hoạn | Moral judgment | Describe the ACTION |
| gớm ghiếc | Moral judgment | Describe TEXTURE/SMELL |
| kinh tởm | Moral judgment | Describe PHYSICAL REACTION |
| đáng kinh ngạc | Editorial | Remove entirely |
| đê hèn | Moral judgment | Describe POWER DYNAMIC |
| tha hóa / sa ngã | Moralizing | Describe CHARACTER'S FEELING |
| vứt bỏ liêm sỉ | AI slop | Show WHAT they did |
| mất nhân tính | Moral judgment | Remove entirely |
| chà đạp hình tượng | Editorial | Remove entirely |
| vũng bùn (metaphorical) | Cliché moralizing | Remove entirely |
| tội lỗi / tội nghiệp | Sympathy/pity | Describe SENSATION |
| nhục nhã (narrator) | Judgment | Show BODY LANGUAGE |
| đồi bại | Moral judgment | Describe the ACT precisely |
| tởm lợm | Moral judgment | Describe TEXTURE/SMELL |

## Category B: Disgust / Revulsion (Narrator Voice)

These break immersion by making the narrator express revulsion.

| ❌ Banned | ✅ Replace With |
|-----------|----------------|
| buồn nôn | Describe physical reaction (co thắt, ợ lên) |
| rác rưởi | Remove — narrator does not editorialize |
| tanh tưởi | Use specific smell: tanh nồng, mùi tinh trùng, mùi mồ hôi |

## Category C: Clinical / Medical Terms

These break the visceral register. Use street Vietnamese.

| ❌ Banned | ✅ Replace With |
|-----------|----------------|
| âm đạo | lồn, bướm, mu |
| dương vật | cặc, cu |
| giao cấu | địt, đụ, chịch |

## Category D: Vietnamese Clichés / AI Slop Phrases

Common AI-generated Vietnamese that signals lazy generation.

| ❌ Banned | ✅ Replace With |
|-----------|----------------|
| ửng hồng | Describe specific color: đỏ ửng, tím bầm, đỏ lựng |
| đỏ hồng | Same as above |
| trắng nõn / trắng nõn nà | Describe texture instead: da mịn, da căng |
| mặt đỏ bừng | Describe heat: mặt nóng rực, tai đỏ lựng |
| trái tim đập thình thịch | Show body: ngực phập phồng, thở dốc |
| "run rẩy" (overused) | Use: co giật, rung lên, bần bật |
| "thổn thức" (overused) | Use: nấc, thở hổn hển |

---

## Validation Rule

```
IF narrator_voice contains ANY word from Categories A-D:
  → HARD REJECT
  → Rewrite using ONLY:
    (1) Physical actions (bành rộng, co giật, rỏ dãi, trợn ngược)
    (2) Fluids (ướt, nhầy, dính, đặc sệt, sền sệt)
    (3) Sounds (lép nhép, chát chúa, thở dốc, rên rỉ)
    (4) Temperature (nóng hổi, lạnh ngắt, rát bỏng)
    (5) Texture (trơn tuột, nhớt nhát, gân guốc)
```

> **EXCEPTION:** Characters in dialogue CAN use Category A/B words about themselves or others (e.g., Haruka calling herself "con đĩ" is CHARACTER VOICE, not narrator editorializing).
