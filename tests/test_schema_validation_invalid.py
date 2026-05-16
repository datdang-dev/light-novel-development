#!/usr/bin/env python3
"""
Test 3: Schema Validation (Invalid Output)

Tests that invalid JSON output fails schema validation and halts execution.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from studio.developers.orchestrator import _mode_single, _session_dir
from studio.developers.agents.mock_agent import MockAgent


class MockAgentInvalid(MockAgent):
    """Mock agent that returns invalid JSON (prose instead of JSON)."""

    def _arch_review_response(self, prompt: str) -> str:
        """Return prose instead of JSON to trigger validation failure."""
        return "This is just prose text, not valid JSON. The architecture looks fine to me."


class KnowledgeIndexMock:
    """Mock knowledge index for testing."""
    def get_rules(self, role: str) -> str:
        return "Mock rules content"


async def test_schema_validation_invalid():
    """Test that invalid output fails schema validation and halts."""
    print("=" * 80)
    print("Test 3: Schema Validation (Invalid Output)")
    print("=" * 80)

    # Setup
    session_dir = _session_dir("test-schema-invalid")
    session_dir.mkdir(parents=True, exist_ok=True)

    # Create context.md
    (session_dir / "context.md").write_text("# Test Context\n\nTest schema validation failure\n")

    # Create mock agent that returns invalid output
    config_dir = Path("studio/developers/config")
    mock_agent = MockAgentInvalid("hermes", "se/m-architect", config_dir)

    agent_pkg = {
        "instance": mock_agent,
        "cfg": {"id": "hermes", "role": "se/m-architect"}
    }

    knowledge = KnowledgeIndexMock()

    # Run test
    print("\n🧪 Running arch mode with invalid (prose) response...")
    await _mode_single(
        session_dir=session_dir,
        prompt="Test schema validation with invalid output",
        agent_pkg=agent_pkg,
        title="Architecture Review",
        template_name="arch_review.md",
        knowledge=knowledge,
        mode="arch"
    )

    # Check that output file was NOT created (orchestrator halted)
    output_file = session_dir / "hermes_last.md"
    context_file = session_dir / "context.md"

    if not output_file.exists():
        print("\n✅ Test PASSED")
        print("   - Orchestrator halted on validation failure")
        print("   - No output file created (expected)")
        print("   - Context not appended (expected)")

        # Verify context was not modified
        context_content = context_file.read_text()
        if "Architecture Review" not in context_content:
            print("   - Context unchanged (verified)")
            return True
        else:
            print("   ⚠️  Context was modified (unexpected)")
            return False
    else:
        print("\n❌ Test FAILED")
        print(f"   - Output file created: {output_file}")
        print("   - Expected: No file (orchestrator should halt)")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_schema_validation_invalid())
    sys.exit(0 if result else 1)
