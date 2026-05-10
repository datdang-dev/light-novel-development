#!/usr/bin/env python3
"""
LND Studio Workflow Link Validator
===================================
Scans agent YAML files, workflow.md, SKILL.md, and .agent/workflows/*.md
for broken path references, missing schemas, and orphaned files.

Usage:
    python validate_links.py                    # Full scan
    python validate_links.py --agents-only      # Only agent YAML files
    python validate_links.py --fix              # Suggest fixes for broken links
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

# ─── Resolve paths ───────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
STUDIO_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = STUDIO_ROOT.parent

# Patterns to extract file references
PATH_PATTERNS = [
    # {{project_root}}/path/to/file
    re.compile(r"\{\{project_root\}\}/([^\s\"'`}\)]+)"),
    # {project-root}/path/to/file
    re.compile(r"\{project-root\}/([^\s\"'`}\)]+)"),
    # studio/path/to/file (relative)
    re.compile(r"(?:^|\s|\"|\')((studio|_lnd-output)/[^\s\"'`}\)]+)", re.MULTILINE),
]


def extract_references(content: str) -> list[str]:
    """Extract all file path references from content."""
    refs = set()
    for pattern in PATH_PATTERNS:
        for match in pattern.finditer(content):
            path = match.group(1).strip().rstrip(".,;:)")
            # Skip template variables
            if "{{" in path or "{" in path:
                continue
            # Skip comments
            if path.startswith("#"):
                continue
            refs.add(path)
    return sorted(refs)


def resolve_path(ref: str) -> Path | None:
    """Try to resolve a reference to an actual file."""
    # Try relative to project root
    p = PROJECT_ROOT / ref
    if p.exists():
        return p

    # Try relative to studio root
    p = STUDIO_ROOT / ref
    if p.exists():
        return p

    # Try as-is (already absolute or weird path)
    p = Path(ref)
    if p.exists():
        return p

    return None


def scan_agent_files() -> list[dict]:
    """Scan all agent YAML files for broken references."""
    agents_dir = STUDIO_ROOT / "agents"
    results = []

    for yaml_file in sorted(agents_dir.glob("*.agent.yaml")):
        content = yaml_file.read_text(encoding="utf-8")
        refs = extract_references(content)

        for ref in refs:
            resolved = resolve_path(ref)
            results.append({
                "source": str(yaml_file.relative_to(PROJECT_ROOT)),
                "reference": ref,
                "exists": resolved is not None,
                "resolved": str(resolved) if resolved else None,
            })

    return results


def scan_skill_files() -> list[dict]:
    """Scan all SKILL.md files for broken references."""
    results = []

    for skill_file in sorted(STUDIO_ROOT.rglob("SKILL.md")):
        content = skill_file.read_text(encoding="utf-8")
        refs = extract_references(content)

        for ref in refs:
            resolved = resolve_path(ref)
            results.append({
                "source": str(skill_file.relative_to(PROJECT_ROOT)),
                "reference": ref,
                "exists": resolved is not None,
                "resolved": str(resolved) if resolved else None,
            })

    return results


def scan_workflow_files() -> list[dict]:
    """Scan .agent/workflows/ for broken references."""
    workflows_dir = PROJECT_ROOT / ".agent" / "workflows"
    results = []

    if not workflows_dir.exists():
        return results

    for wf_file in sorted(workflows_dir.glob("*.md")):
        content = wf_file.read_text(encoding="utf-8")
        refs = extract_references(content)

        for ref in refs:
            resolved = resolve_path(ref)
            results.append({
                "source": str(wf_file.relative_to(PROJECT_ROOT)),
                "reference": ref,
                "exists": resolved is not None,
                "resolved": str(resolved) if resolved else None,
            })

    return results


def scan_step_files() -> list[dict]:
    """Scan step files for broken references."""
    results = []

    for step_file in sorted(STUDIO_ROOT.rglob("steps/step-*.md")):
        content = step_file.read_text(encoding="utf-8")
        refs = extract_references(content)

        for ref in refs:
            resolved = resolve_path(ref)
            results.append({
                "source": str(step_file.relative_to(PROJECT_ROOT)),
                "reference": ref,
                "exists": resolved is not None,
                "resolved": str(resolved) if resolved else None,
            })

    return results


def check_schema_coverage() -> list[dict]:
    """Check that all agents referencing schemas have corresponding files."""
    schemas_dir = STUDIO_ROOT / "schemas"
    results = []

    # Find all schema references across codebase
    schema_refs = set()
    for f in STUDIO_ROOT.rglob("*.yaml"):
        content = f.read_text(encoding="utf-8")
        for match in re.finditer(r"(\w[\w-]+\.schema\.json)", content):
            schema_refs.add(match.group(1))

    for f in STUDIO_ROOT.rglob("*.md"):
        content = f.read_text(encoding="utf-8")
        for match in re.finditer(r"(\w[\w-]+\.schema\.json)", content):
            schema_refs.add(match.group(1))

    for schema_name in sorted(schema_refs):
        schema_path = schemas_dir / schema_name
        results.append({
            "schema": schema_name,
            "exists": schema_path.exists(),
            "path": str(schema_path.relative_to(PROJECT_ROOT)) if schema_path.exists() else None,
        })

    return results


def check_agent_registry_consistency() -> list[dict]:
    """Check that agent-registry.yaml matches actual agent YAML files."""
    registry_file = STUDIO_ROOT / "agents" / "agent-registry.yaml"
    results = []

    if not registry_file.exists():
        return [{"error": "agent-registry.yaml not found"}]

    with open(registry_file, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)

    # Get registered agent IDs
    registered_ids = set()
    for agent in registry.get("agents", []):
        registered_ids.add(agent["id"])

    # Get actual agent YAML files
    agents_dir = STUDIO_ROOT / "agents"
    actual_files = set()
    for f in agents_dir.glob("*.agent.yaml"):
        # Parse to get ID
        content = yaml.safe_load(f.read_text(encoding="utf-8"))
        if content and "agent" in content and "metadata" in content["agent"]:
            agent_id = content["agent"]["metadata"].get("id", "")
            # Extract short name from path-like ID
            short_id = Path(agent_id).stem.replace(".agent", "")
            actual_files.add(short_id)

    # Find mismatches
    in_registry_not_file = registered_ids - actual_files
    in_file_not_registry = actual_files - registered_ids

    for agent_id in sorted(in_registry_not_file):
        results.append({
            "agent_id": agent_id,
            "issue": "In registry but no YAML file found",
            "severity": "warning",
        })

    for agent_id in sorted(in_file_not_registry):
        results.append({
            "agent_id": agent_id,
            "issue": "Has YAML file but not in registry",
            "severity": "warning",
        })

    return results


def full_scan() -> dict:
    """Run all validation checks."""
    agents = scan_agent_files()
    skills = scan_skill_files()
    workflows = scan_workflow_files()
    steps = scan_step_files()
    schemas = check_schema_coverage()
    registry = check_agent_registry_consistency()

    all_refs = agents + skills + workflows + steps
    broken = [r for r in all_refs if not r["exists"]]
    valid = [r for r in all_refs if r["exists"]]
    missing_schemas = [s for s in schemas if not s["exists"]]

    return {
        "summary": {
            "total_references": len(all_refs),
            "valid": len(valid),
            "broken": len(broken),
            "schemas_referenced": len(schemas),
            "schemas_missing": len(missing_schemas),
            "registry_issues": len(registry),
        },
        "broken_references": broken,
        "missing_schemas": missing_schemas,
        "registry_issues": registry,
    }


def print_report(results: dict):
    """Print formatted validation report."""
    summary = results["summary"]

    print("=" * 60)
    print("  LND STUDIO — LINK VALIDATION REPORT")
    print("=" * 60)
    print()
    print(f"  Total references scanned: {summary['total_references']}")
    print(f"  ✅ Valid:                  {summary['valid']}")
    print(f"  ❌ Broken:                 {summary['broken']}")
    print(f"  📋 Schemas referenced:     {summary['schemas_referenced']}")
    print(f"  ❌ Schemas missing:         {summary['schemas_missing']}")
    print(f"  ⚠️  Registry issues:        {summary['registry_issues']}")
    print()

    if results["broken_references"]:
        print("─" * 60)
        print("  BROKEN REFERENCES")
        print("─" * 60)
        # Group by source file
        by_source: dict[str, list] = {}
        for ref in results["broken_references"]:
            by_source.setdefault(ref["source"], []).append(ref["reference"])

        for source, refs in sorted(by_source.items()):
            print(f"\n  📄 {source}")
            for ref in refs:
                print(f"     ❌ {ref}")

    if results["missing_schemas"]:
        print()
        print("─" * 60)
        print("  MISSING SCHEMAS")
        print("─" * 60)
        for schema in results["missing_schemas"]:
            print(f"  ❌ {schema['schema']}")

    if results["registry_issues"]:
        print()
        print("─" * 60)
        print("  REGISTRY INCONSISTENCIES")
        print("─" * 60)
        for issue in results["registry_issues"]:
            print(f"  ⚠️  {issue.get('agent_id', 'unknown')}: {issue.get('issue', issue.get('error', ''))}")

    print()
    if summary["broken"] == 0 and summary["schemas_missing"] == 0:
        print("  🎉 ALL CLEAR — No broken references found!")
    else:
        total_issues = summary["broken"] + summary["schemas_missing"]
        print(f"  ⚠️  {total_issues} issue(s) found. Fix before deploying pipeline.")

    print()


def main():
    parser = argparse.ArgumentParser(description="LND Studio Workflow Link Validator")
    parser.add_argument("--agents-only", action="store_true", help="Only scan agent YAML files")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.agents_only:
        refs = scan_agent_files()
        broken = [r for r in refs if not r["exists"]]
        results = {
            "summary": {"total_references": len(refs), "valid": len(refs) - len(broken), "broken": len(broken),
                        "schemas_referenced": 0, "schemas_missing": 0, "registry_issues": 0},
            "broken_references": broken,
            "missing_schemas": [],
            "registry_issues": [],
        }
    else:
        results = full_scan()

    if args.json:
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_report(results)

    sys.exit(1 if results["summary"]["broken"] > 0 or results["summary"]["schemas_missing"] > 0 else 0)


if __name__ == "__main__":
    main()
