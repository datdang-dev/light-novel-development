---
name: recommend
description: Generate curated manga recommendations based on themes, tags, or reference galleries
---

# Recommend Capability

## Overview

Generate curated hentai manga recommendations based on a reference gallery, theme description, or tag combination. Produce a ranked report with download-ready gallery IDs.

## Execution Steps

### Step 1: Understand User Preference

Accept one of:
- **Reference Gallery** — "find manga similar to gallery 3444767"
- **Theme Description** — "gyaru schoolgirl with condom play" or "tìm truyện giống Kanagi Haruka"
- **Tag Combination** — explicit tags the user wants
- **Artist Style** — "more by artist pija" or similar artists

### Step 2: Build Tag Profile

If starting from a reference gallery, extract its tag profile:

```javascript
const ref = await hitomi.galleries.retrieve(GALLERY_ID);
const tagProfile = ref.tags.map(t => t.name);
// Use the top tags as search basis
```

If starting from theme description, translate to tags:

| Theme | Recommended Tags |
|-------|-----------------|
| Gyaru schoolgirl | `female:gyaru female:schoolgirl_uniform` |
| Corruption/NTR | `female:netorare tag:cheating` |
| Mesugaki/bratty | `female:mesugaki female:femdom` |
| Dark skin tanned | `female:dark_skin female:gyaru` |
| Used condom/trophy | `tag:condom female:prostitution` |
| Athletic/swimsuit | `female:swimsuit female:muscle` |

### Step 3: Multi-Query Search

Run multiple searches with different tag combos and sort methods to get diverse results:

```javascript
const searches = [
    { tags: 'female:gyaru tag:condom', sort: SortType.PopularityAllTime },
    { tags: 'female:gyaru female:schoolgirl_uniform', sort: SortType.PopularityMonth },
    { tags: 'female:dark_skin female:gyaru', sort: SortType.Date },
];

const allResults = new Map(); // dedupe by ID
for (const s of searches) {
    const refs = await hitomi.galleries.list({
        tags: hitomi.tags.parse(s.tags),
        orderBy: s.sort
    });
    for (const ref of refs.slice(0, 15)) {
        const g = await ref.retrieve();
        if (!allResults.has(g.id)) allResults.set(g.id, g);
    }
}
```

### Step 4: Score & Rank

Score each gallery based on:
1. **Tag overlap** with user's desired tags (higher = better)
2. **Page count** (prefer 15+ pages for prose adaptation)
3. **Language availability** (Japanese preferred for OCR pipeline)
4. **Artist reputation** (known artists get bonus)

### Step 5: Generate Recommendation Report

```markdown
# Đề Xuất Manga: [Theme]

**Dựa trên:** [reference or user description]
**Số lượng:** [count] bộ được đề xuất

---

## 🏆 Top Picks

### 1. [Title](https://hitomi.la/galleries/{id}.html)
- **ID:** {id} — `dùng ID này để download`
- **Artist:** {artists}
- **Tags:** {tags}
- **Pages:** {pages}
- **Lý do đề xuất:** [why this matches]

---

## 📋 Danh Sách Đầy Đủ

| # | Title | Artist | Pages | Key Tags |
|---|-------|--------|-------|----------|
| 1 | [Title](url) | artist | 24 | gyaru, condom |
| 2 | ... | ... | ... | ... |

## 🔗 Quick Download Commands

Để tải về bất kỳ bộ nào, nói: "download gallery [ID]"
```

### Step 6: Optional — Thumbnail Gallery

Download cover thumbnails for visual browsing:

```javascript
const thumbDir = `{project-root}/hitomi_test/thumbnails_{theme}/`;
for (const [id, g] of allResults) {
    const thumbs = g.getThumbnails();
    if (thumbs?.length > 0) {
        const buf = await thumbs[0].fetch(Extension.Webp, ThumbnailSize.Small);
        const safeName = g.title?.display?.replace(/[\/\?<>\\:\*\|":]/g, '').substring(0, 50) ?? id;
        writeFileSync(path.join(thumbDir, `${id} - ${safeName}.webp`), buf);
    }
}
```

## Recommendation Strategies

### "More Like This"
Extract tags from a reference gallery → search for galleries sharing 3+ common tags.

### "Same Artist"
Find all works by the same artist → sort by popularity.

### "Escalation" 
Start with user's current comfort tags → add progressive fetish tags (e.g., gyaru → gyaru+prostitution → gyaru+group).

### "Complementary"
If user likes gyaru+condom, suggest the inverse/complement: schoolgirl+nakadashi (no condom).
