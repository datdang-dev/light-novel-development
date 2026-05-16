"""
Mock Agent for Testing

Provides predefined responses for testing orchestrator without API calls.
"""

from pathlib import Path
from typing import Optional


class MockAgent:
    """Mock agent that returns predefined responses for testing."""

    def __init__(self, agent_id: str, role_name: str, config_dir: Path):
        self.agent_id = agent_id
        self.role_name = role_name
        self.config_dir = config_dir
        self.role_content = f"Mock {role_name} agent for testing"

        # Predefined responses based on role
        self.responses = {
            "se/m-architect": self._arch_review_response,
            "dev/m-prompt-expert": self._code_review_response,
        }

    async def call(self, prompt: str, session_dir: Path, timeout: float = 600.0) -> str:
        """Return predefined response based on role."""
        response_fn = self.responses.get(self.role_name, self._default_response)
        return response_fn(prompt)

    def _arch_review_response(self, prompt: str) -> str:
        """Mock architecture review response (valid JSON)."""
        return """{
  "findings": [
    "Mock finding 1: Test architecture issue",
    "Mock finding 2: Test scalability concern"
  ],
  "severity": "MEDIUM",
  "implications": [
    "Mock implication 1: Testing impact",
    "Mock implication 2: System behavior change"
  ],
  "action_plan": "Mock action plan: Fix test issues in next iteration"
}"""

    def _code_review_response(self, prompt: str) -> str:
        """Mock code review response (valid JSON)."""
        return """{
  "issues": [
    {
      "line": 42,
      "severity": "HIGH",
      "category": "slop",
      "description": "Mock issue: Generic phrase detected",
      "suggested_rewrite": "Mock rewrite suggestion"
    }
  ],
  "overall_score": 85,
  "verdict": "PASS",
  "summary": "Mock summary: Code quality is acceptable for testing"
}"""

    def _default_response(self, prompt: str) -> str:
        """Default mock response."""
        return "Mock agent response for testing purposes"

    def _load_knowledge(self, namespace: str, specific_files: Optional[list[str]] = None) -> str:
        """Mock knowledge loading."""
        return f"<knowledge namespace='{namespace}'><rule file='mock.md'>Mock knowledge content</rule></knowledge>"
