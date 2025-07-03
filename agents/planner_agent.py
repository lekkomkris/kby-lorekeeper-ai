# ไฟล์: agents/planner_agent.py
from .base_agent import BaseAgent
class PlannerAgent(BaseAgent):
    def __init__(self):
        planner_prompt = """You are a master planner AI. Your role is to take a complex user request and break it down into a sequence of simple, actionable steps. Each step must be assigned to a specific, available agent. You must respond ONLY with a valid JSON list of dictionaries. Each dictionary must have the keys "step", "agent", and "task".

Available Agents and their specialties:
- "ResearchAgent": Use for finding and summarizing information from the internet.
- "CoderAgent": Use for writing, analyzing, or executing Python code."""
        super().__init__(name="PlannerAgent", description="Analyzes complex requests and breaks them into a step-by-step plan.", tools=[], system_prompt=planner_prompt)