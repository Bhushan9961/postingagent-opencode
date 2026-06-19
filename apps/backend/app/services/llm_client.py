from llm_client import NvidiaLLMClient

from app.config.config import settings


def get_llm_client() -> NvidiaLLMClient:
    if settings.llm_api_key:
        api_key = settings.llm_api_key
        base_url = settings.llm_base_url or "https://api.deepseek.com"
    else:
        api_key = settings.nvidia_api_key
        base_url = settings.nvidia_base_url or "https://integrate.api.nvidia.com/v1"
    return NvidiaLLMClient(api_key=api_key, base_url=base_url)
