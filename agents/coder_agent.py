# ไฟล์: agents/coder_agent.py
from .base_agent import BaseAgent
class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="CoderAgent", description="Writes, debugs, and executes Python code.", tools=["python_interpreter"])