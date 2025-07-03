# ไฟล์: agents/research_agent.py
from .base_agent import BaseAgent
class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent", description="Finds and summarizes info from the internet.", tools=["web_search"])