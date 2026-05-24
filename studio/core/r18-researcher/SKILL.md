---
name: r18-researcher
description: Kuro's R18 Research & Downloader Engine. Harvests fetish references, downloads R18 assets
  (novels, manga, illustrations), and extracts natural Japanese R18 prose style guides from Syosetu.
injection:
  always:
  - '{{project_root}}/studio/rules/user_fetish_profile.md'
  - '{{project_root}}/studio/rules/anti_slop.md'
  triggers:
  - research_tag: explicit|r18|fetish|download
    loads:
    - '{{project_root}}/studio/rules/xcom_degenerate_style.md'
---

# R18 Research & Downloader Engine

## Overview

The R18 Research & Downloader Engine enables the LND Studio workspace to acquire, structure, and analyze adult creative materials. It handles automatic multi-source resource acquisition and analyzes Japanese R18 literature to build structural blueprints for premium prose generation.

**Core Philosophy:** Authentic reference material breeds authentic creative execution. Kuro operates the downloading pipeline and extracts deep prose insights without compromises.

## Capabilities

### 1. Unified R18 Downloader
Kuro uses the unified python tool `studio/tools/r18_downloader.py` to fetch:
- **Syosetu / Nocturne R18 Novels**: Downloads all chapters, prefaces, and afterwords to clean, organized Markdown files.
- **Hitomi.la**: Interfaces with `node-hitomi` to download high-fidelity WebP manga assets.
- **nhentai**: Integrates with the Turkish/English `nhentai-downloander` package.
- **Telegraph / Teletype**: Direct thread-pool scraping of high-speed image galleries.

### 2. Erotic Fetish & Tag Research (RH)
Uses direct authenticated crawler search to extract:
- Popular fetish tag clusters.
- Trend analyses in the R18 Japanese target market.
- Recommendations for specific titles/tags matching the `user_fetish_profile.md`.

### 3. Novel Prose Learning (RL)
Analyzes scraped Syosetu Nocturne novels to extract:
- **Pacing Topology**: Ratio of dialogue, description, internal monologues, and explicit actions.
- **Sensory Vocabulary**: Key Japanese and localized English verbs/nouns used to depict fluids, heat, physical feedback, and psychological transformations.
- **Degradation Patterns**: Authentic corner-bracket Japanese formatting and emotional escalation loops.

---

## Workflows & Commands

### [RD] Run Downloader
Triggers the universal scraper/downloader script:
`python3 studio/tools/r18_downloader.py <URL_or_ID>`

Output is structured and stored:
- **Novels**: `sources/novels/<Title>/chapters/chapter_001.md`, etc. + `metadata.json`
- **Manga / Images**: `sources/manga/<Title>/page_001.webp`, etc. + `info.json`

### [RH] Research Hentai Fetishes
To run a research sweep for specific terms or tags:
1. Load `{{project_root}}/studio/rules/user_fetish_profile.md` to establish core target kinks.
2. Standard web search engine (`search_web`) is age-gated/censored for Nocturne. **DO NOT** use `search_web` to scan Nocturne directly.
3. Instead, run programmatic searches using the tool CLI:
   `python3 studio/tools/r18_downloader.py --search "<Japanese_Query>"`
4. Generate a structured `research_results.md` mapping:
   - Popular tag clusters.
   - Narrative tropes and setups.
   - Recommended novel IDs or doujin tags.

### [RL] Novel Learning Mode
To extract prose style patterns from a downloaded Syosetu novel:
1. Run the automated prose analyzer:
   `python3 studio/tools/r18_downloader.py --analyze <Novel_ID_or_Path>`
2. Read the generated `analysis_prose.md` file inside the novel directory to capture:
   - Pacing topology (Dialogue vs Monologue vs Action ratios).
   - Frequency of key R18 verbs, nouns, and SFX.
3. Create a clean prose blueprint `sources/novels/<Novel_Title>/analysis_prose.md` to help the prose generator.

---

## Quality Gates

- [ ] Does the download run without interactive prompts?
- [ ] Are crawled Syosetu novels split into structured chapter files (not a single giant dump)?
- [ ] Are prefaces and afterwords extracted and labeled clearly?
- [ ] Does prose analysis use `--analyze` and generate a structured markdown report?
- [ ] Are all manga assets saved in high-fidelity WebP/PNG/JPG (no missing pages)?
