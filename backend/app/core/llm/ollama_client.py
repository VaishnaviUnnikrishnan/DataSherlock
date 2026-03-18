import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Fallback local LLM client via Ollama."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    def chat(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"[Ollama Error] {str(e)}"
