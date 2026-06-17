from openai import AsyncOpenAI

from app.config.config import settings


def get_llm_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_base_url,
    )


DEFAULT_MODEL = "deepseek-ai/deepseek-v4-pro"
IMAGE_MODEL = "qwen/qwen-image"
TTS_MODEL = "resemble-ai/chatterbox-multilingual-tts"
