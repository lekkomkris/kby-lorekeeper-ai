import json
import os
from api_clients import ask_gemini, search_tavily, execute_python_code_in_docker

class BaseAgent:
    """
    คลาสแม่แบบสำหรับ AI Agent ทุกตัวใน Metamind OS
    ประกอบไปด้วยตรรกะ ReAct (Reasoning and Acting) พื้นฐาน
    """
    def __init__(self, name: str, description: str, tools: list, system_prompt: str = ""):
        self.name = name
        self.description = description
        self.tools = tools
        self.system_prompt = system_prompt if system_prompt else self._create_default_system_prompt()

    def _create_default_system_prompt(self):
        """สร้าง System Prompt พื้นฐานโดยอัตโนมัติตามเครื่องมือที่ Agent มี"""
        tool_descriptions = []
        if "web_search" in self.tools:
            tool_descriptions.append('- "web_search": Use this to search the internet for recent events or information.')
        if "python_interpreter" in self.tools:
            tool_descriptions.append('- "python_interpreter": Use this to execute Python code for calculations, file I/O, etc.')
        
        if not tool_descriptions:
            return f"You are {self.name}, a specialized AI assistant. Your role is: {self.description}. Please answer the user's request directly."

        return f"""
You are {self.name}, a specialized AI assistant. Your role is: {self.description}.
You have access to the following tools. To use a tool, you must respond ONLY with a single, valid JSON object in the format:
{{"tool": "tool_name", "query": "your_search_query_or_code"}}

Available tools:
{"\n".join(tool_descriptions)}

If you can answer directly from your knowledge, do so in a normal, conversational manner.
"""

    def _clean_code_string(self, code_string: str):
        """Removes markdown fences from a code string if they exist."""
        if code_string.strip().startswith("```python"):
            code_string = code_string.strip()[9:]
        if code_string.strip().startswith("```"):
            code_string = code_string.strip()[3:]
        if code_string.strip().endswith("```"):
            code_string = code_string.strip()[:-3]
        return code_string.strip()

    def _execute_tool(self, tool_name, tool_query):
        """เรียกใช้เครื่องมือตามที่ AI ร้องขอ"""
        print(f"\n[System] Executing tool: '{tool_name}'...")
        if tool_name == "web_search":
            return search_tavily(tool_query)
        elif tool_name == "python_interpreter":
            clean_code = self._clean_code_string(tool_query)
            print(f"--- Code to Execute ---\n{clean_code}\n-----------------------")
            return execute_python_code_in_docker(clean_code)
        else:
            return f"Error: Unknown tool '{tool_name}'"

    def run(self, user_prompt: str):
        """เมธอดหลักในการรัน Agent ซึ่งมี ReAct Loop อยู่ข้างใน"""
        print(f"[{self.name}] Received task. Thinking...")
        initial_prompt = f"{self.system_prompt}\n\nUser's Task: {user_prompt}"
        response_text = ask_gemini(initial_prompt)

        try:
            start_index = response_text.find('{')
            end_index = response_text.rfind('}') + 1
            if start_index != -1 and end_index != 0:
                json_str = response_text[start_index:end_index]
                tool_call = json.loads(json_str)
            else:
                raise ValueError("No JSON object found")

            if "tool" in tool_call and "query" in tool_call:
                tool_name = tool_call["tool"]
                tool_query = tool_call["query"]
                
                print(f"[{self.name}] Decided to use tool: '{tool_name}'...")
                tool_result = self._execute_tool(tool_name, tool_query)
                
                print(f"[System] Task completed. Tool Output:\n{tool_result}")
                print(f"[{self.name}] Synthesizing final answer...")

                second_prompt = f"Based on the result from using the '{tool_name}' tool, which was:\n---\n{tool_result}\n---\nPlease provide a final, comprehensive answer to the original user task: \"{user_prompt}\""
                final_answer = ask_gemini(second_prompt)
                return final_answer
        
        except (json.JSONDecodeError, ValueError, TypeError):
            # AI ตอบกลับโดยตรง
            return response_text