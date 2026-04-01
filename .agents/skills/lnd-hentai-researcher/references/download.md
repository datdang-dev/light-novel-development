---
name: download
description: Download full gallery images from Hitomi.la by gallery ID
---

# Download Capability

## Overview

Download all pages of a Hitomi.la gallery to the local filesystem for pipeline processing.

## Execution Steps

### Step 1: Identify Gallery

Accept one of:
- **Gallery ID** (numeric, e.g., `3444767`)
- **Hitomi URL** (e.g., `https://hitomi.la/doujinshi/title-123456.html`) → extract the numeric ID
- **Title from previous search** → look up ID from search results

### Step 2: Determine Output Directory

Default pattern: `{project-root}/sources/manga/{Sanitized_Title}/`

Sanitize the title:
- Replace `/\?<>\:*|"` with empty string
- Replace spaces with `_`
- Capitalize first letter of each word (Title_Case)
- Truncate to 60 characters if needed

### Step 3: Execute Download

Use `./scripts/download-gallery.mjs` or generate inline:

```javascript
import hitomi, { Extension } from 'node-hitomi';
import { writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';

const GALLERY_ID = <user_provided_id>;
const OUT_DIR = '<computed_output_path>';

async function run() {
    if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

    console.log('Retrieving gallery...');
    const gallery = await hitomi.galleries.retrieve(GALLERY_ID);
    console.log(`Title: ${gallery.title.display}`);
    console.log(`Total pages: ${gallery.files.length}`);

    let success = 0, failed = 0;

    for (let i = 0; i < gallery.files.length; i++) {
        const pageNum = String(i + 1).padStart(3, '0');
        const outPath = path.join(OUT_DIR, `page_${pageNum}.webp`);

        if (existsSync(outPath)) { success++; continue; }

        try {
            const buffer = await gallery.files[i].fetch(Extension.Webp);
            writeFileSync(outPath, buffer);
            success++;
            if (success % 10 === 0) console.log(`[${success}/${gallery.files.length}]`);
        } catch (e) {
            // Retry once after 2s
            try {
                await new Promise(r => setTimeout(r, 2000));
                const buffer = await gallery.files[i].fetch(Extension.Webp);
                writeFileSync(outPath, buffer);
                success++; 
            } catch (e2) {
                failed++;
                console.error(`[page_${pageNum}] Failed: ${e2.message}`);
            }
        }
    }
    console.log(`Done! Success: ${success}, Failed: ${failed}`);
}
run();
```

### Step 4: Verify Download

After download completes, verify:
1. Count files in output directory
2. Compare against expected page count from gallery metadata
3. Report any missing pages

### Step 5: Report

```markdown
# Download Report: [Title]

- **Gallery ID:** [id]
- **Artist:** [artist]
- **Pages:** [downloaded]/[total]
- **Output:** `sources/manga/[Title]/`
- **Status:** ✅ Complete | ⚠️ Partial ([missing] pages failed)

## Next Steps
- Run `/panel-forensic` for visual analysis
- Run `/gooner-alchemist` for full prose pipeline
```

## Resumable Downloads

The script automatically skips already-downloaded files (`existsSync` check), so re-running is safe and will only download missing pages.

## Batch Downloads

For downloading multiple galleries, generate a loop script:

```javascript
const GALLERY_IDS = [123456, 234567, 345678];
for (const id of GALLERY_IDS) {
    // ... download each with sanitized title as directory name
}
```
