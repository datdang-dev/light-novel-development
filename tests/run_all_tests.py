#!/usr/bin/env python3
"""
Run All Tests - Phase 1 + Phase 2
Executes all regression and validation tests.
"""

import subprocess
import sys
from pathlib import Path


def run_test(test_file: str) -> tuple[bool, str]:
    """Run a single test file and return (success, output)."""
    try:
        result = subprocess.run(
            ["python3", test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Test timed out after 30 seconds"
    except Exception as e:
        return False, f"Exception: {type(e).__name__}: {e}"


def main():
    """Run all tests and report results."""
    print("=" * 80)
    print("Running All Tests - Phase 1 + Phase 2")
    print("=" * 80)

    tests = [
        ("Test 2: Schema Validation (Valid)", "tests/test_schema_validation_valid.py"),
        ("Test 3: Schema Validation (Invalid)", "tests/test_schema_validation_invalid.py"),
        ("Test 4: Lazy Knowledge Loading", "tests/test_lazy_knowledge_loading.py"),
        ("Test 5: XML Context Wrapping", "tests/test_xml_context_wrapping.py"),
        ("Test 6: Mode Registry", "tests/test_mode_registry.py"),
    ]

    results = []

    for name, test_file in tests:
        print(f"\n{'=' * 80}")
        print(f"Running: {name}")
        print(f"{'=' * 80}")

        success, output = run_test(test_file)
        results.append((name, success))

        if success:
            print(f"✅ {name} PASSED")
        else:
            print(f"❌ {name} FAILED")
            print("\nOutput:")
            print(output)

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{len(results)} passed, {failed} failed")

    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
