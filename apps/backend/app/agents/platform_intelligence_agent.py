from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class PlatformIntelligenceAgent(BaseAgent):
    """Agent 2: Monitor platform requirements continuously."""

    def __init__(self):
        super().__init__("platform_intelligence_agent")

    async def process(self, state: dict) -> dict:
        platform_rules = {
            "linkedin": {
                "image_sizes": {"max_width": 1200, "max_height": 627},
                "carousel_max_pages": 10,
                "caption_limit": 3000,
                "video_max_length_seconds": 600,
                "supports": ["image", "carousel", "video", "text"],
            },
            "instagram": {
                "image_sizes": {"square": "1080x1080", "portrait": "1080x1350", "landscape": "1080x566"},
                "carousel_max_pages": 10,
                "caption_limit": 2200,
                "video_max_length_seconds": 90,
                "supports": ["image", "carousel", "video", "reels"],
            },
            "facebook": {
                "image_sizes": {"max_width": 1200, "max_height": 630},
                "carousel_max_pages": 10,
                "caption_limit": 63206,
                "video_max_length_seconds": 14400,
                "supports": ["image", "carousel", "video", "text"],
            },
            "x": {
                "image_sizes": {"max_width": 1600, "max_height": 1600},
                "caption_limit": 280,
                "video_max_length_seconds": 140,
                "supports": ["image", "video", "text", "thread"],
            },
            "youtube": {
                "image_sizes": {"thumbnail": "1280x720"},
                "video_max_length_seconds": 43200,
                "supports": ["video", "shorts"],
            },
            "pinterest": {
                "image_sizes": {"standard": "1000x1500", "square": "1000x1000"},
                "caption_limit": 500,
                "supports": ["image", "video"],
            },
        }
        return {"platform_rules": platform_rules}
