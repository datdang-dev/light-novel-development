# Step 06c — Companion Timeline Extraction

## Mục tiêu
Với mỗi companion (nhân vật đồng hành), xây dựng timeline đầy đủ:
1. **JOIN EVENT**: Khi nào/ở đâu companion này join party
2. **BOND ARC**: Các mốc bond progression (variable-gated)
3. **R18 UNLOCK CHAIN**: Mỗi R18 scene cần prerequisites gì

---

## Quy trình thực hiện

### 1. Tìm JOIN EVENT

```python
# Trong tất cả Map*.json, tìm code=129 (Change Party Member) với action=0 (Add)
# actor_id phải khớp với companion đang xét
# Record: map_id, event_id, page_conditions (switch/variable requirements)
```

**Output mong muốn:**
```
[COMPANION: Yarizo]
JOIN: Map012 (独角兽酒馆/Unicorn Tavern), EV_Yarizo_Intro
REQUIRES: main_progress >= 1 (player đã vào Vương Đô)
FIRST_TEXT: "今天是由我来负责" / "Hôm nay tôi phụ trách"
```

### 2. Tracing Bond Variable

```python
# Tìm variable name chứa companion name hoặc 羁绊 (bond)
# Liệt kê tất cả events SET/ADD variable này
# Sort theo thứ tự tăng dần của giá trị variable
```

**Output mong muốn:**
```
[YARIZO BOND TRACK: V[亚利佐羁绊]]
  Bond += 1: CE370 (Yarizo thấy Kohaku lần đầu ở tavern)
  Bond += 1: EV001 Map012 (khoe cu, Kohaku ngửi)
  Bond += 1: EV002 Map012 (đe dọa insert)
  Bond >= 3: EV005 (debt repayment mở khóa)
  ...
```

### 3. Map Recollection Room Events → Source Events

Với mỗi EV trong Map029 (Recollection Room):

```
Map029 EV001 [亚利佐] 
  → Trace: xem page conditions (V[亚利佐羁绊] >= N?)
  → Find source: tìm event trong map khác có CÙNG text/CG
  → Record: source_map, source_event, prerequisites
```

### 4. Build Unlock Chain

Sắp xếp R18 scenes theo thứ tự có thể unlock sớm nhất:

```
EARLIEST UNLOCK = MAX(
  companion_join_chapter,
  bond_level_required / bond_gain_rate,
  main_progress_required
)
```

---

## Template Output: Companion Timeline Card

```markdown
## [COMPANION NAME] — Timeline Card

**JOIN EVENT**
- Map: [map name]
- Condition: main_progress >= [N], SW[X] = ON
- Context: [brief scene description]
- Novel Chapter: Ch.[N]

**BOND PROGRESSION**
| Bond Level | Event | Location | Novel Chapter |
|-----------|-------|----------|--------------|
| 0→1 | [description] | [map] | Ch.[N] |
| 1→2 | [description] | [map] | Ch.[N+1] |
...

**R18 SCENES (in unlock order)**
| Scene ID | Source Map/EV | Prerequisites | Novel Chapter | Scene Type |
|---------|--------------|---------------|--------------|-----------|
| [id] | [map_ev] | bond>=N, main>=M | Ch.[X] | [BOND/MAIN/LOSS/MEMORY] |
...
```

---

## Nymphomania Priestess — Companion Cards

### 亚利佐 (Yarizo) Timeline Card

**JOIN EVENT**
- Map: Map012 (独角兽酒馆 / Unicorn Tavern)
- Condition: main_progress >= 1 (sau khi vào Vương Đô)
- Context: Yarizo gặp Kohaku tại quán rượu, tự giới thiệu khiêu khích
- Novel Chapter: **Ch.7** (khi nhóm đến Unicorn Tavern lần đầu)

**BOND PROGRESSION**
| Bond | Event/CE | Description | Earliest Chapter |
|------|---------|-------------|-----------------|
| 0 | CE370 | Yarizo nhìn trộm Kohaku từ xa | Ch.7 |
| 1 | EV001 (Map029/Map012) | Khoe cu → Kohaku ngửi | Ch.7 |
| 2 | EV002 | Yarizo đe dọa insert | Ch.8 |
| 2 | EV003 | Nhìn trộm mông | Ch.8 |
| 3 | EV005 | Debt repayment bắt đầu | Ch.9 |
| 3 | CE371 | Kohaku đón nhận "lãi suất" | Ch.9 |
| 4 | EV169 (V142≥1) | Yarizo brothel stage 1 | Ch.10 |
| 5 | CE372 | Yarizo tuyên bố Kohaku thuộc về mình | Ch.11 |
| 5 | EV048 | 3P thất bại (ED scene) | Ch.11 |
| 6 | EV049 | Yarizo khách sạn | Ch.11 |
| 6 | EV166 (animated) | Animated inn scene | Ch.11 |
| 7 | EV051 | Đuổi Jimmy, private với Kohaku | Ch.12 |
| 7 | EV076 | Kohaku thủ dâm công khai | Ch.12 |
| 8 | EV080 | Yarizo khen pussy | Ch.13 |
| 9 | EV090 | Yarizo đóng vai nhân viên | Ch.14 |

---

### PM Timeline Card

**JOIN EVENT**
- Map: Map012 (王都 / Capital), PM shop / street
- Context: PM gặp Kohaku+Jimmy trên phố, event `初遇PM` (ice cream CG series)
- Condition: Đến Vương Đô (main_progress >= 1)
- Novel Chapter: **Ch.7** (cùng chapter với Yarizo introduction)

**BOND PROGRESSION**
| Bond | Event | Description | Earliest Chapter |
|------|-------|-------------|-----------------|
| 0 | EV029 | Gặp PM trên phố | Ch.7 |
| 1 | EV026 | PM nhận hoa, gật đầu | Ch.7 |
| 1 | EV028 | Quest tìm luyện kim sư | Ch.7 |
| 2 | EV027 | PM làm việc trong shop | Ch.7 |
| 3 | EV030 | Yarizo khoe mẽ trước PM | Ch.8 |
| 4 | EV012 | PM thighjob (羁绊3) | Ch.9 |
| 5 | EV031 | PM bunny suit + Yarizo NTR trước PM | Ch.10 |
| 6 | EV032 | Jimmy+Kohaku sex trước mặt PM | Ch.10 |
| 7 | EV033 | Jimmy liếm đít PM | Ch.10 |
| 8 | EV034 | Anemone trap scene | Ch.11 |
| 9 | (CG) | PM footjob / rimjob series | Ch.15 |

---

### 莉莉丝 (Lilith) Timeline Card

**JOIN EVENT**
- Map: Map008 (澡堂/Bathhouse area), EV013
- Context: `"\\n[10]隔着一堵墙洗澡… 那是……\\n[10]……！"` — Jimmy nghe Lilith tắm qua vách
- Condition: main_progress >= 1, sau khi đến Vương Đô
- Novel Chapter: **Ch.8** (khu nhà tắm sự kiện)

**BOND PROGRESSION**
| Bond | Event/CE | Description | Earliest Chapter |
|------|---------|-------------|-----------------|
| 0 | Map008 EV013 | Nghe Lilith tắm qua vách | Ch.8 |
| 1 | CE309 (露营2) | Lilith camping lần 1 | Ch.9 |
| 2 | CE310 (露营3) | Lilith "muốn hút" | Ch.9 |
| 3 | EV020 | Lilith xem Jimmy+Kohaku làm | Ch.10 |
| 4 | Map065 EV2 P2 | **Lilith BJ** (main_progress=2) | Ch.11 |
| 5 | EV021 | Lilith nhận "đại cặc đẩy tử cung" | Ch.13 |
| 6 | CE308 | Lilith battle loss (goblin) | Battle |

---

## Critical Note for Screenwriter

**Yarizo và PM đều gặp nhóm ở Vương Đô (Ch.7), nhưng:**
- Yarizo → tự giới thiệu khiêu khích ngay tại Unicorn Tavern
- PM → gặp tình cờ trên phố, sau đó mới có quest

**Lilith gặp gỡ TRƯỚC** tại khu nhà tắm (Ch.8), không phải tại Unicorn Tavern.

**Không có companion nào làm R18 trong Ch.1-6.** Đây là giai đoạn Kohaku+Jimmy với:
- Goblin followers (từ rừng)
- NPC encounters (không tên)
- Kohaku's internal corruption arc
