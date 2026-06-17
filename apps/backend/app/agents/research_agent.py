from agent_core import BaseAgent
from llm_client import NvidiaLLMClient


class ResearchAgent(BaseAgent):
    """Agent 1: Research market, competitors, pain points, trends, and desires."""

    def __init__(self, llm: NvidiaLLMClient):
        super().__init__("research_agent")
        self.llm = llm

    async def process(self, state: dict) -> dict:
        campaign = state.get("campaign", {})
        product_info = campaign.get("product_info", "")
        target_audience = campaign.get("target_audience", "")

        research = await self.llm.chat_json(
            system_prompt=(
                "You are a market research analyst. Research the market, competitors, "
                "customer pain points, trends, and desires for the given product and audience. "
                "Return JSON with keys: competitors (list), pain_points (list), trends (list), "
                "customer_desires (list), reddit_insights (list)."
            ),
            user_prompt=f"Product: {product_info}\nTarget Audience: {target_audience}",
        )

        return {"research": research}
