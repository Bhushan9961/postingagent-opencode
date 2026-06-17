from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class CreativeDirectorAgent(BaseAgent):
    """Agent 5: Choose optimal content format per platform."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("creative_director_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        content_plan = state.get("content_plan", {})
        platform_rules = state.get("platform_rules", {})

        content_format = await self.llm.chat_json(
            system_prompt=(
                "You are a creative director. Choose the optimal content format for each "
                "platform considering platform rules. Return JSON with per-platform "
                "content_type, duration, layout, and CTA."
            ),
            user_prompt=f"Content Plan: {content_plan}\nPlatform Rules: {platform_rules}",
        )
        return {"content_format": content_format}
