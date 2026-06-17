from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class ContentPlannerAgent(BaseAgent):
    """Agent 4: Generate a 30-day content calendar."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("content_planner_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        strategy = state.get("strategy", {})
        content_plan = await self.llm.chat_json(
            system_prompt=(
                "You are a content planner. Generate a 30-day content calendar with "
                "founder stories, case studies, AI demos, product breakdowns, "
                "educational content, and behind-the-scenes content. "
                "Return JSON with key 'items' containing list of objects with keys: "
                "day (int), platform (str), content_type (str), title (str), description (str), cta (str)."
            ),
            user_prompt=f"Strategy: {strategy}",
        )
        return {"content_plan": content_plan}
