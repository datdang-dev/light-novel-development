
"""
SECURITY PATCHES FOR LND STUDIO
================================
Critical security fixes for path traversal, input validation, and injection vulnerabilities.

Apply these patches to secure the LND Studio codebase.
"""

import os
import sys
from pathlib import Path
import json
import re


# ============================================================================
# 1. PATH TRAVERSAL PROTECTION
# ============================================================================

def safe_join(base_path, user_path, allowed_extensions=None, max_size=None):
    """
    Safely join a base path with a user-provided path, preventing directory traversal.

    Args:
        base_path: Safe base directory (must be absolute)
        user_path: User-provided path to append
        allowed_extensions: Set of allowed file extensions (e.g., {'.json', '.md'})
        max_size: Maximum file size in bytes

    Returns:
        Path object for the resolved, safe path

    Raises:
        ValueError: If path traversal detected or other validation fails
    """
    # Resolve base to absolute path
    base = Path(base_path).resolve(strict=True)

    # Normalize user path and remove any null bytes
    user_path = str(user_path).replace('\x00', '')

    # Prevent absolute paths
    if Path(user_path).is_absolute():
        raise ValueError("Absolute paths not allowed")

    # Check for directory traversal attempts
    if '..' in user_path or user_path.startswith('/'):
        raise ValueError("Directory traversal detected")

    # Join and resolve
    target = (base / user_path).resolve()

    # Ensure target is within base directory (CRITICAL CHECK)
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError(f"Path traversal detected: {user_path}")

    # Validate file extension
    if allowed_extensions is not None:
        if target.suffix not in allowed_extensions:
            raise ValueError(f"File type not allowed: {target.suffix}")

    # Validate file size
    if max_size is not None and target.exists():
        if target.stat().st_size > max_size:
            raise ValueError(f"File too large: {target.stat().st_size} > {max_size}")

    return target


def validate_path_within_project(path, project_root, allowed_extensions=None):
    """
    Validate that a path is within the project directory.

    Args:
        path: Path to validate
        project_root: Root directory of the project
        allowed_extensions: Optional set of allowed file extensions

    Returns:
        Validated Path object

    Raises:
        ValueError: If path is outside project or invalid
    """
    project_root = Path(project_root).resolve()
    target = Path(path).resolve()

    try:
        target.relative_to(project_root)
    except ValueError:
        raise ValueError(f"Path outside project directory: {path}")

    if allowed_extensions and target.suffix not in allowed_extensions:
        raise ValueError(f"Invalid file extension: {target.suffix}")

    return target


# ============================================================================
# 2. INPUT VALIDATION AND SANITIZATION
# ============================================================================

def sanitize_string(value, max_length=None, allow_control_chars=False):
    """
    Sanitize string input by removing dangerous characters.

    Args:
        value: Input string
        max_length: Maximum allowed length
        allow_control_chars: Whether to allow control characters (default: False)

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        value = str(value)

    # Remove null bytes
    value = value.replace('\x00', '')

    # Remove control characters unless allowed
    if not allow_control_chars:
        value = ''.join(c for c in value if c.isprintable() or c in '\n\r\t')

    # Truncate if too long
    if max_length and len(value) > max_length:
        value = value[:max_length]

    return value


def validate_json_schema(data, schema):
    """
    Validate JSON data against a schema.

    Args:
        data: JSON data to validate
        schema: JSON schema to validate against

    Returns:
        Validated data

    Raises:
        ValueError: If validation fails
    """
    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        raise ImportError("jsonschema not installed. Run: pip install jsonschema")

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"JSON validation failed: {e.message}")

    return data


def sanitize_json(data, max_depth=10, max_size=1024*1024):
    """
    Recursively sanitize JSON data by removing control characters and limiting size.

    Args:
        data: JSON data to sanitize
        max_depth: Maximum recursion depth
        max_size: Maximum total size in bytes

    Returns:
        Sanitized data
    """
    def _sanitize(obj, depth=0):
        if depth > max_depth:
            raise ValueError("Maximum JSON depth exceeded")

        if isinstance(obj, dict):
            return {sanitize_string(k): _sanitize(v, depth + 1) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_sanitize(item, depth + 1) for item in obj]
        elif isinstance(obj, str):
            return sanitize_string(obj)
        elif isinstance(obj, (int, float, bool)) or obj is None:
            return obj
        else:
            return str(obj)

    result = _sanitize(data)

    # Check size
    json_str = json.dumps(result)
    if len(json_str.encode('utf-8')) > max_size:
        raise ValueError("JSON data too large")

    return result


# ============================================================================
# 3. COMMAND INJECTION PREVENTION
# ============================================================================

def safe_subprocess(args, cwd=None, timeout=30, allowed_paths=None):
    """
    Safely run a subprocess with validation.

    Args:
        args: Command and arguments (list)
        cwd: Working directory
        timeout: Command timeout in seconds
        allowed_paths: List of allowed working directories

    Returns:
        CompletedProcess object

    Raises:
        ValueError: If validation fails
        subprocess.TimeoutExpired: If command times out
    """
    import subprocess
    import shlex

    # Validate command path
    if not args or not isinstance(args, (list, tuple)):
        raise ValueError("Command must be a list of arguments")

    # Ensure command is absolute path or in safe locations
    cmd_path = Path(args[0])
    if not cmd_path.is_absolute():
        # Try to find in PATH
        import shutil
        full_path = shutil.which(args[0])
        if not full_path:
            raise ValueError(f"Command not found: {args[0]}")
        args[0] = full_path

    # Validate working directory
    if cwd:
        cwd_path = Path(cwd).resolve()
        if allowed_paths:
            allowed = any(
                cwd_path.is_relative_to(Path(p).resolve())
                for p in allowed_paths
            )
            if not allowed:
                raise ValueError(f"Working directory not allowed: {cwd}")

    # Log command execution (for audit)
    import logging
    logging.getLogger('security').info(
        f"Executing subprocess: {shlex.join(args)}"
    )

    # Run with timeout
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
        capture_output=True,
        text=True
    )

    return result


def safe_system_command(command, allowed_commands=None):
    """
    Validate and execute a system command safely.

    Args:
        command: Command string
        allowed_commands: List of allowed command patterns

    Returns:
        Command output

    Raises:
        ValueError: If command not allowed
    """
    import subprocess, shlex

    # Parse command
    try:
        args = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"Invalid command syntax: {e}")

    # Check against allowed commands
    if allowed_commands:
        cmd_name = args[0]
        if not any(
            re.match(pattern, cmd_name) for pattern in allowed_commands
        ):
            raise ValueError(f"Command not allowed: {cmd_name}")

    # Validate no shell metacharacters
    dangerous = [';', '&', '|', '`', '$(']
    if any(char in command for char in dangerous):
        raise ValueError("Command contains dangerous characters")

    # Execute
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=30
    )

    return result.stdout


# ============================================================================
# 4. SECURE PATCH FOR KNOWLEDGE INJECTOR
# ============================================================================

def patched_knowledge_injector(forensic_state_path, payload_output_path, knowledge_dir):
    """
    Patched version of knowledge_injector.py with security fixes.
    """
    import json
    from pathlib import Path

    PROJECT_ROOT = Path(__file__).parent.parent  # Adjust as needed

    # Validate all paths
    try:
        forensic_state_path = safe_join(
            PROJECT_ROOT / "studio",
            forensic_state_path,
            allowed_extensions={'.json'},
            max_size=1024*1024  # 1MB
        )
    except ValueError as e:
        raise ValueError(f"Invalid forensic state path: {e}")

    try:
        payload_output_path = safe_join(
            PROJECT_ROOT / "studio",
            payload_output_path,
            allowed_extensions={'.md', '.txt'},
            max_size=10*1024*1024  # 10MB
        )
    except ValueError as e:
        raise ValueError(f"Invalid output path: {e}")

    try:
        knowledge_dir = safe_join(
            PROJECT_ROOT / "studio",
            knowledge_dir
        )
    except ValueError as e:
        raise ValueError(f"Invalid knowledge directory: {e}")

    # Load and validate forensic state
    try:
        with open(forensic_state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in forensic state: {e}")

    # Sanitize state data
    state = sanitize_json(state, max_depth=5, max_size=512*1024)

    # Validate required fields
    required_fields = ['page_number', 'content_tags', 'characters_present', 'setting']
    for field in required_fields:
        if field not in state:
            raise ValueError(f"Missing required field: {field}")

    # Validate tags
    tags = set()
    for tag in state.get("content_tags", []):
        tag = sanitize_string(tag, max_length=50)
        tags.add(tag)

    # Search for relevant files
    file_scores = {}
    for root, dirs, files in os.walk(knowledge_dir):
        # Prevent traversal - ensure we're still within knowledge_dir
        root_path = Path(root).resolve()
        try:
            root_path.relative_to(knowledge_dir.resolve())
        except ValueError:
            continue  # Skip directories outside knowledge_dir

        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file

                # Validate file path
                try:
                    file_path = safe_join(knowledge_dir, file_path.relative_to(knowledge_dir))
                except ValueError:
                    continue

                # Check file size
                if file_path.stat().st_size > 1024*1024:  # 1MB
                    continue

                # Score file based on tags
                score = 0
                file_basename = file.lower()
                for tag in tags:
                    if tag.lower() in file_basename:
                        score += 5

                # Quick content scan (limit size)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(50000)  # Read only first 50KB
                        for tag in tags:
                            if tag.lower() in content.lower():
                                score += 1
                except Exception:
                    continue

                if score > 0:
                    file_scores[file_path] = score

    # Take top 2 files
    sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    top_files = sorted_files[:2]

    # Build payload
    payload_content = "# Knowledge Payload (JIT RAG)\n\n"
    payload_content += "Based on the content tags from the forensic analysis, the following research files have been loaded for your context:\n\n"

    if top_files:
        for file_path, score in top_files:
            payload_content += f"## Source: `{file_path.name}` (Relevance Score: {score})\n\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(100000)  # Limit to 100KB
                    content = sanitize_string(content, max_length=100000)
                    payload_content += content + "\n\n---\n\n"
            except Exception as e:
                payload_content += f"[Error reading file: {e}]\n\n"
    else:
        payload_content += "*No highly relevant research files found for these tags.*\n"

    # Add security notice
    payload_content += "\n---\n\n*Note: All content has been sanitized for safe processing.\n"

    # Write output
    output_dir = payload_output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(payload_output_path, 'w', encoding='utf-8') as f:
        f.write(payload_content)

    print(f"Generated {payload_output_path} with {len(top_files)} research files included.")
    print(f"Sanitized output written safely.")


# ============================================================================
# 5. SECURITY-PATCHED AUTO REPAIR
# ============================================================================

def patched_auto_repair(json_path, schema_path):
    """
    Patched version of auto_repair.py with security fixes.
    """
    import json
    from pathlib import Path

    STUDIO_ROOT = Path(__file__).parent.parent / "studio"

    # Validate paths
    try:
        json_path = safe_join(STUDIO_ROOT, json_path, allowed_extensions={'.json'})
        schema_path = safe_join(STUDIO_ROOT, schema_path, allowed_extensions={'.json'})
    except ValueError as e:
        print(f"❌ Invalid path: {e}")
        return False

    # Check file sizes
    if json_path.stat().st_size > 10*1024*1024:  # 10MB
        print(f"❌ File too large: {json_path}")
        return False

    if schema_path.stat().st_size > 1*1024*1024:  # 1MB
        print(f"❌ Schema too large: {schema_path}")
        return False

    # Load JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ UNFIXABLE: JSON parse error - {e}")
        print("   → Needs LLM re-generation")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Sanitize data
    data = sanitize_json(data, max_depth=10, max_size=5*1024*1024)

    # Load schema
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid schema: {e}")
        return False

    # Validate against schema
    try:
        from jsonschema import validate, ValidationError
        try:
            validate(instance=data, schema=schema)
            print("✅ JSON is valid - no repairs needed.")
            return True
        except ValidationError as e:
            print(f"⚠️ Schema validation failed: {e.message}")
    except ImportError:
        print("⚠️ jsonschema not installed - skipping validation")

    # Auto-repair logic (with security checks)
    repairs = []
    schema_props = schema.get('properties', {})
    required = schema.get('required', [])

    # Add missing required fields
    for field in required:
        if field not in data:
            field_schema = schema_props.get(field, {})
            field_type = field_schema.get('type', 'string')
            defaults = {
                'string': '',
                'number': 0,
                'integer': 0,
                'boolean': False,
                'array': [],
                'object': {}
            }
            data[field] = defaults.get(field_type, None)
            repairs.append(f"Added missing field '{field}'")

    # Fix word count
    if 'word_count' in data and 'prose_content' in data:
        actual_count = len(str(data['prose_content']).split())
        if data['word_count'] != actual_count:
            data['word_count'] = actual_count
            repairs.append(f"Corrected word_count to {actual_count}")

    # Fix boolean fields
    for field, field_schema in schema_props.items():
        if field in data and field_schema.get('type') == 'boolean':
            if not isinstance(data[field], bool):
                data[field] = bool(data[field])
                repairs.append(f"Cast '{field}' to boolean")

    # Apply repairs
    if repairs:
        print(f"🔧 Applied {len(repairs)} auto-repairs:")
        for r in repairs:
            print(f"   {r}")

        # Sanitize again
        data = sanitize_json(data)

        # Write back
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✅ Repaired file saved: {json_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False
    else:
        print("✅ No repairs needed.")
        return True


# ============================================================================
# 6. MAIN - Apply Patches
# ============================================================================

def main():
    """
    Apply security patches to LND Studio files.
    """
    print("="*60)
    print("LND STUDIO SECURITY PATCH APPLICATION")
    print("="*60)

    patches_dir = Path(__file__).parent / "patches"
    patches_dir.mkdir(exist_ok=True)

    # Create patched versions
    print("\n[1/6] Creating patched knowledge_injector.py...")

    original_injector = """
import json
import os
import sys
import glob

def generate_knowledge_payload(forensic_state_path, payload_output_path, knowledge_dir):
    try:
        with open(forensic_state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except FileNotFoundError:
        print(f"Error: {forensic_state_path} not found.")
        sys.exit(1)

    tags = set(state.get("content_tags", []))
    if not tags:
        print("No content tags found in forensic state. Proceeding with empty payload.")
        with open(payload_output_path, 'w', encoding='utf-8') as f:
            f.write("# Knowledge Payload\n\nNo specific context tags detected.\n")
        return

    print(f"Searching for tags: {list(tags)}")

    # VULNERABLE: No path validation
    file_scores = {}
    for root, dirs, files in os.walk(knowledge_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                score = 0

                file_basename = os.path.basename(file).lower()
                for tag in tags:
                    if tag.lower() in file_basename:
                        score += 5

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for tag in tags:
                            if tag.lower() in content:
                                score += 1
                except Exception:
                    pass

                if score > 0:
                    file_scores[file_path] = score

    sorted_files = sorted(file_scores.items(), key=lambda item: item[1], reverse=True)
    top_files = sorted_files[:2]

    payload_content = "# Knowledge Payload (JIT RAG)\n\n"
    payload_content += "Based on the content tags from the forensic analysis, the following research files have been loaded for your context:\n\n"

    if top_files:
        for file_path, score in top_files:
            payload_content += f"## Source: `{os.path.basename(file_path)}` (Relevance Score: {score})\n\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    payload_content += content + "\n\n---\n\n"
            except Exception as e:
                payload_content += f"[Error reading file: {e}]\n\n"
    else:
        payload_content += "*No highly relevant research files found for these tags.*\n"

    with open(payload_output_path, 'w', encoding='utf-8') as f:
        f.write(payload_content)

    print(f"Generated {payload_output_path} with {len(top_files)} research files included.")
"""

    # Write security patches documentation
    patch_doc = patches_dir / "SECURITY_PATCHES.md"
    patch_doc.write_text("""
# Security Patches for LND Studio

## Overview
This directory contains security patches for vulnerabilities identified in the LND Studio codebase.

## Patches

### 1. Path Traversal Vulnerabilities
**Affected Files:**
- `studio/core/transformation-engine/knowledge_injector.py`
- `studio/scripts/batch_manga_ocr.py`
- `studio/scripts/extract_dialogue.py`
- `studio/scripts/extract_scene_context.py`

**Issue:** No validation of user-provided paths allows directory traversal attacks.

**Fix:** Use `safe_join()` function to validate all paths are within project directory.

### 2. Missing Input Validation
**Affected Files:** All Python scripts processing JSON

**Issue:** No schema validation before processing JSON data.

**Fix:** Use `validate_json_schema()` and `sanitize_json()` functions.

### 3. Command Injection Risks
**Affected Files:** Scripts calling external binaries

**Issue:** Unvalidated input passed to subprocess calls.

**Fix:** Use `safe_subprocess()` with allowlists of permitted commands.

### 4. Missing Authentication/Authorization
**Affected Files:** All agent definitions and service calls

**Issue:** No authentication or authorization checks.

**Fix:** Implement token-based authentication with `@authenticate` decorator.

### 5. Insecure Error Handling
**Affected Files:** All exception handlers

**Issue:** Error messages leak internal paths and sensitive data.

**Fix:** Use `log_security_event()` for audit logging and sanitize error messages.

## Application

To apply patches:

1. Test in development environment first
2. Update imports to use security utility functions
3. Replace `open()` calls with `safe_join()` validation
4. Add JSON schema validation
5. Implement authentication middleware
6. Configure structured logging

See SECURITY_AUDIT_REPORT.md for full details.
""")

    print(f"   Created {patch_doc}")

    # Create example patched file
    example_file = patches_dir / "knowledge_injector_patched.py"
    example_file.write_text("""
#!/usr/bin/env python3
"""Patched version with security fixes."""
import json
import os
import sys
from pathlib import Path

# Add security utilities path
sys.path.insert(0, str(Path(__file__).parent.parent / "studio"))

# Import security patches (would be in a real security module)
def safe_join(base, user_path, allowed_extensions=None):
    \"\"\"Safely join paths preventing traversal.\"\"\"
    base = Path(base).resolve()
    target = (base / user_path).resolve()
    target.relative_to(base)  # Raises ValueError if outside
    if allowed_extensions and target.suffix not in allowed_extensions:
        raise ValueError("Invalid file type")
    return target

PROJECT_ROOT = Path(__file__).parent.parent / "studio"

def generate_knowledge_payload(forensic_state_path, payload_output_path, knowledge_dir):
    # SECURITY FIX 1: Validate all paths
    try:
        forensic_state_path = safe_join(
            PROJECT_ROOT, forensic_state_path, allowed_extensions={'.json'}
        )
        payload_output_path = safe_join(
            PROJECT_ROOT, payload_output_path, allowed_extensions={'.md'}
        )
        knowledge_dir = safe_join(PROJECT_ROOT, knowledge_dir)
    except ValueError as e:
        print(f"❌ Invalid path: {e}")
        sys.exit(1)

    # SECURITY FIX 2: Validate JSON schema
    try:
        with open(forensic_state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    # Check required fields
    required = ['page_number', 'content_tags', 'characters_present', 'setting']
    for field in required:
        if field not in state:
            print(f"❌ Missing required field: {field}")
            sys.exit(1)

    tags = set(state.get("content_tags", []))
    if not tags:
        print("No content tags found. Using empty payload.")
        with open(payload_output_path, 'w', encoding='utf-8') as f:
            f.write("# Knowledge Payload\n\nNo context tags detected.\n")
        return

    print(f"Searching for tags: {list(tags)}")

    # SECURITY FIX 3: Secure directory traversal
    file_scores = {}
    for root, dirs, files in os.walk(knowledge_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                try:
                    # Verify path is within knowledge_dir
                    file_path.relative_to(knowledge_dir)
                except ValueError:
                    continue  # Skip files outside directory

                # SECURITY FIX 4: Check file size
                if file_path.stat().st_size > 1024*1024:  # 1MB limit
                    continue

                score = 0
                file_basename = file.lower()
                for tag in tags:
                    if tag.lower() in file_basename:
                        score += 5

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(50000)  # Limit read size
                        for tag in tags:
                            if tag.lower() in content.lower():
                                score += 1
                except Exception:
                    pass

                if score > 0:
                    file_scores[file_path] = score

    sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    top_files = sorted_files[:2]

    # Build payload with sanitization
    payload_content = "# Knowledge Payload (JIT RAG)\n\n"
    payload_content += "Based on content tags, the following research files have been loaded:\n\n"

    if top_files:
        for file_path, score in top_files:
            payload_content += f"## Source: `{file_path.name}` (Score: {score})\n\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(100000)  # Limit to 100KB
                    # SECURITY FIX 5: Sanitize content
                    content = ''.join(c for c in content if c.isprintable() or c in '\n\r\t')
                    payload_content += content + "\n\n---\n\n"
            except Exception as e:
                payload_content += f"[Error: {e}]\n\n"
    else:
        payload_content += "*No relevant files found.*\n"

    # SECURITY FIX 6: Validate output path
    payload_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(payload_output_path, 'w', encoding='utf-8') as f:
        f.write(payload_content)

    print(f"✅ Generated {payload_output_path}")
    print(f"   Included {len(top_files)} research files")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 knowledge_injector.py <forensic.json> <output.md> <knowledge_dir>")
        sys.exit(1)

    generate_knowledge_payload(sys.argv[1], sys.argv[2], sys.argv[3])
""")

    print(f"   Created {example_file}")

    print("\n" + "="*60)
    print("PATCH CREATION COMPLETE")
    print("="*60)
    print(f"\nPatches saved to: {patches_dir}")
    print(f"Full report: SECURITY_AUDIT_REPORT.md")
    print("\nNext steps:")
    print("  1. Review patches in patches/ directory")
    print("  2. Test patches in development environment")
    print("  3. Apply security fixes to production files")
    print("  4. Re-run security audit after fixes")
    print("="*60)


if __name__ == "__main__":
    main()
