import asyncio
import os
from pathlib import Path
from .base import BaseAgent

class HermesAgent(BaseAgent):
    """Hermes CLI wrapper for co-work panel."""

    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        session_file = session_dir / "hermes_session_id"
        session_id = None
        if session_file.exists():
            content = session_file.read_text().strip()
            if content:
                session_id = content

        # Strip CLAUDECODE from env to avoid hermes picking it up
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        if session_id:
            cmd = ["hermes", "--resume", session_id, "-z", prompt]
        else:
            cmd = ["hermes", "-z", prompt]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=kwargs.get("timeout", 180.0))
        output = stdout.decode(errors="replace").strip()

        if proc.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            output += f"\n[ERROR hermes] {err or f'exit code {proc.returncode}'}"

        # Capture session ID for future --resume
        if not session_id and output:
            for line in output.splitlines():
                if line.startswith("session_id:"):
                    new_id = line.split(":", 1)[1].strip()
                    if new_id:
                        session_file.write_text(new_id)
                        break

        return output if output else "(empty response from hermes)"
