# 📋 RETROSPECTIVE — RPG Adapter Skill Failure Analysis
> Date: 2026-05-02 · Meeting: AI Self-Audit
> Triggered by: User complaint về skill "ngu đi"

---

## 🎭 MEETING PARTICIPANTS
- **Kana** (Visual Context Analyst) — đại diện extraction pipeline
- **Director K** (Orchestrator) — đại diện workflow logic
- **Suki** (Prose Writer) — đại diện output quality

---

## ❌ VẤN ĐỀ NGƯỜI DÙNG XÁC ĐỊNH

> *"Timeline sẽ follow theo tiến trình nhiệm vụ, ví dụ event để có các follower như Yaziro, PM, Lilith sẽ có các tuyến nhiệm vụ riêng chứ đâu phải đùng 1 cái có event được"*

User nói rõ: **Yarizo, PM, Lilith không thể xuất hiện và làm R18 scenes ngay lập tức — họ phải được unlock theo quest timeline.**

---

## 🔍 ROOT CAUSE ANALYSIS

### Vấn đề 1: Skill không có bước "Quest Prerequisite Mapping"
**Symptom:** Novel script map Yarizo vào Ch.6 làm R18 scene ngay, trong khi game data cho thấy:
- **Yarizo (亚利佐)**: Xuất hiện tại Unicorn Tavern (独角兽酒馆), có bond variable system riêng (CE370→CE372). Không thể có scene EV001 (Yarizo khoe cu) trước khi NPC này được "encounter" đúng flow.
- **PM**: Join mechanic thông qua `初遇PM` event + alchemist quest. Game data có CG series `初遇PM/event-pm-ice_cream-*` — đây là **first meeting**, không phải sex scene.
- **Lilith (莉莉丝)**: CE356, CE309, CE310 cho thấy Lilith có toàn bộ arc riêng về camping/露营 trước khi có sex event.

**Root cause:** Skill chỉ có `step-06b-r18-audit.md` để catalog R18 scenes, nhưng **KHÔNG CÓ BƯỚC NÀO** để map prerequisite conditions của từng scene vào timeline.

### Vấn đề 2: Bỏ qua Switch/Variable dependency chain
**Symptom:** Novel script đặt scenes theo "cảm giác" thay vì theo variable gates.

**Bằng chứng từ game data:**
- `主线进度 SET=0→10` là backbone timeline, nhưng companion events chạy trên **variable track riêng**.
- Yarizo có `V[羁绊]` (bond variable), PM có `V[167]` (口交次数), `V[168]` (小穴次数) — đây là **progression counters**, không phải flags đơn giản.
- Map023 EV041 `["让您久等了 / 祭司大人…"]` ADD Actor 1+2 — đây là nơi Kohaku **re-join** party sau khi bị tách ra tại nhà tù. Script hiện tại bỏ qua context này hoàn toàn.

**Root cause:** `step-06-timeline.md` và `step-06b-r18-audit.md` không extract variable dependency chains. Skill chỉ biết "scene này có R18" mà không biết "scene này chỉ unlock SAU KHI player đã làm X".

### Vấn đề 3: Không phân biệt Scene Type
**Symptom:** Mọi R18 event đều được treat như "chapter content", bao gồm cả:
- **Recollection Room scenes** (Map029) — đây là MEMORY/REPLAY, không phải first-time event
- **Battle loss scenes** — conditional, chỉ xảy ra khi thua
- **Bond events** — chỉ mở khi bond đủ cao
- **Main quest scenes** — locked behind 主线进度

**Root cause:** Skill không có bước phân loại scene type trước khi map vào timeline.

### Vấn đề 4: Skill được design cho "extract" không phải cho "screenwriting"
**Symptom:** Output là danh sách scenes, không phải narrative flow.

**Root cause:** SKILL.md chỉ route đến:
1. Data extraction tools
2. Prose generation (Suki)

Không có bước **"Narrative Timeline Construction"** — nơi AI đóng vai biên kịch và sắp xếp scenes theo:
- Prerequisite logic (quest gates)
- Pacing (density của R18 per chapter)
- Character arc (từng companion có arc riêng)
- Emotional escalation (nhẹ → nặng)

---

## 📐 WHAT SHOULD HAVE HAPPENED

Đúng quy trình cho "adapt RPG to novel với full R18 scenes":

```
STEP A: Extract main quest backbone (主线进度 0→10)
  → Map each SET point to a novel "chapter boundary"

STEP B: For each companion (Yarizo/PM/Lilith/Alice):
  → Extract their JOIN event (where/when they join party)
  → Extract their BOND progression (variable track)
  → Extract ALL their R18 events WITH prerequisite conditions
  → Sort R18 events by earliest possible unlock point

STEP C: For each R18 event:
  → Classify: main_quest / bond_event / battle_loss / recollection_replay
  → Assign to chapter AFTER all prerequisites satisfied
  → Never place earlier than companion join event

STEP D: Build narrative timeline (the screenwriter step)
  → Each chapter = 1 main quest beat
  → Companion R18 events woven in AFTER their unlock conditions
  → Battle loss scenes = nightmare/what-if unless player chose loss path
  → Recollection Room = not chronological, use as flashback/memory
```

---

## ✅ ACTION ITEMS

1. **UPDATE SKILL.md** → Add "Quest-Gated Narrative Mapping" as core capability
2. **CREATE step-06c-companion-timeline.md** → New step: extract companion join + bond arc + R18 unlock chain
3. **CREATE step-06d-narrative-assembly.md** → Screenwriter step: assemble scenes into timeline respecting prerequisites
4. **UPDATE novel_script.md** → Re-map all scenes with correct prerequisite gating

---

## 🎯 ĐIỀU QUAN TRỌNG NHẤT

> **Recollection Room (Map029) là BẢO TÀNG, không phải chronological timeline.**
> Nó ghi nhớ các event đã xảy ra — không có nghĩa là tất cả events xảy ra theo thứ tự đó.
> Biên kịch phải trace NGƯỢC từ recollection room về MAP event gốc, tìm prerequisite, rồi mới đặt vào chapter đúng vị trí.
