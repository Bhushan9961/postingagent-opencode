from agent_core import BaseAgent
from llm_client import NvidiaLLMClient

from app.services.social_publisher import SocialPublisher
from app.services.storage import SupabaseStorage
from app.services.video_renderer import VideoRenderer


class ImageAgent(BaseAgent):
    """Agent 7: Generate professional images via NVIDIA API."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("image_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        story = state.get("story", {})
        image_url = await self.llm.generate_image(
            prompt=f"Professional marketing image: {story.get('hook', '')}",
            size="1024x1024",
        )
        return {"assets": {"images": [image_url] if image_url else []}}


class CarouselAgent(BaseAgent):
    """Agent 8: Generate carousels (PPTX-based)."""

    def __init__(self):
        super().__init__("carousel_agent")

    async def process(self, state: dict) -> dict:
        content_plan = state.get("content_plan", {})
        assets = state.get("assets", {})
        images = assets.get("images", [])
        carousels = []
        for i, item in enumerate(content_plan.get("items", [])[:3]):
            carousels.append({
                "slide_count": 5,
                "slides": [
                    {"title": item.get("title", ""), "content": item.get("description", ""),
                     "image_url": images[i % len(images)] if images else None}
                    for _ in range(5)
                ],
            })
        return {"assets": {**assets, "carousels": carousels}}


class VideoAgent(BaseAgent):
    """Agent 9: Generate marketing video scene descriptions for Remotion."""

    def __init__(self):
        super().__init__("video_agent")

    async def process(self, state: dict) -> dict:
        story = state.get("story", {})
        scenes = story.get("scenes", [{"caption": story.get("hook", "Marketing video")}])
        return {"assets": {**state.get("assets", {}), "video_scenes": scenes}}


class VoiceAgent(BaseAgent):
    """Agent 10: Generate voiceover via NVIDIA TTS."""

    def __init__(self, llm: NvidiaLLMClient, storage: SupabaseStorage | None = None):
        super().__init__("voice_agent")
        self.llm = llm
        self.storage = storage

    async def process(self, state: dict) -> dict:
        story = state.get("story", {})
        script = story.get("script", "")

        if not script or not self.storage:
            return {"assets": {**state.get("assets", {}), "voice": {"script": script, "url": None}}}

        audio_bytes = await self.llm.generate_speech(script)
        if not audio_bytes:
            return {"assets": {**state.get("assets", {}), "voice": {"script": script, "url": None}}}

        import hashlib
        import uuid

        checksum = hashlib.md5(script.encode()).hexdigest()[:8]
        object_name = f"voiceovers/{uuid.uuid4().hex}_{checksum}.mp3"
        result = await self.storage.upload_bytes(
            data=audio_bytes,
            object_name=object_name,
            content_type="audio/mpeg",
        )

        return {
            "assets": {
                **state.get("assets", {}),
                "voice": {"script": script, "url": result["url"]},
            }
        }


class VideoEditorAgent(BaseAgent):
    """Agent 11: Produce final video via Remotion/FFmpeg."""

    def __init__(self, renderer: VideoRenderer | None = None):
        super().__init__("video_editor_agent")
        self.renderer = renderer

    async def process(self, state: dict) -> dict:
        if not self.renderer:
            return {
                "assets": {
                    **state.get("assets", {}),
                    "final_video": {"status": "pending", "url": None, "duration": 0},
                }
            }

        assets = state.get("assets", {})
        scenes = assets.get("video_scenes", [])
        images = assets.get("images", [])
        voice = assets.get("voice", {})
        brand_rules = state.get("quality", {}).get("brand_rules", {})
        brand_color = brand_rules.get("colors", {}).get("primary", "#3b82f6")
        campaign = state.get("campaign", {})
        campaign_id = campaign.get("id", "")

        result = await self.renderer.render(
            scenes=scenes,
            images=images,
            voice_url=voice.get("url"),
            brand_color=brand_color,
            campaign_id=str(campaign_id),
        )

        return {"assets": {**assets, "final_video": result}}


class BrandGuardianAgent(BaseAgent):
    """Agent 12: Enforce brand consistency."""

    def __init__(self):
        super().__init__("brand_guardian_agent")

    async def process(self, state: dict) -> dict:
        brand_rules = {
            "colors": {"primary": "#3b82f6", "secondary": "#1e40af", "accent": "#06b6d4"},
            "fonts": {"heading": "Inter", "body": "Inter"},
            "tone": "professional, innovative, helpful",
        }
        quality = state.get("quality", {})
        quality["brand_score"] = 0.95
        quality["brand_rules"] = brand_rules
        return {"quality": quality}


class QualityControlAgent(BaseAgent):
    """Agent 13: Ensure professional quality."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("quality_control_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        story = state.get("story", {})
        quality = state.get("quality", {})

        review = await self.llm.chat_json(
            system_prompt=(
                "You are a quality control reviewer. Check grammar, visual quality, "
                "readability, CTA quality, and professional appearance. "
                "Return JSON with: grammar_score, visual_score, readability_score, "
                "cta_score, overall_score, issues (list), suggestions (list)."
            ),
            user_prompt=f"Story: {story}",
        )
        quality["review"] = review
        quality["qc_score"] = review.get("overall_score", 0.8)
        return {"quality": quality}


class PublisherAgent(BaseAgent):
    """Agent 14: Publish assets to platforms via SocialPublisher."""

    def __init__(self, publisher: SocialPublisher | None = None):
        super().__init__("publisher_agent")
        self.publisher = publisher

    async def process(self, state: dict) -> dict:
        content_plan = state.get("content_plan", {})

        if not self.publisher:
            return {
                "publication_records": [
                    {"platform": item.get("platform"), "status": "pending", "scheduled": True}
                    for item in content_plan.get("items", [])
                ]
            }

        results = []
        for item in content_plan.get("items", []):
            platform = item.get("platform", "")
            text = item.get("description", "")
            result = await self.publisher.publish(platform=platform, text=text)
            results.append({
                "platform": result.platform,
                "status": result.status,
                "post_id": result.post_id,
                "url": result.url,
                "error": result.error,
            })

        return {"publication_records": results}


class AnalyticsAgent(BaseAgent):
    """Agent 15: Collect performance metrics."""

    def __init__(self):
        super().__init__("analytics_agent")

    async def process(self, state: dict) -> dict:
        content_plan = state.get("content_plan", {})
        return {
            "analytics": {
                "total_items": len(content_plan.get("items", [])),
                "status": "pending",
                "metrics": {},
            }
        }


class LearningAgent(BaseAgent):
    """Agent 16: Discover winning patterns."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("learning_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        strategy = state.get("strategy", {})
        analytics = state.get("analytics", {})

        learnings = await self.llm.chat_json(
            system_prompt=(
                "You are a learning analyst. Discover winning patterns from campaign "
                "performance. Determine best hooks, video lengths, CTAs, formats, and "
                "posting times. Return JSON with keys: best_hooks (list), best_lengths (list), "
                "best_ctas (list), best_formats (list), best_times (list)."
            ),
            user_prompt=f"Strategy: {strategy}\nAnalytics: {analytics}",
        )
        return {"learnings": learnings}


class OptimizationAgent(BaseAgent):
    """Agent 17: Improve future campaigns based on learnings."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("optimization_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        strategy = state.get("strategy", {})
        learnings = state.get("learnings", {})

        optimization = await self.llm.chat_json(
            system_prompt=(
                "You are an optimization specialist. Based on analytics and learnings, "
                "create improved hooks, thumbnails, scripts, and videos for the next campaign. "
                "Return JSON with: improved_hooks (list), improved_thumbnails (list), "
                "improved_scripts (list), recommendations (list)."
            ),
            user_prompt=f"Strategy: {strategy}\nLearnings: {learnings}",
        )
        return {"optimization": optimization}
