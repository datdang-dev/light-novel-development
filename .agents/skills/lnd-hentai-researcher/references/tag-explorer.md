---
name: tag-explorer
description: Explore and discover Hitomi.la tags for research planning
---

# Tag Explorer Capability

## Overview

Explore the Hitomi.la tag taxonomy to discover valid tags, find related tags, and understand tag frequency. Essential for building precise search queries.

## Execution Steps

### Step 1: Identify User's Interest

What the user wants to explore:
- **Autocomplete** — "what tags exist for 'mesugaki'?"
- **Discovery** — "what female tags are popular?"
- **Validation** — "is 'pantyjob' a valid tag?"
- **Related** — "tags similar to 'gyaru'"

### Step 2: Tag Search (Autocomplete)

```javascript
import hitomi from 'node-hitomi';

const results = await hitomi.tags.search('mesugaki');
// Returns: [['female:mesugaki', 1234], ['male:mesugaki', 56], ...]
// Each entry: [fullTagName, galleryCount]

for (const [tag, count] of results.slice(0, 20)) {
    console.log(`${tag} (${count} galleries)`);
}
```

### Step 3: Multi-Term Discovery

For exploring multiple related terms:

```javascript
const terms = ['gyaru', 'bitch', 'schoolgirl', 'condom', 'dark_skin', 'tan'];
for (const term of terms) {
    const results = await hitomi.tags.search(term);
    const top5 = results.slice(0, 5).map(([tag, count]) => `${tag} (${count})`);
    console.log(`"${term}": ${top5.join(', ')}`);
}
```

### Step 4: Report Format

```markdown
# Tag Explorer Report

## Search Terms

| Term | Top Matches |
|------|-------------|
| gyaru | female:gyaru (12345), tag:gyaru (234) |
| bitch | tag:bitch (5678), female:bitch (456) |

## Recommended Queries

Based on your interests, here are optimized search queries:

1. **Gyaru + School setting:** `female:gyaru female:schoolgirl_uniform tag:condom`
2. **Dark skin combo:** `female:dark_skin female:gyaru female:big_breasts`
```

## Tag Categories Reference

### Popular Female Tags (R18)
| Tag | Description |
|-----|-----------|
| `female:gyaru` | Tanned/fashion girl archetype |
| `female:schoolgirl_uniform` | School uniform |
| `female:big_breasts` | Large breasts |
| `female:dark_skin` | Dark/tanned skin |
| `female:stockings` | Wearing stockings |
| `female:sweating` | Sweating depiction |
| `female:mesugaki` | Bratty girl (cheeky/provocative) |
| `female:paizuri` | Breast sex |
| `female:nakadashi` | Creampie |
| `female:defloration` | First time |
| `female:ahegao` | Exaggerated pleasure face |

### Popular General Tags
| Tag | Description |
|-----|-----------|
| `tag:condom` | Condom usage depicted |
| `tag:full_color` | Full color artwork |
| `tag:mosaic_censorship` | Mosaic censoring |
| `tag:uncensored` | No censorship |

### Type Filters
| Filter | Description |
|--------|-----------|
| `type:doujinshi` | Fan/indie works |
| `type:manga` | Published manga |
| `type:artistcg` | Artist CG sets |
| `type:gamecg` | Game CG sets |
| `type:anime` | Anime content |
