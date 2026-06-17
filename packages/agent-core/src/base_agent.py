from abc import ABC, abstractmethod
from typing import Any

import structlog

logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all LangGraph agents."""

    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(agent=self.name)

    @abstractmethod
    async def process(self, state: dict) -> dict:
        """Process the current campaign state and return updates."""
        ...

    async def __call__(self, state: dict) -> dict:
        self.logger.info("agent_started")
        try:
            result = await self.process(state)
            self.logger.info("agent_completed")
            return result
        except Exception as e:
            self.logger.error("agent_failed", error=str(e))
            raise
