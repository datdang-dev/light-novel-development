# LND Studio Developers Framework

**Version:** 2.0.0 (Phase 2 Complete)  
**Last Updated:** 2026-05-16  
**Status:** Production Ready

---

## Overview

The LND Studio Developers Framework is a multi-agent orchestration system for coordinating AI agents in content adaptation workflows. It provides declarative mode configuration, schema validation, lazy knowledge loading, and extensible agent coordination.

**Key Features:**
- 🎯 **Zero-Code Mode Extension** - Add new modes via YAML only
- 📊 **Schema Validation** - Pydantic-based output validation
- 🧠 **Lazy Knowledge Loading** - 80% token reduction
- 🔄 **Multi-Agent Coordination** - Single, sequential, and debate modes
- 🛡️ **Legacy Prevention** - Pre-commit hooks block technical debt
- 📝 **XML Context Wrapping** - Structured context injection

---

## Architecture

```
studio/developers/
├── config/
│   ├── mode_registry.yaml          # Declarative mode configuration
│   ├── templates/                  # Prompt templates
│   │   ├── arch_review.md
│   │   ├── code_review.md
│   │   └── ...
│   └── roles/                      # Knowledge base
│       ├── se/rules/               # Software engineering rules
│       ├── dev/rules/              # Development rules
│       └── qa/rules/               # QA rules
├── orchestrator.py                 # Main orchestration engine
├── mode_registry.py                # Registry loader & validator
├── schemas.py                      # Pydantic output schemas
├── agents/
│   ├── base.py                     # Base agent class
│   ├── registry.py                 # Agent factory
│   └── mock_agent.py               # Testing mock
└── knowledge_index.py              # Knowledge loading system
```

---

## Quick Start

### 1. Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r studio/developers/requirements.txt
```

### 2. Run Orchestrator

```bash
python3 -m studio.developers.orchestrator \
  --task my-review \
  --mode arch \
  --prompt "Review this architecture" \
  --agents hermes:se/m-architect \
  --files path/to/file.py
```

### 3. Check Output

```bash
ls _out/agent-sessions/my-review/
# hermes_last.md    - Agent output
# context.md        - Session context
```

---

## Mode Registry

### Available Modes

| Mode | Type | Description | Agents |
|------|------|-------------|--------|
| `arch` | single | Architecture review | 1 (se/m-architect) |
| `code` | single | Code/prose review | 1 (dev/m-writer) |
| `review` | sequential | Arch + Code review | 2 (architect + writer) |
| `cross` | debate | Multi-agent debate | 2+ (any roles) |
| `qa` | single | Quality audit | 1 (qa/m-auditor) |

### Adding a New Mode

Edit `config/mode_registry.yaml`:

```yaml
modes:
  mymode:
    description: "My custom mode"
    execution_type: "single"
    template: "my_template.md"
    output_schema: "MyOutput"
    knowledge_namespaces: ["custom"]
    knowledge_files:
      custom:
        - "rules.md"
```

**No code changes required!** See `MODE_REGISTRY_GUIDE.md` for details.

---

## Agent System

### Agent Roles

Agents are defined by role paths: `{namespace}/{tier}-{specialty}`

**Examples:**
- `se/m-architect` - Software Engineering Master Architect
- `dev/m-writer` - Development Master Writer
- `qa/m-auditor` - QA Master Auditor

### Creating Agents

```python
from studio.developers.agents.registry import create_agent

agent = create_agent(
    agent_id="hermes",
    role="se/m-architect",
    config_dir=Path("studio/developers/config")
)
```

### Agent Capabilities

Each agent has:
- **Role-specific knowledge** - Loaded from `config/roles/{namespace}/rules/`
- **Prompt building** - Constructs prompts from templates
- **Schema validation** - Validates output against Pydantic schemas
- **Context management** - Maintains session context

---

## Knowledge System

### Knowledge Namespaces

| Namespace | Purpose | Location |
|-----------|---------|----------|
| `se` | Software engineering rules | `config/roles/se/rules/` |
| `dev` | Development guidelines | `config/roles/dev/rules/` |
| `qa` | Quality assurance | `config/roles/qa/rules/` |

### Lazy Loading

Specify exact files to load (recommended):

```yaml
knowledge_files:
  se:
    - "global_rule_hub.md"
    - "delegation_protocol.md"
    - "system.md"
```

**Benefits:**
- 80% token reduction (15,000 → 3,000 tokens)
- Faster loading
- More focused context

### Greedy Loading (Deprecated)

Loads all files in namespace:

```yaml
knowledge_namespaces: ["se"]
# No knowledge_files → loads all .md files
```

---

## Schema Validation

### Output Schemas

All agent outputs are validated against Pydantic schemas in `schemas.py`.

**Example:**

```python
from pydantic import BaseModel

class ArchReviewOutput(BaseModel):
    findings: list[str]
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    implications: list[str]
    action_plan: str
```

### Validation Flow

1. Agent generates output
2. Orchestrator validates against schema
3. If valid → save to file, append to context
4. If invalid → halt execution, log error

**Benefits:**
- Guarantees structured output
- Prevents malformed responses
- Enables downstream processing

---

## Context Management

### XML Context Wrapping

Context is injected using XML tags for clear boundaries:

```xml
<system_context>
  <historical_summary>
    Previous session summary...
  </historical_summary>
  
  <recent_context>
    Recent conversation...
  </recent_context>
  
  <current_task>
    Current prompt...
  </current_task>
</system_context>
```

### Context Files

Each session maintains:
- `context.md` - Cumulative session context
- `{agent}_last.md` - Last agent output
- `state.yaml` - Session state (future)

---

## Testing

### Test Suite

```bash
# Run all tests
python3 tests/run_all_tests.py

# Run specific test
python3 tests/test_mode_registry.py
python3 tests/test_schema_validation_valid.py
```

### Test Coverage

| Test | Purpose | Status |
|------|---------|--------|
| test_schema_validation_valid.py | Valid JSON passes | ✅ PASS |
| test_schema_validation_invalid.py | Invalid JSON fails | ✅ PASS |
| test_lazy_knowledge_loading.py | Lazy loading works | ✅ PASS |
| test_xml_context_wrapping.py | XML structure correct | ✅ PASS |
| test_mode_registry.py | Registry validates | ✅ PASS |

**Total:** 5/5 tests passing (100%)

---

## Legacy Prevention

### Pre-Commit Hook

Blocks legacy file patterns:

```bash
# Blocked patterns
*_old, *_backup, *_deprecated
*.bak, *.orig, ~$
old/, backup/, deprecated/
```

**Location:** `.git/hooks/pre-commit`

### Bypass (Not Recommended)

```bash
git commit --no-verify
```

---

## Performance

### Token Efficiency

| Component | Before | After | Reduction |
|-----------|--------|-------|-----------|
| Context injection | 8,000 | 2,000 | **75%** ↓ |
| Template overhead | 500 | 300 | **40%** ↓ |
| Knowledge loading | 15,000 | 3,000 | **80%** ↓ |
| **TOTAL** | **23,500** | **5,300** | **77%** ↓ |

### Optimization Techniques

1. **Lazy Knowledge Loading** - Load only required files
2. **XML Context Wrapping** - Clear boundaries reduce overhead
3. **Schema Validation** - Prevents verbose error handling
4. **Negative Prompts** - Reduces AI slop in output

---

## Configuration

### Global Settings

Edit `config/mode_registry.yaml`:

```yaml
settings:
  timeout: 600.0              # Default timeout (seconds)
  context_threshold: 120      # Context size threshold
```

### Agent Configuration

Edit `config/agents.yaml` (future):

```yaml
agents:
  hermes:
    role: "se/m-architect"
    model: "claude-sonnet-4"
    temperature: 0.7
```

---

## API Reference

### Orchestrator

```python
from studio.developers.orchestrator import run_orchestrator

await run_orchestrator(
    task_name="my-task",
    mode="arch",
    prompt="Review this",
    agents=["hermes:se/m-architect"],
    files=["path/to/file.py"]
)
```

### Mode Registry

```python
from studio.developers.mode_registry import MODE_REGISTRY

# Validate mode
is_valid, error = MODE_REGISTRY.validate_mode("arch")

# Get mode config
config = MODE_REGISTRY.get_mode("arch")

# Get template
template = MODE_REGISTRY.get_template("arch")

# Get schema
schema = MODE_REGISTRY.get_schema("arch")

# Get knowledge files
files = MODE_REGISTRY.get_knowledge_files("arch", "se")
```

### Agent Factory

```python
from studio.developers.agents.registry import create_agent

agent = create_agent("hermes", "se/m-architect", config_dir)
```

---

## Troubleshooting

### Common Issues

**1. Mode Not Found**
```
Error: Unknown mode: mymode
Fix: Check mode_registry.yaml spelling
```

**2. Template Not Found**
```
Error: Template not found: my_template.md
Fix: Create file in config/templates/
```

**3. Schema Validation Failed**
```
Error: 1 validation error for ArchReviewOutput
Fix: Check agent output matches schema
```

**4. Knowledge Files Not Loading**
```
Error: Files not found in namespace
Fix: Verify files exist in config/roles/{namespace}/rules/
```

### Debug Mode

```bash
# Enable verbose logging
export DEBUG=1

python3 -m studio.developers.orchestrator \
  --task debug-test \
  --mode arch \
  --prompt "Test" \
  --agents hermes:se/m-architect
```

---

## Development

### Project Structure

```
studio/developers/
├── config/              # Configuration files
├── agents/              # Agent implementations
├── tests/               # Test suite
├── orchestrator.py      # Main entry point
├── mode_registry.py     # Registry system
├── schemas.py           # Output schemas
└── knowledge_index.py   # Knowledge loader
```

### Adding Features

1. **New Mode:** Edit `config/mode_registry.yaml`
2. **New Template:** Add to `config/templates/`
3. **New Schema:** Add to `schemas.py`
4. **New Agent:** Implement in `agents/`
5. **New Test:** Add to `tests/`

### Code Style

- Follow PEP 8
- Use type annotations
- Write docstrings
- Add tests for new features

---

## Resources

| Resource | Location |
|----------|----------|
| Mode Registry Guide | `MODE_REGISTRY_GUIDE.md` |
| Phase 2 Summary | `../../_out/agent-sessions/framework-refactor-meeting-v2/PHASE_2_COMPLETE.md` |
| Test Suite | `../../tests/` |
| Templates | `config/templates/` |
| Schemas | `schemas.py` |

---

## Version History

### 2.0.0 (2026-05-16) - Phase 2 Complete
- ✅ Mode registry YAML
- ✅ Orchestrator refactored
- ✅ Negative prompts enhanced
- ✅ Pre-commit hook added
- ✅ Lazy knowledge loading
- ✅ 77% token reduction

### 1.0.0 (2026-05-15) - Phase 1 Complete
- ✅ Schema validation
- ✅ XML context wrapping
- ✅ Knowledge index
- ✅ Agent registry
- ✅ Test infrastructure

---

## Support

For issues or questions:
1. Check this README
2. Review `MODE_REGISTRY_GUIDE.md`
3. Run tests: `python3 tests/run_all_tests.py`
4. Check Phase 2 documentation

---

## License

Internal project - LND Studio

---

**Maintained by:** LND Studio Development Team  
**Last Updated:** 2026-05-16  
**Status:** ✅ Production Ready
