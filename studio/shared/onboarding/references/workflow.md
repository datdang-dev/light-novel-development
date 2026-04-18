---
name: 'project-onboarding'
description: 'Context Grounding session to give Meta-Agents full project awareness before discussion or planning tasks.'
---

# Project Onboarding Workflow

**Purpose:** Ground the current AI agent with comprehensive project context so it can participate effectively in strategic discussions, architectural reviews, party mode sessions, or roleplay.

## RULES

- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese
- MUST follow exact sequence below
- DO NOT skip any file — if a file is missing, note it and continue

---

## SEQUENCE OF INSTRUCTIONS

### 1. Load Studio Identity

Read and internalize the following files:

- `{project-root}/studio/module.yaml` — Module definition, version, and dependencies
- `{project-root}/studio/agent-registry.csv` — Full roster of all specialist agents
- `{project-root}/studio/config/pipeline-context.md` — Master pipeline rules, architecture constraints, delegation protocols

**OUTPUT:**

```text
📋 Đã nạp Studio Identity:
  - Module: {module_name} v{version}
  - Agents đang hoạt động: {agent_count}
  - Pipeline Architecture: V6.1
```

### 2. Load World & Lore Context

Read and internalize the following files (if they exist):

- `{project-root}/studio/knowledge/glossaries/hentai_lexicon.md` — Domain-specific vocabulary
- `{project-root}/studio/knowledge/fetish-db/README.md` — Fetish categorization system
- `{project-root}/studio/core/lewd-writer/data/gooner-manifesto.md` — Core writing philosophy

**OUTPUT:**

```text
🌍 Đã nạp World Context:
  - Lexicon: {loaded/not_found}
  - Fetish DB: {loaded/not_found}
  - Manifesto: {loaded/not_found}
```

### 3. Load Active Project State (if exists)

Check for active pipeline state:

- Scan `{output_folder}/_pipeline/` for any `state.yaml` files
- If found, read the most recent one and extract: `project`, `chapter`, `current_page`, `status`, `pages_processed`

**IF STATE EXISTS — OUTPUT:**

```text
🎯 Dự án đang hoạt động:
  - Project: {project}
  - Chapter: {chapter}
  - Tiến độ: {pages_processed.length}/{pages_total} pages
  - Trạng thái: {status}
```

**IF NO STATE — OUTPUT:**

```text
💤 Không có dự án đang chạy. Sẵn sàng cho brainstorming hoặc review.
```

### 4. Load Character Bible (if exists)

Check `{output_folder}/_bible/` for any project folders:

- If found, list the available character bible files
- Read the index or first 2-3 character files to understand the cast

**OUTPUT:**

```text
👥 Character Bible:
  - {character_count} nhân vật đã được lập hồ sơ
  - Nhân vật chính: {main_characters}
```

### 5. Load Writing Rules

Read the critical `studio/rules/` files:

- `{project-root}/studio/rules/lewd_writing_mechanics.md`
- `{project-root}/studio/rules/sensory_density.md`
- `{project-root}/studio/rules/dialogue_format.md`
- `{project-root}/studio/rules/character_voice.md`

**OUTPUT:**

```text
📏 Đã nạp {count} quy tắc viết bắt buộc.
```

### 6. Present Onboarding Summary

**OUTPUT:**

```text
✅ ONBOARDING HOÀN TẤT!

Tôi ({agent_name}) đã nắm bắt toàn bộ bối cảnh của LND Studio:
  - Kiến trúc Studio và {agent_count} agents
  - Lore, thế giới quan, và hệ thống fetish
  - Dự án hiện tại: {project_status}
  - {character_count} nhân vật trong bible
  - {rules_count} quy tắc viết R18

Giờ bạn muốn thảo luận / review / planning gì, {user_name}?
```

**HALT and wait for user input.**

---

## VERIFICATION CHECKLIST

- [ ] Studio Identity loaded (module.yaml, agent-registry, pipeline-context)
- [ ] World Context loaded (lexicon, fetish-db, manifesto)
- [ ] Active Project State checked
- [ ] Character Bible scanned
- [ ] Writing Rules loaded
- [ ] Summary presented to user
