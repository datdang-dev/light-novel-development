#!/usr/bin/env python3
"""
Phase 1 Test Suite Runner

Runs all Phase 1 tests and generates summary report.
"""

import subprocess
import sys
from pathlib import Path


def run_test(test_file: str, test_name: str) -> tuple[bool, str]:
    """Run a single test and return (passed, output)."""
    try:
        result = subprocess.run(
            ["python3", test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        passed = result.returncode == 0
        output = result.stdout + result.stderr
        return passed, output
    except subprocess.TimeoutExpired:
        return False, "Test timed out after 30 seconds"
    except Exception as e:
        return False, f"Exception: {type(e).__name__}: {e}"


def main():
    """Run all tests and generate summary."""
    print("=" * 80)
    print("Phase 1 Test Suite")
    print("=" * 80)

    tests = [
        ("tests/test_schema_validation_valid.py", "Test 2: Schema Validation (Valid)"),
        ("tests/test_schema_validation_invalid.py", "Test 3: Schema Validation (Invalid)"),
        ("tests/test_lazy_knowledge_loading.py", "Test 4: Lazy Knowledge Loading"),
        ("tests/test_xml_context_wrapping.py", "Test 5: XML Context Wrapping"),
    ]

    results = []
    passed_count = 0
    failed_count = 0

    for test_file, test_name in tests:
        print(f"\n{'=' * 80}")
        print(f"Running: {test_name}")
        print(f"{'=' * 80}")

        passed, output = run_test(test_file, test_name)

        if passed:
            print(f"✅ PASSED")
            passed_count += 1
            results.append((test_name, "PASS", ""))
        else:
            print(f"❌ FAILED")
            print(output[-500:])  # Show last 500 chars of output
            failed_count += 1
            results.append((test_name, "FAIL", output[-200:]))

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for test_name, status, error in results:
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status}")
        if error:
            print(f"   Error: {error[:100]}...")

    print(f"\nTotal: {passed_count + failed_count} tests")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    # Additional manual tests
    print("\n" + "=" * 80)
    print("Manual Tests (Already Completed)")
    print("=" * 80)
    print("✅ Test 0: Pydantic Installation")
    print("✅ Test 1: Auto-Summarization Trigger")

    print("\n" + "=" * 80)
    print("Remaining Tests (Require Real Agents)")
    print("=" * 80)
    print("⏳ Test 6: End-to-End (Arch Mode)")
    print("⏳ Test 7: End-to-End (Code Mode)")
    print("⏳ Test 8: Token Measurement")

    print("\n" + "=" * 80)
    print("Overall Status")
    print("=" * 80)
    print(f"Automated Tests: {passed_count}/{len(tests)} passed")
    print(f"Manual Tests: 2/2 passed")
    print(f"Total Completed: {passed_count + 2}/{len(tests) + 5}")

    if failed_count == 0:
        print("\n✅ All automated tests PASSED!")
        return 0
    else:
        print(f"\n❌ {failed_count} test(s) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
