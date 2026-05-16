#!/usr/bin/env python3
"""
Test Mode Registry

Verifies that mode_registry.yaml loads correctly and provides
expected mode configurations.
"""

import sys
from pathlib import Path

# Add studio.developers to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from studio.developers.mode_registry import ModeRegistry

def test_registry_loads():
    """Test that registry file loads without errors."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"

    try:
        registry = ModeRegistry(registry_path)
        print("✅ Registry loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to load registry: {e}")
        return False

def test_mode_exists():
    """Test that expected modes exist."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"
    registry = ModeRegistry(registry_path)

    expected_modes = ["arch", "code", "review", "cross", "qa"]
    modes = registry.list_modes()

    print(f"\nAvailable modes: {modes}")

    for mode in expected_modes:
        if mode in modes:
            print(f"✅ Mode '{mode}' exists")
        else:
            print(f"❌ Mode '{mode}' missing")
            return False

    return True

def test_mode_validation():
    """Test mode validation."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"
    registry = ModeRegistry(registry_path)

    # Test valid mode
    is_valid, error = registry.validate_mode("arch")
    if is_valid:
        print(f"\n✅ Mode 'arch' validation passed")
    else:
        print(f"\n❌ Mode 'arch' validation failed: {error}")
        return False

    # Test invalid mode
    is_valid, error = registry.validate_mode("nonexistent")
    if not is_valid:
        print(f"✅ Invalid mode correctly rejected: {error}")
    else:
        print(f"❌ Invalid mode should have been rejected")
        return False

    return True

def test_mode_config():
    """Test retrieving mode configuration."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"
    registry = ModeRegistry(registry_path)

    # Test arch mode
    mode_config = registry.get_mode("arch")

    print(f"\nArch mode config:")
    print(f"  - Template: {registry.get_template('arch')}")
    print(f"  - Schema: {registry.get_schema('arch')}")
    print(f"  - Execution type: {registry.get_execution_type('arch')}")
    print(f"  - Namespaces: {registry.get_knowledge_namespaces('arch')}")

    # Verify expected values
    if registry.get_template("arch") == "arch_review.md":
        print("✅ Template correct")
    else:
        print("❌ Template incorrect")
        return False

    if registry.get_schema("arch") == "ArchReviewOutput":
        print("✅ Schema correct")
    else:
        print("❌ Schema incorrect")
        return False

    if registry.get_execution_type("arch") == "single":
        print("✅ Execution type correct")
    else:
        print("❌ Execution type incorrect")
        return False

    return True

def test_knowledge_files():
    """Test knowledge file retrieval."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"
    registry = ModeRegistry(registry_path)

    files = registry.get_knowledge_files("arch", "se")
    print(f"\nArch mode 'se' namespace files: {files}")

    expected_files = ["global_rule_hub.md", "delegation_protocol.md", "system.md"]
    if files == expected_files:
        print("✅ Knowledge files correct")
        return True
    else:
        print(f"❌ Expected {expected_files}, got {files}")
        return False

def test_settings():
    """Test global settings retrieval."""
    registry_path = Path(__file__).parent.parent / "studio/developers/config/mode_registry.yaml"
    registry = ModeRegistry(registry_path)

    timeout = registry.get_setting("timeout")
    threshold = registry.get_setting("context_summarize_threshold")

    print(f"\nGlobal settings:")
    print(f"  - Timeout: {timeout}")
    print(f"  - Context threshold: {threshold}")

    if timeout == 600.0 and threshold == 120:
        print("✅ Settings correct")
        return True
    else:
        print("❌ Settings incorrect")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("Mode Registry Tests")
    print("=" * 80)

    tests = [
        ("Registry loads", test_registry_loads),
        ("Modes exist", test_mode_exists),
        ("Mode validation", test_mode_validation),
        ("Mode config", test_mode_config),
        ("Knowledge files", test_knowledge_files),
        ("Global settings", test_settings),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        print(f"\n{'=' * 80}")
        print(f"Test: {name}")
        print(f"{'=' * 80}")

        try:
            if test_fn():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1

    print(f"\n{'=' * 80}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 80}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
