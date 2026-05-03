---
name: gallery-info
description: Retrieve and display detailed information about a specific Hitomi.la gallery
---

# Gallery Info Capability

## Overview

Retrieve comprehensive metadata for a specific gallery by ID, including all tags, artists, characters, languages, related galleries, and provide a summary assessment for LND pipeline compatibility.

## Execution Steps

### Step 1: Parse Gallery ID

Accept:
- Numeric ID: `3444767`
- URL: `https://hitomi.la/doujinshi/title-3444767.html` → extract `3444767`
- Title from previous search → map to ID

### Step 2: Retrieve Gallery

```javascript
import hitomi from 'node-hitomi';

const gallery = await hitomi.galleries.retrieve(GALLERY_ID);
```

### Step 3: Extract All Metadata

```javascript
const info = {
    id: gallery.id,
    title: gallery.title?.display,
    titleJapanese: gallery.title?.japanese,
    type: gallery.type,
    languages: gallery.languages?.map(l => l.name),
    artists: gallery.artists?.map(a => a.name),
    groups: gallery.groups?.map(g => g.name),
    characters: gallery.characters?.map(c => c.name),
    series: gallery.series?.map(s => s.name),
    tags: gallery.tags?.map(t => ({ name: t.name, url: t.url })),
    pageCount: gallery.files?.length,
    date: gallery.date,
};
```

### Step 4: Pipeline Assessment

Evaluate suitability for LND prose adaptation:

| Factor | Good | Problematic |
|--------|------|-----------|
| **Page Count** | 15-50 pages | <5 or >100 |
| **Language** | Japanese (OCR), English | No text |
| **Type** | Doujinshi, Manga | CG Set (no panels) |
| **Tags** | Story-driven fetish tags | Pure gallery/pin-up |
| **Text Density** | Dialogue-heavy | Textless/silent |

### Step 5: Output Report

```markdown
# Gallery Info: [Title]

## Basic Info
| Field | Value |
|-------|-------|
| **ID** | [id] |
| **Title** | [display_title] |
| **Title (JP)** | [japanese_title] |
| **Type** | [type] |
| **Artist** | [artists] |
| **Group** | [groups] |
| **Series** | [series] |
| **Characters** | [characters] |
| **Languages** | [languages] |
| **Pages** | [page_count] |
| **Date** | [date] |

## Tags
[comma-separated full tag list with counts if available]

## LND Pipeline Assessment
- **Suitability:** ⭐⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐
- **Recommended Pipeline:** [/gooner-alchemist | /panel-forensic only | /lnd-orchestrator]
- **Notes:** [assessment notes]

## Quick Actions
- Download: "download gallery [id]"
- Find similar: "recommend similar to [id]"
- Find more by artist: "search artist:[artist_name]"
```
