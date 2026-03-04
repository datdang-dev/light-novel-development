# Step 01: Build Release Manifest

**Goal:** Create the single source of truth for the release package.

## Instructions

1. **Locate Target**: Identify the target release directory (e.g., `_lnd-output/_release/anata_no_semen_kaishuu_shimasu_4_alpha/`).
2. **Scan Assets**: Scan the directory to identify all files inside `novel/base/`, `novel/modded/`, and `roleplay/`.
3. **Determine Version**: Ask the user or determine the appropriate Semantic Version (e.g., `v0.1.0-alpha`, `v1.0.0`).
4. **Create JSON**: Create a file named `release_manifest.json` in the root of the release directory.

### Mandatory Manifest Structure

```json
{
  "project": "[Project Name]",
  "version": "[Version]",
  "release_date": "[YYYY-MM-DD]",
  "studio": "LND Studio",
  "content_warnings": [
    "R18+",
    "Mind-break",
    "Consent Issues (if applicable)"
  ],
  "assets": {
    "novel": {
      "base_pages": ["[list of relative paths]"],
      "modded_pages": ["[list of relative paths]"]
    },
    "roleplay": {
      "context_files": ["[list of relative paths]"]
    }
  }
}
```

## Completion

Once the `release_manifest.json` is successfully written and saved, proceed immediately to `./step-02-web-chat-kit.md`. Do not wait for confirmation unless clarification on Version/Tags is needed.
