from abc import ABC, abstractmethod


class PromptLoader(ABC):
    """Interface for loading prompt templates dynamically on demand."""

    @abstractmethod
    def load_direct_prompt(self, mood_seed: str, user_context: str = "", prompt_name: str = "direct_caption") -> str:
        """Load and compile the single-step direct visual caption prompt."""
        pass
