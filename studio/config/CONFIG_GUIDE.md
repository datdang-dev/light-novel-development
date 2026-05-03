# LND Studio Configuration Guide

This document outlines the keys that clients should configure for their specific project instances. Ideally, these are placed in `studio/config/config.yaml`.

## Core Variables

### `project_name`
- **Description**: The working title of the current adaptation project.
- **Example**: `Namaiki_Mesugaki_Vol1`

### `output_folder`
- **Description**: The absolute or relative path where generated prose, audit reports, and final chapters are saved.
- **Example**: `_lnd_output/`

### `communication_language`
- **Description**: The primary language the agents use to write the output prose and communicate with you.
- **Example**: `Vietnamese` (Required for standard LND framework).

### `document_output_language`
- **Description**: Specifically for technical documents, audit reports, and metadata blocks.
- **Example**: `English` or `Vietnamese`.

## Project-Specific Overrides (Optional)

In some cases, you may want to override global behavior for a specific project without modifying the core `studio/rules/`. You can define:

### `target_audit_score_override`
- **Description**: If you wish to lower or raise the minimum passing score from the default `85`.
- **Example**: `90` (Stricter) or `70` (Looser).

### `banned_words_list`
- **Description**: A custom list of words that Suki is forbidden from using in this specific project.
- **Example**: `["thịt", "giao cấu"]`

## How Agents Use This

The Orchestrator agent reads this configuration during the **Phase 0: Discovery & Bible Sync** step and injects these values into the `context_payload.md` — which is passed dynamically to all downstream specialists (Kana, Suki, Riko) at runtime.
