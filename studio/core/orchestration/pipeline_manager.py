import yaml
from pathlib import Path
from typing import Dict, Any, List

class PipelineManager:
    """
    Manages production pipelines for LND Studio.
    Provides structured context and schema enforcement for content generation.
    """
    
    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        with open(self.registry_path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        self.pipelines = self.data.get("pipelines", {})

    def get_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        return self.pipelines.get(pipeline_id)

    def get_step(self, pipeline_id: str, step_index: int) -> Dict[str, Any]:
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            return None
        steps = pipeline.get("steps", [])
        if 0 <= step_index < len(steps):
            return steps[step_index]
        return None

    def get_total_steps(self, pipeline_id: str) -> int:
        pipeline = self.get_pipeline(pipeline_id)
        return len(pipeline.get("steps", [])) if pipeline else 0
