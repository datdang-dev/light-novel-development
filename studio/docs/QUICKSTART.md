# 🚀 LND Studio V7.0 — Quickstart Guide

Welcome to LND Studio, the Ultimate Multi-Agent Japanese R18 Prose Adaptation Engine. This guide will take you from zero to running your first full AI-driven manga adaptation in 5 simple steps.

---

## Step 1: Bootstrap the Project Root

For the AI agents to locate their files reliably, you must explicitly declare the project root. 
1. Open the file `studio/config/BOOTSTRAP.md`.
2. Ensure the `PROJECT_ROOT` path perfectly matches the absolute path of your LND Studio directory (e.g., `/home/username/working/lnd_dev`). 

*Note: All agents run a critical action on boot to read this file and set their internal `{project-root}` variable.*

---

## Step 2: Configure the Environment

Open `studio/config/config.yaml` (if it doesn't exist, create it using the `CONFIG_GUIDE.md` reference) and set your basic parameters:
- `output_folder`: Where you want the final `.md` files saved (e.g., `_lnd_output`).
- `communication_language`: Usually `Vietnamese`.

---

## Step 3: Initialize Your Manga Payload

For the flagship Gooner-Alchemist pipeline, the AI needs source material:
1. Create a folder for your target manga (e.g., `sources/mangas/My_Manga`).
2. Populate it with images (`001.webp`, `002.webp`, etc.).
3. If this is a Chinese or Japanese raw, ensure OCR is ready or wait for the system to process it during the Forensic Phase.

---

## Step 4: Run the Gooner Alchemist Pipeline

With the root, config, and files ready, it's time to invoke the master orchestrator, **Director K**.

In your IDE or chat interface, type:
`/gooner-alchemist`

This command wakes up the Orchestrator, who will:
1. Load your `BOOTSTRAP.md`.
2. Discover the target manga pages.
3. Delegate **Panel Forensics** to *Kana* and *Dr. Atomic*.
4. Hand the forensic data to **Suki** to write the explicit prose.
5. Have **Riko** audit the prose against the 100-point gooner rubric.

You just sit back and watch the agents pass files to each other.

---

## Step 5: Iteration & Customization

If a draft fails the audit, the system will auto-retry up to 3 times before asking for your help.
- **Want to change Character Voice?** Run `/character-architect` to build a robust profile.
- **Need to adjust the Fetish Focus?** Modify `context_payload.md` or the databases in `studio/knowledge/`.
- **Custom Workflows?** See the `.agent/workflows/` directory for additional commands like `/renpy-adaptation` and `/lewd-writer`.

Enjoy the automated gooner perfection!
