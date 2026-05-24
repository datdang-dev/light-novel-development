from abc import ABC, abstractmethod
from pathlib import Path
import json

class BaseAgent(ABC):
    """Base interface for AI Developer agents in the Studio."""

    def __init__(self, role_name: str, config_dir: Path):
        self.role_name = role_name
        self.config_dir = config_dir
        self.role_content = self._load_role(role_name)

    def _load_role(self, role_name: str) -> str:
        roles_dir = self.config_dir / "roles"
        role_file = roles_dir / f"{role_name}.md"
        if not role_file.exists():
            return f"# Role: {role_name}\n(Role definition not found at {role_file})"
        return role_file.read_text(errors="replace")

    def _load_knowledge(self, namespace: str, specific_files: list[str] = None) -> str:
        """Load only requested knowledge files from a namespace.

        Args:
            namespace: Knowledge namespace (se, dev, qa)
            specific_files: List of filenames to load. If None, loads all files in namespace.

        Returns:
            XML-wrapped knowledge content
        """
        index_file = self.config_dir / "knowledge_index.json"
        if not index_file.exists():
            return f"<!-- Warning: knowledge_index.json not found at {index_file} -->"

        try:
            index = json.loads(index_file.read_text())
        except json.JSONDecodeError as e:
            return f"<!-- Error parsing knowledge_index.json: {e} -->"

        if namespace not in index["namespaces"]:
            return f"<!-- Warning: Unknown namespace '{namespace}' -->"

        ns = index["namespaces"][namespace]
        base_path = Path(ns["path"])

        # Load only specific files if provided, else load all
        files_to_load = specific_files or ns["files"]

        content = [f"<knowledge namespace='{namespace}' description='{ns['description']}'>"]

        for fname in files_to_load:
            fpath = base_path / fname
            if fpath.exists():
                file_content = fpath.read_text(errors="replace")
                content.append(f"<rule file='{fname}'>\n{file_content}\n</rule>")
            else:
                content.append(f"<!-- Warning: File not found: {fpath} -->")

        content.append("</knowledge>")

        return "\n".join(content)

    async def call_api_direct(self, prompt: str, model: str = "coding-model") -> str:
        """Call the local port 20128 API directly as a robust fallback/override."""
        import urllib.request
        import json
        import asyncio

        def _parse_body(res_body: str) -> str:
            res_body = res_body.strip()
            if res_body.startswith("{"):
                try:
                    res_json = json.loads(res_body)
                    if "choices" in res_json and len(res_json["choices"]) > 0:
                        choice = res_json["choices"][0]
                        if "message" in choice and "content" in choice["message"]:
                            return choice["message"]["content"]
                        elif "delta" in choice and "content" in choice["delta"]:
                            return choice["delta"]["content"]
                    return res_body
                except Exception:
                    return res_body
            else:
                content = []
                for line in res_body.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("data:"):
                        data_str = line[len("data:"):].strip()
                        if data_str == "[DONE]":
                            continue
                        try:
                            chunk = json.loads(data_str)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                choice = chunk["choices"][0]
                                if "delta" in choice and "content" in choice["delta"]:
                                    content.append(choice["delta"]["content"])
                                elif "message" in choice and "content" in choice["message"]:
                                    content.append(choice["message"]["content"])
                        except Exception:
                            pass
                return "".join(content)

        def _make_call():
            url = "http://localhost:20128/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-21b7954167b683bc-e9yyb0-0431b1ff"
            }
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode("utf-8"), 
                headers=headers,
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=180) as response:
                    res_body = response.read().decode("utf-8")
                    return _parse_body(res_body)
            except Exception as e:
                # Try fallback model if coding-model failed
                if model == "coding-model":
                    data["model"] = "kc/google/gemini-2.5-pro"
                    req2 = urllib.request.Request(
                        url,
                        data=json.dumps(data).encode("utf-8"),
                        headers=headers,
                        method="POST"
                    )
                    try:
                        with urllib.request.urlopen(req2, timeout=180) as response2:
                            res_body2 = response2.read().decode("utf-8")
                            return _parse_body(res_body2)
                    except Exception as e2:
                        return f"[ERROR API] Both coding-model ({e}) and fallback ({e2}) failed."
                return f"[ERROR API] Request failed: {e}"

        return await asyncio.to_thread(_make_call)

    @abstractmethod
    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        """Call the agent CLI or API.

        Args:
            prompt: The full prompt string.
            session_dir: Path to the task's session directory for persistence.
        """
        pass
