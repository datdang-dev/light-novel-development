#!/usr/bin/env python3
"""
Test 2: Schema Validation (Valid Output)

Tests that valid JSON output passes schema validation.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from studio.developers.orchestrator import _mode_single, _session_dir, TEMPLATES_DIR
from studio.developers.agents.mock_agent import MockAgent
from studio.developers.agents.base import BaseAgent


class KnowledgeIndexMock:
    """Mock knowledge index for testing."""
    def get_rules(self, role: str) -> str:
        return "Mock rules content"


async def test_schema_validation_valid():
    """Test that valid JSON passes schema validation."""
    print("=" * 80)
    print("Test 2: Schema Validation (Valid Output)")
    print("=" * 80)

    # Setup
    session_dir = _session_dir("test-schema-valid")
    session_dir.mkdir(parents=True, exist_ok=True)

    # Create context.md
    (session_dir / "context.md").write_text("# Test Context\n\nTest schema validation\n")

    # Create mock agent
    config_dir = Path("studio/developers/config")
    mock_agent = MockAgent("hermes", "se/m-architect", config_dir)

    agent_pkg = {
        "instance": mock_agent,
        "cfg": {"id": "hermes", "role": "se/m-architect"}
    }

    knowledge = KnowledgeIndexMock()

    # Run test
    print("\n🧪 Running arch mode with valid JSON response...")
    try:
        await _mode_single(
            session_dir=session_dir,
            prompt="Test schema validation with valid output",
            agent_pkg=agent_pkg,
            title="Architecture Review",
            template_name="arch_review.md",
            knowledge=knowledge,
            mode="arch"
        )

        # Check results
        output_file = session_dir / "hermes_last.md"
        if output_file.exists():
            output = output_file.read_text()
            print("\n✅ Test PASSED")
            print(f"   - Output file created: {output_file}")
            print(f"   - Output size: {len(output)} bytes")
            print(f"   - Schema validation passed (no exception raised)")
            return True
        else:
            print("\n❌ Test FAILED")
            print(f"   - Output file not created: {output_file}")
            return False

    except Exception as e:
        print(f"\n❌ Test FAILED with exception:")
        print(f"   {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_schema_validation_valid())
    sys.exit(0 if result else 1)
