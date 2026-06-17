from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class StorytellingAgent(BaseAgent):
    """Agent 6: Create high-converting content with hooks, scripts, narratives, CTAs."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("storytelling_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        strategy = state.get("strategy", {})
        content_format = state.get("content_format", {})

        story = await self.llm.chat_json(
            system_prompt=(
                "You are a master storyteller. Create high-converting content using "
                "AIDA, PAS, StoryBrand, or Hero Journey frameworks. Generate hooks, "
                "scripts, narratives, CTAs, and scene descriptions. "
                "Return JSON with keys: hook, script, narrative, cta, scenes (list)."
            ),
            user_prompt=f"Strategy: {strategy}\nFormat: {content_format}",
        )
        return {"story": story}
