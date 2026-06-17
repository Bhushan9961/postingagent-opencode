from openai import AsyncOpenAI
import structlog

logger = structlog.get_logger()

DEFAULT_MODEL = "deepseek-ai/deepseek-v4-pro"
IMAGE_MODEL = "qwen/qwen-image"
TTS_MODEL = "resemble-ai/chatterbox-multilingual-tts"


class NvidiaLLMClient:
    """Client for NVIDIA NIM API (OpenAI-compatible)."""

    def __init__(self, api_key: str, base_url: str = "https://integrate.api.nvidia.com/v1"):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.logger = logger.bind(service="nvidia_llm")

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        self.logger.info("llm_request", model=model)
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.3,
    ) -> dict:
        self.logger.info("llm_json_request", model=model)
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\nReturn valid JSON only."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        import json

        return json.loads(content)

    async def generate_image(
        self,
        prompt: str,
        model: str = IMAGE_MODEL,
        size: str = "1024x1024",
    ) -> str | None:
        self.logger.info("image_request", model=model)
        response = await self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            n=1,
        )
        if response.data and len(response.data) > 0:
            return response.data[0].url
        return None
