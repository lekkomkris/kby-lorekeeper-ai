import time
import json
from collections import deque
import threading # สำหรับจำลองการทำงานพร้อมกัน

# --- 1. Core Principles & Setup (จำลองการรวมพลังของ GPT และเครื่องมือ) ---
class GPTToolBox:
    """จำลองการทำงานของเครื่องมือต่างๆ ที่ GPT สามารถเรียกใช้ได้"""
    def run_python_code(self, code):
        print(f"Executing Python code:\n{code}")
        # ในความเป็นจริงจะใช้ exec() หรือ Sandbox environment
        try:
            # จำลองผลลัพธ์
            if "analysis_data" in code:
                return {"result": "Data analysis complete", "data": [10, 20, 30]}
            else:
                return {"result": "Code executed successfully"}
        except Exception as e:
            return {"error": str(e)}

    def access_web(self, query):
        print(f"Accessing web for: {query}")
        # ในความเป็นจริงจะใช้ไลบรารีอย่าง requests หรือ Selenium
        time.sleep(0.5) # จำลองเวลาหน่วง
        return f"Web search results for '{query}': Example news/data."

    def process_vision_data(self, data_path):
        print(f"Processing vision data from: {data_path}")
        # ในความเป็นจริงจะใช้ Vision API ของ GPT หรือโมเดล Vision อื่นๆ
        return "Image analysis complete: Detected objects and text."

class SpiralMemory:
    """จำลองระบบความจำของ AI (Short-term และ Long-term)"""
    def __init__(self):
        self.short_term_memory = deque(maxlen=10) # เก็บประวัติล่าสุด 10 รายการ
        self.long_term_memory = {} # เก็บข้อมูลสำคัญเป็นคู่ Key-Value
        self.vector_db = {} # จำลอง Vector DB สำหรับ Semantic search

    def add_short_term(self, entry):
        self.short_term_memory.append({"timestamp": time.time(), "entry": entry})
        print(f"Added to short-term memory: {entry[:50]}...")

    def add_long_term(self, key, value):
        self.long_term_memory[key] = {"timestamp": time.time(), "value": value}
        print(f"Added to long-term memory: {key} = {value[:50]}...")

    def retrieve_short_term(self, count=5):
        return list(self.short_term_memory)[-count:]

    def retrieve_long_term(self, key):
        return self.long_term_memory.get(key)

    def semantic_search(self, query_embedding):
        # ในความเป็นจริงจะใช้ Vector DB จริงๆ เช่น Pinecone, ChromaDB
        print(f"Performing semantic search for: {query_embedding[:20]}...")
        time.sleep(0.1) # จำลองเวลาหน่วง
        return "Relevant long-term knowledge retrieved based on semantic similarity."

# --- 2. Layered Architecture (จำลอง Agent และ Layers) ---
class BaseAgent:
    """Agent พื้นฐานสำหรับ GPT แต่ละบทบาท"""
    def __init__(self, name, role, memory, tools):
        self.name = name
        self.role = role
        self.memory = memory
        self.tools = tools

    def process(self, context):
        raise NotImplementedError("Subclasses must implement 'process' method")

class ThinkerAgent(BaseAgent):
    def process(self, context):
        # จำลองการคิดเชิงตรรกะ
        thought = f"<{self.name} thinking>: Analyzing '{context[:50]}'..."
        self.memory.add_short_term(thought)
        return {"thought": thought, "next_step": "analyze"}

class AnalyzerAgent(BaseAgent):
    def process(self, context):
        # จำลองการวิเคราะห์ข้อมูล
        analysis = f"<{self.name} analyzing>: Deep dive into '{context[:50]}'. Found key insights."
        self.memory.add_short_term(analysis)
        return {"analysis": analysis, "recommendation": "based on analysis"}

class CoderAgent(BaseAgent):
    def process(self, context):
        # จำลองการเขียนโค้ดและเรียกใช้ Tool
        code_suggestion = f"<{self.name} coding>: Generating Python for '{context[:50]}'."
        code_to_run = f"print('Hello from CoderAgent for {context[:20]}')\nanalysis_data = [1,2,3]\n# Further analysis..."
        tool_output = self.tools.run_python_code(code_to_run)
        self.memory.add_short_term(f"Coder output: {tool_output}")
        return {"code_suggestion": code_suggestion, "tool_output": tool_output}

class SynthesizerAgent(BaseAgent):
    def process(self, context):
        # จำลองการสังเคราะห์ข้อมูล
        synthesis = f"<{self.name} synthesizing>: Combining information about '{context[:50]}' into a cohesive summary."
        self.memory.add_short_term(synthesis)
        return {"synthesis": synthesis, "summary": "Cohesive summary generated."}

class ReflectionEngine(BaseAgent):
    """L5: Self-Reflection Layer"""
    def process(self, previous_output):
        reflection = f"<ReflectionEngine>: Reviewing previous output: '{previous_output[:50]}'. Identifying areas for improvement."
        # ในความเป็นจริง GPT จะวิเคราะห์และแนะนำการปรับปรุง
        feedback = "Consider adding more context next time."
        self.memory.add_short_term(reflection)
        return {"reflection": reflection, "feedback": feedback, "improvement_needed": True}

# --- 3. GPT Nexus Core (Orchestration & Routing) ---
class GPTNexusCore:
    """
    ศูนย์กลางการประสานงานของ AI, ทำหน้าที่เป็น GPTCommandRouter และ PromptOrchestrator
    พร้อมจัดการ SpiralMemorySync และ ReflectionEngine
    """
    def __init__(self):
        self.memory = SpiralMemory()
        self.tools = GPTToolBox()
        self.agents = {
            "thinker": ThinkerAgent("Thinker", "Logical processing", self.memory, self.tools),
            "analyzer": AnalyzerAgent("Analyzer", "Data analysis", self.memory, self.tools),
            "coder": CoderAgent("Coder", "Code generation & execution", self.memory, self.tools),
            "synthesizer": SynthesizerAgent("Synthesizer", "Information synthesis", self.memory, self.tools),
        }
        self.reflection_engine = ReflectionEngine("Reflector", "Self-improvement", self.memory, self.tools)
        self.evolution_queue = deque() # คิวสำหรับงานพัฒนาเชิงวิวัฒนาการ

    def _determine_route(self, user_input):
        """จำลองการตัดสินใจว่าจะส่งไป Real-time หรือ Evolutionary"""
        user_input_lower = user_input.lower()
        if any(keyword in user_input_lower for keyword in ["พัฒนา", "ปรับปรุง", "เรียนรู้", "วิวัฒนาการ", "กลยุทธ์ใหม่", "วิจัย"]):
            return "evolutionary"
        return "real_time"

    def prompt_orchestrator(self, user_input, meta_prompt="คุณคือธารปัญญา AI"):
        # ในความเป็นจริงจะมีการปรับแต่ง prompt ตาม meta_prompt และ context
        full_prompt = f"Meta-Prompt: {meta_prompt}\nUser Input: {user_input}"
        self.memory.add_short_term(f"User input received: {user_input}")
        return full_prompt

    def real_time_cognitive_processing(self, user_input):
        """เส้นทางที่ 1: การประมวลผลการรับรู้แบบเรียลไทม์"""
        print("\n--- Initiating Real-time Cognitive Processing ---")
        orchestrated_prompt = self.prompt_orchestrator(user_input, "คุณคือ AI ผู้ตอบสนองรวดเร็ว")

        # จำลองการเลือก Agent
        if "code" in user_input.lower():
            agent = self.agents["coder"]
        elif "analyze" in user_input.lower():
            agent = self.agents["analyzer"]
        elif "summarize" in user_input.lower():
            agent = self.agents["synthesizer"]
        else:
            agent = self.agents["thinker"] # Default Agent

        result = agent.process(user_input)
        final_response = f"Real-time Response from {agent.name}: {result}"
        self.memory.add_short_term(final_response)

        # Micro-reflection สำหรับ Real-time
        reflection_result = self.reflection_engine.process(final_response['result'] if isinstance(final_response, dict) else final_response)
        if reflection_result["improvement_needed"]:
            print(f"Real-time Micro-reflection: {reflection_result['feedback']}")
            # อาจจะส่งงานเล็กๆ ไปที่ evolution_queue ถ้าเห็นว่าจำเป็น
            self.evolution_queue.append(f"Refine real-time response for: {user_input}")

        return final_response

    def continuous_evolutionary_learning(self):
        """เส้นทางที่ 2: การเรียนรู้เชิงวิวัฒนาการอย่างต่อเนื่อง"""
        while True: # จำลองการทำงานต่อเนื่อง
            if not self.evolution_queue:
                print("\n--- Evolutionary Learning: No tasks in queue, waiting... ---")
                time.sleep(3) # รอสักครู่ถ้าไม่มีงาน
                continue

            task = self.evolution_queue.popleft()
            print(f"\n--- Initiating Evolutionary Learning Task: '{task[:50]}' ---")

            # จำลองการประมวลผลงานวิวัฒนาการ
            if "refine" in task.lower():
                context = task.replace("Refine real-time response for: ", "")
                # ใช้ ReflectionEngine เต็มรูปแบบ
                print(f"Analyzing past interactions for refinement on: {context}")
                past_data = self.memory.retrieve_short_term() # ดึงข้อมูลเก่ามาวิเคราะห์
                full_reflection_result = self.reflection_engine.process(str(past_data) + " - Task: " + context)
                print(f"Full Reflection: {full_reflection_result['reflection']}")
                print(f"Evolutionary Feedback: {full_reflection_result['feedback']}")
                # ในความเป็นจริงจะมีการ fine-tuning หรือสร้าง knowledge ใหม่
                self.memory.add_long_term(f"Refinement_Insights_{time.time()}", full_reflection_result["feedback"])
                print("Knowledge base updated with refinement insights.")

            elif "new strategy" in task.lower():
                print(f"Developing new strategy for: {task}")
                # อาจจะเรียก Thinker, Analyzer, Synthesizer มาทำงานร่วมกัน
                thought = self.agents["thinker"].process(task)
                analysis = self.agents["analyzer"].process(thought['thought'])
                synthesis = self.agents["synthesizer"].process(analysis['analysis'])
                new_strategy = f"New Strategy Developed: {synthesis['summary']}"
                self.memory.add_long_term(f"New_Strategy_{time.time()}", new_strategy)
                print(new_strategy)

            print(f"--- Evolutionary Learning Task '{task[:50]}' Completed ---")
            time.sleep(1) # จำลองเวลาในการประมวลผล

    def run_system(self, user_input):
        route = self._determine_route(user_input)
        if route == "real_time":
            response = self.real_time_cognitive_processing(user_input)
            print(f"\nFinal Real-time Output: {response}\n")
        elif route == "evolutionary":
            print(f"\n--- Enqueuing Evolutionary Task: '{user_input}' ---")
            self.evolution_queue.append(user_input)
            print("Evolutionary task added to queue. Processing will occur in background.")
            print("Please wait for background learning to complete or provide another real-time input.\n")

# --- การติดตั้งและรันระบบ ---
if __name__ == "__main__":
    nexus = GPTNexusCore()

    # เริ่มต้นเส้นทาง Evolutionary Learning ใน Background Thread
    evolution_thread = threading.Thread(target=nexus.continuous_evolutionary_learning, daemon=True)
    evolution_thread.start()
    print("Evolutionary Learning thread started in background.")

    # จำลองการใช้งาน Real-time
    print("\nWelcome to TharPanya AI! What can I help you with?")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYour command (Real-time or Evolutionary): ")
        if user_input.lower() == 'exit':
            print("Exiting TharPanya AI. Goodbye!")
            break
        nexus.run_system(user_input)

        # ตัวอย่างการส่งงาน Evolutionary Task ไปเอง (นอกเหนือจากที่ตรวจจับจาก user_input)
        if "hello" in user_input.lower():
             nexus.evolution_queue.append("Perform a knowledge review based on recent 'hello' interactions.")