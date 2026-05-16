import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .pipeline_manager import PipelineManager

class ProductionRunner:
    """
    Production-grade runner for LND Studio pipelines.
    Designed to be used by the LND Orchestrator (Director K) 
    to maintain the 'Chain of Truth' across multi-agent steps.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.mgr = PipelineManager(project_root / "studio/core/orchestration/pipeline_registry.yaml")
        self.session_dir: Optional[Path] = None

    def start_session(self, task_id: str):
        self.session_dir = self.project_root / "_out" / "production-sessions" / task_id
        self.session_dir.mkdir(parents=True, exist_ok=True)
        return self.session_dir

    def get_step_context(self, pipeline_id: str, step_index: int) -> Dict[str, Any]:
        """Loads the role, template, and schema for the current step."""
        step = self.mgr.get_step(pipeline_id, step_index)
        if not step:
            raise ValueError(f"Step {step_index} not found in pipeline {pipeline_id}")
            
        # Resolve absolute paths
        template_path = self.project_root / step["template"]
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        return {
            "step_id": step["id"],
            "agent": step["agent"],
            "template": template_content,
            "output_schema": step["output_schema"],
            "knowledge": step.get("knowledge", [])
        }

    def save_step_output(self, step_id: str, output_data: Dict[str, Any]):
        """Saves the structured output of a step to the session directory."""
        if not self.session_dir:
            raise RuntimeError("Session not started.")
            
        output_file = self.session_dir / f"{step_id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        return output_file
