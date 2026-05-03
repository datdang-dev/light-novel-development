---
name: search
description: Search Hitomi.la galleries by tags, artist, or combined query
---

# Search Capability

## Overview

Search Hitomi.la for galleries matching specific tags, artists, characters, or combined queries. Produce a structured markdown report with results.

## Execution Steps

### Step 1: Parse User Intent

Extract search parameters from user request:
- **Tags** (e.g., gyaru, schoolgirl, condom, bitch, dark_skin, netorare)
- **Artist** (e.g., pija, shiomaneki, distance)
- **Character** (e.g., kanagi haruka)
- **Sort order** — default: `PopularityAllTime`
- **Result limit** — default: 30
- **Language filter** — optional (japanese, english, chinese, korean)

### Step 2: Build Query

Construct the `node-hitomi` query:

```javascript
import hitomi, { SortType } from 'node-hitomi';

// Tag-based search (recommended — most accurate)
const tags = hitomi.tags.parse('female:gyaru female:dark_skin tag:condom');
const refs = await hitomi.galleries.list({
    tags: tags,
    orderBy: SortType.PopularityAllTime
});

// Artist search
const refs = await hitomi.galleries.list({
    tags: hitomi.tags.parse('artist:pija'),
    orderBy: SortType.Date
});
```

**Tag prefix rules:**
| Prefix | Usage | Example |
|--------|-------|---------|
| `female:` | Female-specific tags | `female:gyaru`, `female:big_breasts` |
| `male:` | Male-specific tags | `male:shotacon` |
| `tag:` | General tags | `tag:condom`, `tag:full_color` |
| `artist:` | Artist name | `artist:pija` |
| `character:` | Character name | `character:kanagi_haruka` |
| `language:` | Language filter | `language:japanese` |
| `type:` | Content type | `type:doujinshi`, `type:manga` |

### Step 3: Retrieve Details

For the top results (limit = user preference, default 30), retrieve full gallery details:

```javascript
for (const ref of refs.slice(0, limit)) {
    const g = await ref.retrieve();
    // Safe property access:
    const title = g.title?.display ?? `Gallery ${g.id}`;
    const artists = g.artists?.map(a => a.name).join(', ') ?? 'Unknown';
    const tags = g.tags?.map(t => t.name).join(', ') ?? '';
    const pages = g.files?.length ?? '?';
}
```

> **IMPORTANT:** The `list()` method returns gallery *references*. You MUST call `.retrieve()` on each reference to get full metadata. If you skip this step, properties like `title`, `tags`, `artists` will be undefined.

### Step 4: Generate Report

Output a markdown file to `{project-root}/hitomi_test/{report_name}.md`:

```markdown
# Kết Quả Tìm Kiếm: [query description]

**Query:** [raw tag query]
**Sort:** [sort method]
**Kết quả:** [total_count] (hiển thị [shown_count] đầu tiên)

---

### 1. [Title](https://hitomi.la/galleries/{id}.html)
- **ID:** {id}
- **Artist:** {artists}
- **Language:** {languages}
- **Type:** {type}
- **Tags:** {tags}
- **Pages:** {pages}
```

### Step 5: Optional — Download Thumbnails

If user wants visual preview, download cover thumbnails:

```javascript
const thumbs = gallery.getThumbnails();
if (thumbs?.length > 0) {
    const buf = await thumbs[0].fetch(Extension.Webp, ThumbnailSize.Small);
    writeFileSync(`thumbnails/${gallery.id}.webp`, buf);
}
```

## Common Search Patterns

### By Theme (Kanagi Haruka style)
```
female:gyaru female:schoolgirl_uniform tag:condom female:dark_skin
```

### By Fetish Combo
```
female:mesugaki female:paizuri female:sweating
```

### By Artist Portfolio
```
artist:pija type:doujinshi
```

### By Character
```
character:kanagi_haruka
```
