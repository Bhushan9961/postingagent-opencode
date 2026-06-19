from llm_client import NvidiaLLMClient

from app.config.config import settings


def get_llm_client() -> NvidiaLLMClient:
    api_key = settings.llm_api_key or settings.nvidia_api_key
    base_url = settings.llm_base_url or settings.nvidia_base_url
    return NvidiaLLMClient(
        api_key=api_key,
        base_url=base_url,
    )
