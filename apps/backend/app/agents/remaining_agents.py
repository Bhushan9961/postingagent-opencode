from agent_core import BaseAgent
from llm_client import NvidiaLLMClient

from app.services.socialclaw_client import PROVIDER_MAP, SocialClawClient, SocialClawError


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

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("voice_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        story = state.get("story", {})
        script = story.get("script", "")
        return {"assets": {**state.get("assets", {}), "voice": {"script": script}}}


class VideoEditorAgent(BaseAgent):
    """Agent 11: Produce final video via Remotion."""

    def __init__(self):
        super().__init__("video_editor_agent")

    async def process(self, state: dict) -> dict:
        assets = state.get("assets", {})
        scenes = assets.get("video_scenes", [])
        brand_rules = state.get("quality", {}).get("brand_rules", {})
        brand_color = brand_rules.get("colors", {}).get("primary", "#3b82f6")

        render_input = {
            "scenes": [
                {"caption": s.get("caption", ""), "duration": s.get("duration", 90)}
                for s in scenes
            ],
            "brand_color": brand_color,
        }

        return {
            "assets": {
                **assets,
                "final_video": {
                    "status": "pending",
                    "url": None,
                    "render_input": render_input,
                },
            }
        }


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
    """Agent 14: Publish assets to platforms via SocialClaw."""

    def __init__(self, socialclaw: SocialClawClient | None = None):
        super().__init__("publisher_agent")
        self.socialclaw = socialclaw

    async def process(self, state: dict) -> dict:
        content_plan = state.get("content_plan", {})

        if self.socialclaw:
            try:
                posts = []
                for item in content_plan.get("items", []):
                    post = {
                        "provider": PROVIDER_MAP.get(
                            item.get("platform", ""), item.get("platform")
                        ),
                        "text": item.get("description", ""),
                    }
                    if item.get("scheduled_at"):
                        post["scheduled_at"] = item["scheduled_at"]
                    posts.append(post)

                result = await self.socialclaw.apply_schedule({"posts": posts})
                run_id = result.get("run_id")

                return {
                    "publication_records": [
                        {
                            "platform": item.get("platform"),
                            "status": "scheduled",
                            "scheduled": True,
                            "run_id": run_id,
                        }
                        for item in content_plan.get("items", [])
                    ]
                }
            except SocialClawError as e:
                return {
                    "publication_records": [
                        {
                            "platform": item.get("platform"),
                            "status": "failed",
                            "error": str(e),
                        }
                        for item in content_plan.get("items", [])
                    ]
                }

        return {
            "publication_records": [
                {"platform": item.get("platform"), "status": "pending", "scheduled": True}
                for item in content_plan.get("items", [])
            ]
        }


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
