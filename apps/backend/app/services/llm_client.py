from llm_client import NvidiaLLMClient

from app.config.config import settings


def get_llm_client() -> NvidiaLLMClient:
    return NvidiaLLMClient(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_base_url,
    )


DEFAULT_MODEL = "deepseek-ai/deepseek-v4-pro"
IMAGE_MODEL = "qwen/qwen-image"
TTS_MODEL = "resemble-ai/chatterbox-multilingual-tts"
