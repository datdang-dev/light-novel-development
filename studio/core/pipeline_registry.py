import yaml
from pathlib import Path

class PipelineRegistry:
    """Registry to dynamically load and manage pipeline definitions from YAML manifests."""
    
    def __init__(self, manifests_dir: Path):
        self.manifests_dir = Path(manifests_dir)
        self._pipelines = {}
        self.reload()

    def reload(self):
        """Scan manifest directory and load pipelines."""
        self._pipelines.clear()
        if not self.manifests_dir.exists():
            return
        
        for yaml_file in self.manifests_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data and "name" in data:
                        self._pipelines[data["name"]] = data
            except Exception as e:
                print(f"⚠️ Warning: Failed to load pipeline manifest {yaml_file.name}: {e}")

    def get(self, name: str) -> dict | None:
        """Get pipeline definition by name."""
        return self._pipelines.get(name)

    def list_pipelines(self) -> dict[str, dict]:
        """Return all registered pipelines."""
        return self._pipelines
