import json
import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any

import httpx
import structlog

logger = structlog.get_logger()

REMOTION_DIR = str(Path(__file__).resolve().parents[3] / "apps" / "remotion")
TEMP_DIR = str(Path(__file__).resolve().parents[3] / "data" / "renders")
os.makedirs(TEMP_DIR, exist_ok=True)


class RemotionUnavailableError(Exception):
    pass


class VideoRenderer:
    def __init__(self, supabase_storage: Any | None = None):
        self.storage = supabase_storage
        self.logger = logger.bind(service="video_renderer")

    async def render(
        self,
        scenes: list[dict],
        images: list[str] | None = None,
        voice_url: str | None = None,
        brand_color: str = "#3b82f6",
        campaign_id: str = "",
    ) -> dict:
        scenes = scenes or []
        if not scenes:
            scenes = [
                {"caption": "Your AI Marketing Operating System", "duration": 90},
                {"caption": "Research. Create. Publish. Learn.", "duration": 90},
            ]

        enriched_scenes = []
        for i, scene in enumerate(scenes):
            enriched_scenes.append({
                "caption": scene.get("caption", ""),
                "duration": scene.get("duration", 90),
                "imageUrl": images[i % len(images)] if images else None,
            })

        try:
            result = await self._render_remotion(enriched_scenes, brand_color, campaign_id)
            if result["status"] == "completed":
                return result
        except (RemotionUnavailableError, FileNotFoundError) as e:
            self.logger.warning("remotion_unavailable", reason=str(e))

        try:
            result = await self._render_ffmpeg(enriched_scenes, voice_url, brand_color, campaign_id)
            return result
        except Exception as e:
            self.logger.error("both_renderers_failed", error=str(e))
            return {"status": "failed", "url": None, "duration": 0, "error": str(e)}

    async def _render_remotion(
        self, scenes: list[dict], brand_color: str, campaign_id: str
    ) -> dict:
        if not os.path.isdir(REMOTION_DIR):
            raise RemotionUnavailableError(f"Remotion dir not found: {REMOTION_DIR}")

        try:
            subprocess.run(
                ["npx", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RemotionUnavailableError("npx not available") from e

        render_id = uuid.uuid4().hex[:12]
        suffix = f"{campaign_id}_{render_id}.mp4" if campaign_id else f"{render_id}.mp4"
        stem = f"campaign_{suffix}" if campaign_id else f"video_{suffix}"
        output_path = os.path.join(TEMP_DIR, stem)
        output_file = stem

        input_props = json.dumps({"scenes": scenes, "brandColor": brand_color})

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(input_props)
            props_file = f.name

        try:
            result = subprocess.run(
                [
                    "npx", "remotion", "render",
                    "src/index.ts",
                    "MarketingVideo",
                    output_path,
                    "--props", props_file,
                    "--log", "error",
                ],
                cwd=REMOTION_DIR,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                raise RemotionUnavailableError(f"Remotion render failed: {result.stderr}")

            video_url = await self._upload_result(output_path, output_file)

            return {
                "status": "completed",
                "url": video_url,
                "duration": sum(s.get("duration", 90) for s in scenes) / 30,
                "renderer": "remotion",
            }
        finally:
            if os.path.exists(props_file):
                os.unlink(props_file)
            if os.path.exists(output_path):
                os.unlink(output_path)

    async def _render_ffmpeg(
        self, scenes: list[dict], voice_url: str | None, brand_color: str, campaign_id: str
    ) -> dict:
        render_id = uuid.uuid4().hex[:12]
        suffix = f"{campaign_id}_{render_id}.mp4" if campaign_id else f"{render_id}.mp4"
        stem = f"campaign_{suffix}" if campaign_id else f"video_{suffix}"
        output_path = os.path.join(TEMP_DIR, stem)
        output_file = stem

        try:
            from moviepy import (
                AudioFileClip,
                CompositeVideoClip,
                ImageClip,
                TextClip,
            )
        except ImportError:
            return {
                "status": "failed", "url": None, "duration": 0, "error": "moviepy not installed"
            }

        _temp_files = set()

        try:
            audio_clip = None
            audio_path = None
            if voice_url:
                try:
                    async with httpx.AsyncClient(timeout=30) as client:
                        r = await client.get(voice_url)
                        if r.status_code == 200:
                            audio_path = os.path.join(TEMP_DIR, f"audio_{render_id}.mp3")
                            with open(audio_path, "wb") as f:
                                f.write(r.content)
                            audio_clip = AudioFileClip(audio_path)
                        else:
                            self.logger.warning("voice_download_failed", status=r.status_code)
                except Exception as e:
                    self.logger.warning("voice_download_error", error=str(e))

            clip_duration = audio_clip.duration if audio_clip else max(len(scenes) * 3, 6)

            vclips = []
            per_scene_duration = clip_duration / max(len(scenes), 1)

            for i, scene in enumerate(scenes):
                start = i * per_scene_duration
                dur = per_scene_duration

                img_src = scene.get("imageUrl") or self._generate_title_card(
                    scene["caption"], brand_color
                )
                bg = ImageClip(img_src, duration=dur).resized(
                    height=1920
                ).with_position(("center", "center"))

                txt = TextClip(
                    text=scene["caption"],
                    font_size=48,
                    color="#f1f5f9",
                    stroke_color="black",
                    stroke_width=2,
                    font="system-ui",
                    text_align="center",
                    size=(864, None),
                    method="caption",
                ).with_duration(dur).with_position(("center", "center")).with_start(start)

                brand = TextClip(
                    text="AI Marketing OS",
                    font_size=14,
                    color="#94a3b8",
                    font="system-ui",
                ).with_duration(dur).with_position(("right", "bottom")).with_start(start)

                vclips.extend([bg, txt, brand])

            if not vclips:
                return {
                    "status": "failed", "url": None, "duration": 0, "error": "no clips generated"
                }

            final = CompositeVideoClip(vclips, size=(1080, 1920)).with_duration(clip_duration)

            if audio_clip:
                final = final.with_audio(audio_clip)

            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                preset="ultrafast",
                logger=None,
            )

            final.close()
            if audio_clip:
                audio_clip.close()

            _temp_files.add(output_path)
            if audio_path:
                _temp_files.add(audio_path)

            video_url = await self._upload_result(output_path, output_file)

            return {
                "status": "completed",
                "url": video_url,
                "duration": clip_duration,
                "renderer": "ffmpeg",
            }
        finally:
            for p in _temp_files:
                if os.path.exists(p):
                    os.unlink(p)

    def _generate_title_card(self, text: str, brand_color: str) -> str:
        from PIL import Image, ImageDraw, ImageFont

        card_path = os.path.join(TEMP_DIR, f"title_{uuid.uuid4().hex}.png")
        img = Image.new("RGB", (1080, 1920), color="#0f172a")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except OSError:
            font = ImageFont.load_default()

        lines = []
        words = text.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > 864:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)

        y = 800
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill="#f1f5f9", font=font)
            y += 64

        draw.rectangle([(510, y + 20), (570, y + 24)], fill=brand_color)

        img.save(card_path)
        return card_path

    async def _upload_result(self, file_path: str, object_name: str) -> str:
        if not self.storage:
            return f"file://{file_path}"

        result = await self.storage.upload_file(
            file_path=file_path,
            object_name=f"videos/{object_name}",
            content_type="video/mp4",
        )
        return result["url"]
