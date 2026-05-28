from abc import ABC, abstractmethod

class MCPClient(ABC):
    """Interface for invoking multi-modal and LLM backend tools."""

    @abstractmethod
    async def analyze_forensic(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        stream_tokens: bool = True,
    ) -> str:
        """Analyze an image using a compiled forensic prompt."""
        pass

    @abstractmethod
    async def generate_prelude(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        """Generate a narrative prelude from compiled prompt (multimodal or text)."""
        pass

    @abstractmethod
    async def generate_caption(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        """Generate the final erotic caption from compiled prompt."""
        pass
