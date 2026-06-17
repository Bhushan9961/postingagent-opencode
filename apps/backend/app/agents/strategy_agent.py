from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class StrategyAgent(BaseAgent):
    """Agent 3: Act as marketing strategist — theme, positioning, emotion, angle, offer."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("strategy_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        campaign = state.get("campaign", {})
        research = state.get("research", {})

        strategy = await self.llm.chat_json(
            system_prompt=(
                "You are a senior marketing strategist. Based on research, determine: "
                "campaign theme, positioning, core emotion, marketing angle, and offer strategy. "
                "Return JSON with keys: theme, positioning, core_emotion, marketing_angle, offer_strategy."
            ),
            user_prompt=f"Campaign: {campaign}\nResearch: {research}",
        )

        return {"strategy": strategy}
