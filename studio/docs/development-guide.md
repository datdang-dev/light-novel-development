# 🚀 Development and Operations Guide 🚀

> **Comprehensive System Setup, Testing, and Pipeline Extension Guide**
> Practical reference for developers and AI agents maintaining the LND Studio workspace.

---

## 🛠️ Sandbox Setup & Dependencies

LND Studio uses a Python 3.10+ virtual environment for core execution scripts and JSON schema validation, alongside Node.js for CLI tools.

### 1. Initialize Virtual Environment
Ensure you are in the project root and activate the pre-configured virtual environment:
```bash
# Activate the virtual environment
source .venv/bin/activate

# Verify Python version and environment path
python --version
pip list
```

### 2. Node Dependencies
For CLI automation and dev-server controls:
```bash
# Install node packages (if modifying frontend adapter dashboards)
npm install
```

---

## 📦 Command Reference Guide

The following commands are available for manual execution and testing:

| Task | Command | Directory |
| :--- | :--- | :--- |
| **Launch Orchestrator** | `./studio/tools/launch_orchestrator.sh` | Project Root |
| **Run Manga OCR** | `python studio/scripts/manga_ocr_processor.py` | Project Root |
| **Run Gooner Audit** | `python studio/scripts/run_audit_check.py --input studio/output/draft.md` | Project Root |
| **Validate Schemas** | `python studio/scripts/validate_schemas.py` | Project Root |
| **Clean Temp Output** | `rm -rf studio/output/*` | Project Root |

---

## 🧪 Testing & QA Operations

All new pipelines, scripts, and rules must be thoroughly validated to prevent drift.

### 1. Run Automated Unit Tests
To execute python test suites covering adapters and schema checks:
```bash
pytest tests/
```

### 2. Sandbox Verification Gate
Before proposing any code change:
1. Verify all modified `.py` files conform to PEP 8 standards.
2. Run schema validators on any modified `.schema.json` contract:
   ```bash
   python studio/scripts/validate_schemas.py --all
   ```
3. Run the dry-run orchestrator to test the `state.yaml` resume logic:
   ```bash
   ./studio/tools/launch_orchestrator.sh --dry-run
   ```

---

## 🏗️ How to Extend the Studio

To add a new specialized capability or service to LND Studio, follow these steps:

### 1. Structure Checklist
Every new component (e.g. `studio/services/new-service/`) must contain:
```text
new-service/
├── SKILL.md            # Entry point containing YAML triggers and execution map
├── steps/              # Step markdown/json scripts
├── references/         # Static guidelines used by the step
├── resources/          # State structures
└── tools/              # Helper python scripts
```

### 2. Register Your Component
1. Add the component to the dynamic dispatch registry: `studio/agents/agent-registry.yaml`.
2. Map the capability under Director K's owned or delegated list in `studio/agents/lnd-orchestrator.agent.yaml`.
3. Test activation using `/new-service` slash command equivalent in your local terminal.
