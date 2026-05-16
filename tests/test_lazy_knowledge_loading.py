#!/usr/bin/env python3
"""
Test 4: Lazy Knowledge Loading

Tests that _load_knowledge() method loads only specified files.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from studio.developers.agents.registry import create_agent


def test_lazy_knowledge_loading():
    """Test lazy knowledge loading with specific files."""
    print("=" * 80)
    print("Test 4: Lazy Knowledge Loading")
    print("=" * 80)

    CONFIG_DIR = Path("studio/developers/config")

    try:
        agent = create_agent("hermes", "se/m-architect", CONFIG_DIR)
    except Exception as e:
        print(f"\n❌ Test FAILED: Could not create agent")
        print(f"   {type(e).__name__}: {e}")
        return False

    # Test 1: Load specific files
    print("\n🧪 Test 1: Loading specific files...")
    try:
        knowledge = agent._load_knowledge("se", ["global_rule_hub.md", "system.md"])
        print(f"   Loaded {len(knowledge)} chars")

        checks = [
            ("<knowledge namespace='se'" in knowledge, "Missing namespace tag"),
            ("<rule file='global_rule_hub.md'>" in knowledge, "Missing global_rule_hub.md"),
            ("<rule file='system.md'>" in knowledge, "Missing system.md"),
        ]

        for check, msg in checks:
            if not check:
                print(f"   ❌ {msg}")
                return False

        print("   ✅ Specific files loaded correctly")
    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {e}")
        return False

    # Test 2: Load all files
    print("\n🧪 Test 2: Loading all files...")
    try:
        knowledge_all = agent._load_knowledge("se")
        print(f"   Loaded {len(knowledge_all)} chars")

        if len(knowledge_all) <= len(knowledge):
            print(f"   ❌ All files should be larger than specific files")
            print(f"      Specific: {len(knowledge)} chars")
            print(f"      All: {len(knowledge_all)} chars")
            return False

        print("   ✅ All files loaded correctly")
    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {e}")
        return False

    # Test 3: Invalid namespace
    print("\n🧪 Test 3: Invalid namespace...")
    try:
        knowledge_invalid = agent._load_knowledge("invalid_namespace")

        if "Unknown namespace" not in knowledge_invalid:
            print(f"   ❌ Should warn about unknown namespace")
            print(f"      Got: {knowledge_invalid[:100]}...")
            return False

        print("   ✅ Invalid namespace handled correctly")
    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {e}")
        return False

    print("\n✅ All lazy loading tests passed!")
    return True


if __name__ == "__main__":
    result = test_lazy_knowledge_loading()
    sys.exit(0 if result else 1)
