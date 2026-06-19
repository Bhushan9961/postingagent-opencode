import asyncio
import os
import uuid

from openai import AsyncOpenAI, RateLimitError
import structlog

logger = structlog.get_logger()

DEFAULT_MODEL = "deepseek-ai/deepseek-v4-pro"
IMAGE_MODEL = "qwen/qwen-image"
TTS_MODEL = "resemble-ai/chatterbox-multilingual-tts"

MAX_RETRIES = 3
BASE_DELAY = 2.0


class NvidiaLLMClient:
    """Client for NVIDIA NIM API (OpenAI-compatible)."""

    def __init__(self, api_key: str, base_url: str = "https://integrate.api.nvidia.com/v1"):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.logger = logger.bind(service="nvidia_llm")

    async def _chat_with_retry(self, **kwargs) -> object:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return await self.client.chat.completions.create(**kwargs)
            except RateLimitError:
                if attempt < MAX_RETRIES:
                    delay = min(BASE_DELAY * (2 ** (attempt - 1)), 30)
                    self.logger.warning(
                        "rate_limited", attempt=attempt, max_retries=MAX_RETRIES, delay=delay
                    )
                    await asyncio.sleep(delay)
                else:
                    raise

    async def generate_speech(self, text: str, model: str = TTS_MODEL) -> bytes | None:
        self.logger.info("tts_request", model=model)
        try:
            response = await self.client.audio.speech.create(
                model=model,
                voice="default",
                input=text,
                response_format="mp3",
            )
            return response.content
        except Exception as e:
            self.logger.error("tts_failed", error=str(e))
            return None

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        self.logger.info("llm_request", model=model)
        response = await self._chat_with_retry(
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
        response = await self._chat_with_retry(
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
        size: str = "1024x1024",
    ) -> str | None:
        self.logger.info("pillow_image", prompt=prompt)
        try:
            from PIL import Image, ImageDraw, ImageFont

            w, h = (int(x) for x in size.split("x"))
            img = Image.new("RGB", (w, h), color="#0f172a")
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except OSError:
                font = ImageFont.load_default()

            lines = []
            words = prompt.split()
            line = ""
            for word in words:
                test = f"{line} {word}".strip()
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] > w - 200:
                    lines.append(line)
                    line = word
                else:
                    line = test
            lines.append(line)

            y = h // 2 - (len(lines) * 64) // 2
            for line_text in lines:
                bbox = draw.textbbox((0, 0), line_text, font=font)
                x = (w - (bbox[2] - bbox[0])) // 2
                draw.text((x, y), line_text, fill="#f1f5f9", font=font)
                y += 64

            draw.rectangle(
                [(w // 2 - 30, y + 20), (w // 2 + 30, y + 24)], fill="#3b82f6"
            )

            output_dir = os.environ.get("RENDER_TEMP_DIR", "/tmp")
            os.makedirs(output_dir, exist_ok=True)
            path = os.path.join(output_dir, f"img_{uuid.uuid4().hex}.png")
            img.save(path)
            return path
        except Exception as e:
            self.logger.error("image_gen_failed", error=str(e))
            return None
