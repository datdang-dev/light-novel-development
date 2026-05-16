"""
Mode Registry Loader

Loads mode configurations from mode_registry.yaml and provides
a clean interface for the orchestrator.

Phase 2 Implementation (2026-05-16)
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ModeRegistry:
    """Registry for orchestrator modes loaded from YAML."""

    def __init__(self, registry_path: Path):
        """Load mode registry from YAML file."""
        self.registry_path = registry_path
        self._config = self._load_registry()
        self.modes = self._config.get("modes", {})
        self.schema_map = self._config.get("schema_map", {})
        self.execution_types = self._config.get("execution_types", {})
        self.settings = self._config.get("settings", {})

    def _load_registry(self) -> Dict[str, Any]:
        """Load and parse YAML registry file."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Mode registry not found: {self.registry_path}")

        with open(self.registry_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_mode(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """Get mode configuration by name."""
        return self.modes.get(mode_name)

    def get_template(self, mode_name: str) -> Optional[str]:
        """Get template filename for a mode."""
        mode = self.get_mode(mode_name)
        return mode.get("template") if mode else None

    def get_schema(self, mode_name: str) -> Optional[str]:
        """Get output schema class name for a mode."""
        mode = self.get_mode(mode_name)
        return mode.get("output_schema") if mode else None

    def get_knowledge_namespaces(self, mode_name: str) -> list[str]:
        """Get knowledge namespaces for a mode."""
        mode = self.get_mode(mode_name)
        return mode.get("knowledge_namespaces", []) if mode else []

    def get_knowledge_files(self, mode_name: str, namespace: str) -> list[str]:
        """Get specific knowledge files for a mode and namespace."""
        mode = self.get_mode(mode_name)
        if not mode:
            return []

        knowledge_files = mode.get("knowledge_files", {})
        return knowledge_files.get(namespace, [])

    def get_execution_type(self, mode_name: str) -> Optional[str]:
        """Get execution type for a mode."""
        mode = self.get_mode(mode_name)
        return mode.get("execution_type") if mode else None

    def get_handler(self, mode_name: str) -> Optional[str]:
        """Get handler function name for a mode's execution type."""
        execution_type = self.get_execution_type(mode_name)
        if not execution_type:
            return None

        exec_config = self.execution_types.get(execution_type)
        return exec_config.get("handler") if exec_config else None

    def validate_mode(self, mode_name: str) -> tuple[bool, Optional[str]]:
        """
        Validate that a mode exists and has required fields.

        Returns:
            (is_valid, error_message)
        """
        mode = self.get_mode(mode_name)
        if not mode:
            return False, f"Unknown mode: {mode_name}"

        # Check required fields
        if "execution_type" not in mode:
            return False, f"Mode '{mode_name}' missing 'execution_type'"

        execution_type = mode["execution_type"]
        if execution_type not in self.execution_types:
            return False, f"Unknown execution type: {execution_type}"

        # Validate based on execution type
        if execution_type == "single":
            if "template" not in mode:
                return False, f"Single mode '{mode_name}' missing 'template'"

        elif execution_type == "sequential":
            if "steps" not in mode:
                return False, f"Sequential mode '{mode_name}' missing 'steps'"

        elif execution_type == "debate":
            if "passes" not in mode:
                return False, f"Debate mode '{mode_name}' missing 'passes'"

        return True, None

    def list_modes(self) -> list[str]:
        """List all available mode names."""
        return list(self.modes.keys())

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a global setting value."""
        return self.settings.get(key, default)
