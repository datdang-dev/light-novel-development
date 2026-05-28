import base64
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image
from studio.core.caption_engine.interfaces.mcp_client import MCPClient


class ToriigateMCPAdapter(MCPClient):
    """Concrete MCPClient implementation communicating with ToriiGate Vision Model Server (serve.py)."""

    def __init__(self, api_url: str = "http://127.0.0.1:1234"):
        self.api_url = api_url

    def _encode_image(self, image_path: str) -> str:
        """Encode target image to base64 JPEG representation."""
        img = Image.open(image_path)
        buf = BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode()

    async def _call_api(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        stream_tokens: bool = True,
    ) -> str:
        payload = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "top_k": 40,
            "min_p": 0.05,
            "repeat_penalty": 1.1,
            "stream_tokens": stream_tokens,
        }

        async with httpx.AsyncClient(timeout=300.0) as client:
            resp = await client.post(
                f"{self.api_url}/v1/chat/completions",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                data = data[0]
            else:
                raise RuntimeError(f"Unexpected response list format: {data}")

        if isinstance(data, dict) and "error" in data:
            raise RuntimeError(f"Backend error: {data['error']}")

        if not isinstance(data, dict):
            raise RuntimeError(f"Expected dict response but got {type(data)}: {data}")

        return (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

    async def analyze_forensic(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are Kana, a forensic visual analyst specializing in R18 manga content analysis."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ]
            }
        ]
        return await self._call_api(messages, max_tokens, temperature, stream_tokens=stream_tokens)

    async def generate_prelude(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are Luna, a narrative world-builder specializing in erotic fiction scenario design."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ]
            }
        ]
        return await self._call_api(messages, max_tokens, temperature, stream_tokens=stream_tokens)

    async def generate_caption(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are Suki, the R18 Prose and Caption specialist."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ]
            }
        ]
        return await self._call_api(messages, max_tokens, temperature, stream_tokens=stream_tokens)
