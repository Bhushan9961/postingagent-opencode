from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph
from llm_client import NvidiaLLMClient

from app.agents.content_planner_agent import ContentPlannerAgent
from app.agents.creative_director_agent import CreativeDirectorAgent
from app.agents.platform_intelligence_agent import PlatformIntelligenceAgent
from app.agents.remaining_agents import (
    AnalyticsAgent,
    BrandGuardianAgent,
    CarouselAgent,
    ImageAgent,
    LearningAgent,
    OptimizationAgent,
    PublisherAgent,
    QualityControlAgent,
    VideoAgent,
    VideoEditorAgent,
    VoiceAgent,
)
from app.agents.research_agent import ResearchAgent
from app.agents.state import CampaignState
from app.agents.storytelling_agent import StorytellingAgent
from app.agents.strategy_agent import StrategyAgent
from app.services.socialclaw_client import SocialClawClient


def build_campaign_graph(llm: NvidiaLLMClient, db_url: str | None = None, socialclaw: SocialClawClient | None = None):
    research_agent = ResearchAgent(llm)
    platform_agent = PlatformIntelligenceAgent()
    strategy_agent = StrategyAgent(llm)
    content_planner = ContentPlannerAgent(llm)
    creative_director = CreativeDirectorAgent(llm)
    storytelling = StorytellingAgent(llm)
    image_agent = ImageAgent(llm)
    carousel_agent = CarouselAgent()
    video_agent = VideoAgent()
    voice_agent = VoiceAgent(llm)
    video_editor = VideoEditorAgent()
    brand_guardian = BrandGuardianAgent()
    qc_agent = QualityControlAgent(llm)
    publisher = PublisherAgent(socialclaw=socialclaw)
    analytics = AnalyticsAgent()
    learning = LearningAgent(llm)
    optimization = OptimizationAgent(llm)

    workflow = StateGraph(CampaignState)

    workflow.add_node("research", research_agent)
    workflow.add_node("platform_intelligence", platform_agent)
    workflow.add_node("strategy", strategy_agent)
    workflow.add_node("content_plan", content_planner)
    workflow.add_node("creative_direction", creative_director)
    workflow.add_node("storytelling", storytelling)
    workflow.add_node("image_generation", image_agent)
    workflow.add_node("carousel_generation", carousel_agent)
    workflow.add_node("video_scene_gen", video_agent)
    workflow.add_node("voiceover", voice_agent)
    workflow.add_node("video_editing", video_editor)
    workflow.add_node("brand_check", brand_guardian)
    workflow.add_node("quality_control", qc_agent)
    workflow.add_node("publisher", publisher)
    workflow.add_node("analytics", analytics)
    workflow.add_node("learning", learning)
    workflow.add_node("optimization", optimization)

    workflow.add_conditional_edges(
        "quality_control",
        lambda state: "publisher" if state.get("quality", {}).get("qc_score", 0) >= 0.7 else END,
    )

    sequential_edges = [
        ("research", "platform_intelligence"),
        ("platform_intelligence", "strategy"),
        ("strategy", "content_plan"),
        ("content_plan", "creative_direction"),
        ("creative_direction", "storytelling"),
        ("storytelling", "image_generation"),
        ("image_generation", "carousel_generation"),
        ("carousel_generation", "video_scene_gen"),
        ("video_scene_gen", "voiceover"),
        ("voiceover", "video_editing"),
        ("video_editing", "brand_check"),
        ("brand_check", "quality_control"),
        ("publisher", "analytics"),
        ("analytics", "learning"),
        ("learning", "optimization"),
    ]

    for source, target in sequential_edges:
        workflow.add_edge(source, target)

    workflow.add_edge("optimization", END)
    workflow.set_entry_point("research")

    if db_url:
        checkpointer = PostgresSaver.from_conn_string(db_url)
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()


async def run_campaign(llm: NvidiaLLMClient, campaign_data: dict, db_url: str | None = None) -> dict:
    graph = build_campaign_graph(llm, db_url)
    initial_state: CampaignState = {
        "campaign": campaign_data,
        "research": {},
        "platform_rules": {},
        "strategy": {},
        "content_plan": {},
        "content_format": {},
        "story": {},
        "assets": {},
        "quality": {},
        "analytics": {},
        "learnings": {},
        "optimization": {},
    }
    result = await graph.ainvoke(initial_state)
    return result
