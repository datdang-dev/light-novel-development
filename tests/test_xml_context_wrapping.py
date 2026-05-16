#!/usr/bin/env python3
"""
Test 5: XML Context Wrapping

Tests that context is wrapped in XML tags for attention anchoring.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from studio.developers.orchestrator import _inject_context, _session_dir


async def test_xml_context_wrapping():
    """Test that context is wrapped in XML tags."""
    print("=" * 80)
    print("Test 5: XML Context Wrapping")
    print("=" * 80)

    # Setup test session
    session_dir = _session_dir("test-xml-wrapping")
    session_dir.mkdir(parents=True, exist_ok=True)

    # Create context.md with some content
    context_file = session_dir / "context.md"
    context_file.write_text("""# Context

## Turn 1
Agent A reviewed the code.

## Turn 2
Agent B suggested improvements.
""")

    # Test 1: Basic XML wrapping
    print("\n🧪 Test 1: Basic XML wrapping (no summary)...")
    try:
        injected = await _inject_context(session_dir, "Test prompt for XML wrapping")

        checks = [
            ("<system_context>" in injected, "Missing <system_context> opening tag"),
            ("</system_context>" in injected, "Missing </system_context> closing tag"),
            ("<current_task>" in injected, "Missing <current_task> tag"),
            ("Test prompt for XML wrapping" in injected, "Missing prompt in current_task"),
            ("<recent_context>" in injected, "Missing <recent_context> tag"),
        ]

        all_passed = True
        for check, msg in checks:
            if check:
                print(f"   ✅ {msg.replace('Missing', 'Found')}")
            else:
                print(f"   ❌ {msg}")
                all_passed = False

        if not all_passed:
            print(f"\n   Raw output:\n{injected[:500]}...")
            return False

    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {e}")
        return False

    # Test 2: With summary file
    print("\n🧪 Test 2: XML wrapping with summary...")
    summary_file = session_dir / "context_summary.md"
    summary_file.write_text("# Summary\n\nKey decisions made in previous turns.")

    try:
        injected = await _inject_context(session_dir, "Test with summary")

        checks = [
            ("<historical_summary>" in injected, "Missing <historical_summary> tag"),
            ("Key decisions made" in injected, "Missing summary content"),
        ]

        all_passed = True
        for check, msg in checks:
            if check:
                print(f"   ✅ {msg.replace('Missing', 'Found')}")
            else:
                print(f"   ❌ {msg}")
                all_passed = False

        if not all_passed:
            print(f"\n   Raw output:\n{injected[:500]}...")
            return False

    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {e}")
        return False

    # Test 3: Verify structure
    print("\n🧪 Test 3: Verify XML structure order...")
    lines = injected.split('\n')

    # Find tag positions
    tags = {
        'system_context_open': None,
        'historical_summary': None,
        'recent_context': None,
        'current_task': None,
        'system_context_close': None,
    }

    for i, line in enumerate(lines):
        if '<system_context>' in line:
            tags['system_context_open'] = i
        elif '<historical_summary>' in line:
            tags['historical_summary'] = i
        elif '<recent_context>' in line:
            tags['recent_context'] = i
        elif '<current_task>' in line:
            tags['current_task'] = i
        elif '</system_context>' in line:
            tags['system_context_close'] = i

    # Verify order
    if tags['system_context_open'] is not None and tags['system_context_close'] is not None:
        if tags['system_context_open'] < tags['system_context_close']:
            print("   ✅ system_context tags properly nested")
        else:
            print("   ❌ system_context tags out of order")
            return False

        if tags['historical_summary'] and tags['recent_context'] and tags['current_task']:
            if tags['historical_summary'] < tags['recent_context'] < tags['current_task']:
                print("   ✅ Tags in correct order: historical → recent → current")
            else:
                print("   ❌ Tags out of order")
                return False
    else:
        print("   ❌ Missing system_context tags")
        return False

    print("\n✅ All XML wrapping tests passed!")
    return True


if __name__ == "__main__":
    result = asyncio.run(test_xml_context_wrapping())
    sys.exit(0 if result else 1)
