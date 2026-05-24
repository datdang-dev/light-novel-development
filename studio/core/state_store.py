import fcntl
import yaml
from pathlib import Path
from datetime import datetime, timezone

class StateStore:
    """Unified State Store for LND Studio pipelines.
    
    Ensures safe concurrent read/write access to the state ledger
    via file-based flock Mutex locking.
    """
    def __init__(self, state_file: Path):
        self.state_file = Path(state_file)
        self.lock_file_path = self.state_file.parent / (self.state_file.name + ".lock")

    def load(self) -> dict | None:
        """Load the state dict from YAML with shared flock lock."""
        if not self.state_file.exists():
            return None
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.lock_file_path, "w") as lock_file:
            try:
                fcntl.flock(lock_file, fcntl.LOCK_SH)
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            finally:
                fcntl.flock(lock_file, fcntl.LOCK_UN)

    def save(self, state: dict):
        """Save the state dict to YAML with exclusive flock lock."""
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.lock_file_path, "w") as lock_file:
            try:
                fcntl.flock(lock_file, fcntl.LOCK_EX)
                with open(self.state_file, "w", encoding="utf-8") as f:
                    yaml.dump(state, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            finally:
                fcntl.flock(lock_file, fcntl.LOCK_UN)
