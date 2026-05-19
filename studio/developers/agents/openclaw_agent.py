import asyncio
import os
import uuid
from pathlib import Path
from .base import BaseAgent

class OpenClawAgent(BaseAgent):
    """Wrapper for the OpenClaw CLI."""

    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        timeout = kwargs.get("timeout", 180.0)
        # OpenClaw agent mode with --json output
        candidates = [
            ["openclaw", "agent", "--local", "--message", prompt],
            ["openclaw", "agent", "--message", prompt],
            ["openclaw", "agent", "--json", "--message", prompt],
        ]

        env = os.environ.copy()

        # try normal candidates first
        last_err = None
        for cmd in candidates:
            try:
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                out = stdout.decode(errors="replace").strip()
                err = stderr.decode(errors="replace").strip()
                if proc.returncode == 0 and out:
                    return out
                last_err = err or last_err
            except Exception as e:
                last_err = str(e)
                continue

        # Fallback 1: try supplying a generated session-id (some OpenClaw setups require explicit session selection)
        gen_session = kwargs.get("session_id") or f"axel-{uuid.uuid4().hex[:8]}"
        fallback_cmds = [
            ["openclaw", "agent", "--local", "--session-id", gen_session, "--message", prompt],
            ["openclaw", "agent", "--agent", "axel", "--message", prompt],
            ["openclaw", "agent", "--session-id", gen_session, "--message", prompt],
        ]

        for cmd in fallback_cmds:
            try:
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                out = stdout.decode(errors="replace").strip()
                err = stderr.decode(errors="replace").strip()
                # persist stderr for debugging
                try:
                    session_dir.mkdir(parents=True, exist_ok=True)
                    (session_dir / "_openclaw.err").write_text(err or "")
                except Exception:
                    pass
                if proc.returncode == 0 and out:
                    return out
                last_err = err or last_err
            except Exception as e:
                last_err = str(e)
                continue

        # Fallback: help dump
        try:
            proc = await asyncio.create_subprocess_exec("openclaw", "agent", "--help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10.0)
            help_text = stdout.decode(errors="replace") + "\n" + stderr.decode(errors="replace")
        except Exception as e:
            help_text = f"(Failed to run openclaw agent --help: {e})"

        # Persist last_err as well for debugging
        try:
            session_dir.mkdir(parents=True, exist_ok=True)
            if last_err:
                (session_dir / "_openclaw.err").write_text((last_err or "") + "\n\n" + help_text)
        except Exception:
            pass

        return f"[ERROR openclaw] No successful invocation. Help:\n{help_text}"
