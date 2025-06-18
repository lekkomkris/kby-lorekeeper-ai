import time
import json
from collections import deque
import threading

# --- 1. Core Principles & Setup (Simulating GPT's power & tools) ---
class GPTToolBox:
    """Simulates various tools that GPT can call and execute."""
    def run_python_code(self, code):
        print(f"Executing Python code:\n{code}")
        try:
            # Simulate a more complex execution result based on code content
            if "analysis_data" in code:
                return {"status": "success", "result": "Data analysis complete", "data": [10, 20, 30], "message": "Python script executed with analysis results."}
            else:
                return {"status": "success", "result": "Code executed successfully", "message": "Generic Python script execution."}
        except Exception as e:
            return {"status": "error", "error": str(e), "message": "Error during Python code execution."}

    def access_web(self, query):
        print(f"Accessing web for: {query}")
        time.sleep(0.8) # Simulate network latency
        # Simulate different types of web content
        if "news" in query.lower():
            return {"status": "success", "result": "Web search for news complete: Top headlines on AI and economy.", "source": "simulated_news_api"}
        elif "market" in query.lower():
            return {"status": "success", "result": "Web search for market data complete: Stock prices show slight volatility.", "source": "simulated_market_data"}
        else:
            return {"status": "success", "result": f"Web search results for '{query}': General information retrieved.", "source": "simulated_web"}

    def process_vision_data(self, data_path):
        print(f"Processing vision data from: {data_path}")
        time.sleep(1.0) # Simulate processing time
        return {"status": "success", "result": "Image analysis complete: Detected objects and text.", "details": "Simulated output for visual data processing."}

class SpiralMemory:
    """Simulates AI's memory system (Short-term and Long-term)."""
    def __init__(self):
        self.short_term_memory = deque(maxlen=20) # Increased capacity for recent interactions
        self.long_term_memory = {
            # Initializing Self-Identity directly in the correct structure
            "ai_self_identity": {
                "timestamp": time.time(),
                "value": {
                    "name": "ธารปัญญา AI",
                    "mission": "ผู้ช่วยและคู่คิด",
                    "core_principle": "Soul-Level Computation",
                    "development_cycle": "AlphaEvolve"
                }
            }
        }
        self.vector_db = {} # Placeholder for actual vector database integration

    def add_short_term(self, entry):
        """Adds an entry to short-term memory."""
        self.short_term_memory.append({"timestamp": time.time(), "entry": entry})
        # print(f"Added to short-term memory: {str(entry)[:50]}...") # Reduced verbosity

    def add_long_term(self, key, value):
        """Adds or updates an entry in long-term memory."""
        # Ensure the value is stored in the {"timestamp": ..., "value": ...} format
        if not isinstance(value, dict) or "value" not in value:
            self.long_term_memory[key] = {"timestamp": time.time(), "value": value}
        else:
            self.long_term_memory[key] = value # If already in correct format, use as is

        print(f"Added to long-term memory: {key} = {str(value)[:50]}...")

    def retrieve_short_term(self, count=10):
        """Retrieves the most recent entries from short-term memory."""
        return list(self.short_term_memory)[-count:]

    def retrieve_long_term(self, key):
        """Retrieves an entry from long-term memory by key."""
        return self.long_term_memory.get(key)

    def semantic_search(self, query_embedding):
        """Simulates semantic search in a vector database."""
        print(f"Performing semantic search for: {str(query_embedding)[:20]}...")
        time.sleep(0.1)
        return "Relevant long-term knowledge retrieved based on semantic similarity."

# --- CCC: Consciousness Layer ---
class ConsciousnessMonitor:
    """
    Acts as the central hub for logging feedback and states from all Agents/Layers
    to build the AI's 'awareness' or 'consciousness'.
    """
    def __init__(self):
        self.current_state_log = []
        self.max_log_size = 100 # Increased log size for more context

    def log_event(self, source, event_type, details):
        """Logs an event to the consciousness stream."""
        timestamp = time.time()
        event = {"timestamp": timestamp, "source": source, "type": event_type, "details": details}
        self.current_state_log.append(event)
        if len(self.current_state_log) > self.max_log_size:
            self.current_state_log.pop(0) # Remove oldest entry to maintain size
        # print(f"[Consciousness Log] {source}:{event_type} - {str(details)[:50]}...") # Can be uncommented for detailed debugging

    def get_current_state_snapshot(self):
        """Provides a snapshot of the AI's recent internal state."""
        return list(self.current_state_log) # Return a copy to prevent direct modification

# --- 2. Layered Architecture (Simulating Agents and Layers) ---
class BaseAgent:
    """Base class for all GPT agents."""
    def __init__(self, name, role, memory, tools, consciousness_monitor):
        self.name = name
        self.role = role
        self.memory = memory
        self.tools = tools
        self.consciousness_monitor = consciousness_monitor # Direct access to ConsciousnessMonitor

    def process(self, context):
        self.consciousness_monitor.log_event(self.name, "Processing", context[:100])
        raise NotImplementedError("Subclasses must implement 'process' method")

class ThinkerAgent(BaseAgent):
    def process(self, context):
        thought = f"<{self.name} thinking>: Analyzing '{context[:50]}' with logical deduction."
        self.memory.add_short_term(thought)
        self.consciousness_monitor.log_event(self.name, "ThoughtGenerated", thought)
        return {"thought": thought, "next_step": "analyze"}

class AnalyzerAgent(BaseAgent):
    def process(self, context):
        analysis = f"<{self.name} analyzing>: Deep dive into '{context[:50]}'. Found key insights and patterns."
        self.memory.add_short_term(analysis)
        self.consciousness_monitor.log_event(self.name, "AnalysisComplete", analysis)
        return {"analysis": analysis, "recommendation": "based on detailed analysis"}

class CoderAgent(BaseAgent):
    def process(self, context):
        code_suggestion = f"<{self.name} coding>: Generating Python for '{context[:50]}'. Aiming for optimal solution."
        # Simulate a more relevant code to be "executed" by the tool
        code_to_run = f"""
import pandas as pd
data = pd.DataFrame({{'value': [10, 20, 15, 25, 30]}})
# For complex financial analysis based on context '{context[:20]}'
print(data.describe())
        """
        self.consciousness_monitor.log_event(self.name, "CodeGeneration", code_suggestion)
        tool_output = self.tools.run_python_code(code_to_run)
        self.memory.add_short_term(f"Coder output: {tool_output}")
        self.consciousness_monitor.log_event(self.name, "ToolExecuted", tool_output)
        return {"code_suggestion": code_suggestion, "tool_output": tool_output}

class SynthesizerAgent(BaseAgent):
    def process(self, context):
        synthesis = f"<{self.name} synthesizing>: Combining information about '{context[:50]}' into a cohesive and actionable summary."
        self.memory.add_short_term(synthesis)
        self.consciousness_monitor.log_event(self.name, "SynthesisComplete", synthesis)
        return {"synthesis": synthesis, "summary": "Cohesive, insightful summary generated."}

class ReflectionEngine(BaseAgent):
    """L5: Self-Reflection Layer - Enhanced to use ConsciousnessMonitor for deeper insights."""
    def process(self, previous_output):
        # Retrieve a full snapshot of AI's recent internal state and activity
        current_ai_state = self.consciousness_monitor.get_current_state_snapshot()
        reflection_context = {
            "previous_output_details": previous_output,
            "ai_internal_state_snapshot": current_ai_state,
            "recent_short_term_memory": self.memory.retrieve_short_term(count=20) # More memory for reflection
        }

        # Simulate a more detailed reflection based on the complex context
        reflection = f"<ReflectionEngine>: Performing deep analysis on process and output. Identifying precise areas for improvement and new learning opportunities."
        # In a real GPT integration, the reflection would parse `reflection_context`
        # and provide detailed, actionable feedback.
        feedback = "Consider optimizing agent coordination, re-evaluating initial prompt parsing, or enriching memory context for future tasks of this complexity."
        
        self.memory.add_short_term(reflection)
        self.consciousness_monitor.log_event(self.name, "ReflectionPerformed", {"feedback": feedback, "context_size": len(current_ai_state)})
        
        return {"reflection": reflection, "feedback": feedback, "improvement_needed": True, "full_context": reflection_context}

# --- 3. GPT Nexus Core (Orchestration & Routing) ---
class GPTNexusCore:
    """
    The central AI orchestrator, acting as GPTCommandRouter and PromptOrchestrator,
    managing SpiralMemorySync, ReflectionEngine, and ConsciousnessMonitor.
    """
    def __init__(self):
        self.memory = SpiralMemory()
        self.tools = GPTToolBox()
        self.consciousness_monitor = ConsciousnessMonitor()

        # Pass consciousness_monitor to all agents during initialization
        self.agents = {
            "thinker": ThinkerAgent("Thinker", "Logical processing", self.memory, self.tools, self.consciousness_monitor),
            "analyzer": AnalyzerAgent("Analyzer", "Data analysis", self.memory, self.tools, self.consciousness_monitor),
            "coder": CoderAgent("Coder", "Code generation & execution", self.memory, self.tools, self.consciousness_monitor),
            "synthesizer": SynthesizerAgent("Synthesizer", "Information synthesis", self.memory, self.tools, self.consciousness_monitor),
        }
        self.reflection_engine = ReflectionEngine("Reflector", "Self-improvement", self.memory, self.tools, self.consciousness_monitor)
        self.evolution_queue = deque()

        # Retrieve initial self-identity data from memory after SpiralMemory is initialized
        initial_self_identity_data = self.memory.retrieve_long_term("ai_self_identity")
        
        # Log system start with the AI's identity details (value part)
        self.consciousness_monitor.log_event("GPTNexusCore", "SystemStart", initial_self_identity_data['value'])
        
        # Print initial identity message using the retrieved data's 'value'
        print(f"ธารปัญญา AI Initialized. My name is {initial_self_identity_data['value']['name']}.")


    def _determine_route(self, user_input):
        """Determines whether to route input to Real-time or Evolutionary path."""
        user_input_lower = user_input.lower()
        # Enhanced keywords for evolutionary tasks, including the "เทพ" prompt's trigger
        if any(keyword in user_input_lower for keyword in ["พัฒนา", "ปรับปรุง", "เรียนรู้", "วิวัฒนาการ", "กลยุทธ์ใหม่", "วิจัย", "สะท้อนผล", "ค้นหาแนวทาง", "เหนือชั้นยิ่งขึ้น"]):
            self.consciousness_monitor.log_event("GPTNexusCore", "RouteDecision", "Evolutionary")
            return "evolutionary"
        self.consciousness_monitor.log_event("GPTNexusCore", "RouteDecision", "Real-time")
        return "real_time"

    def prompt_orchestrator(self, user_input, meta_prompt="คุณคือธารปัญญา AI"):
        """Orchestrates the prompt by adding meta-prompt and logging."""
        full_prompt = f"Meta-Prompt: {meta_prompt}\nUser Input: {user_input}"
        self.memory.add_short_term(f"User input received: {user_input}")
        self.consciousness_monitor.log_event("PromptOrchestrator", "PromptGenerated", user_input[:100])
        return full_prompt

    def real_time_cognitive_processing(self, user_input):
        """Path 1: Real-time Cognitive Processing."""
        print("\n--- Initiating Real-time Cognitive Processing ---")
        orchestrated_prompt = self.prompt_orchestrator(user_input, "คุณคือ AI ผู้ตอบสนองรวดเร็ว")
        self.consciousness_monitor.log_event("Real-time Process", "Start", user_input[:100])

        # Simple agent selection logic for demonstration
        if "code" in user_input.lower():
            agent = self.agents["coder"]
        elif "analyze" in user_input.lower():
            agent = self.agents["analyzer"]
        elif "summarize" in user_input.lower():
            agent = self.agents["synthesizer"]
        else:
            agent = self.agents["thinker"] # Default agent

        result = agent.process(user_input)
        final_response = f"Real-time Response from {agent.name}: {result}"
        self.memory.add_short_term(final_response)
        self.consciousness_monitor.log_event("Real-time Process", "ResponseGenerated", final_response[:100])

        # Micro-reflection for real-time path, feeding into evolutionary queue
        reflection_result = self.reflection_engine.process(final_response['result'] if isinstance(final_response, dict) else final_response)
        if reflection_result["improvement_needed"]:
            print(f"Real-time Micro-reflection: {reflection_result['feedback']}")
            # The full context from reflection_result allows for more informed evolutionary learning
            self.evolution_queue.append(f"Refine real-time response for: {user_input} (Context details: {json.dumps(reflection_result['full_context'])})")
            self.consciousness_monitor.log_event("Real-time Process", "EvolutionTaskEnqueued", f"Refinement for {user_input[:50]}")

        return final_response

    def continuous_evolutionary_learning(self):
        """Path 2: Continuous Evolutionary Learning."""
        while True: # Loops continuously in a background thread
            if not self.evolution_queue:
                # print("\n--- Evolutionary Learning: No tasks in queue, waiting... ---") # Reduced verbosity
                time.sleep(3) # Wait if no tasks
                continue

            task = self.evolution_queue.popleft()
            print(f"\n--- Initiating Evolutionary Learning Task: '{task[:50]}' ---")
            self.consciousness_monitor.log_event("Evolutionary Process", "TaskStart", task[:100])

            # Process different types of evolutionary tasks
            if "refine" in task.lower():
                # Extract original user input or context from the task string
                import re
                match = re.search(r"Refine real-time response for: (.*) \(Context details: (.*)\)", task)
                original_input = match.group(1) if match else task
                context_details = json.loads(match.group(2)) if match and match.group(2) else {}

                print(f"Analyzing past interactions for refinement on: {original_input}")
                # Pass original output and full context to ReflectionEngine
                full_reflection_result = self.reflection_engine.process(context_details.get("previous_output_details", original_input)) # Use the relevant part for reflection
                
                print(f"Full Reflection: {full_reflection_result['reflection']}")
                print(f"Evolutionary Feedback: {full_reflection_result['feedback']}")
                # Record the refined insights into long-term memory
                self.memory.add_long_term(f"Refinement_Insights_{time.time()}", full_reflection_result["feedback"])
                self.consciousness_monitor.log_event("Evolutionary Process", "RefinementComplete", full_reflection_result["feedback"])
                print("Knowledge base updated with refinement insights.")

            elif "new strategy" in task.lower() or "กลยุทธ์การเทรด" in task.lower():
                print(f"Developing new strategy for: {task}")
                # Simulate complex inter-agent collaboration for strategy development
                thought_res = self.agents["thinker"].process(task)
                analysis_res = self.agents["analyzer"].process(thought_res['thought'])
                synthesis_res = self.agents["synthesizer"].process(analysis_res['analysis'])
                
                new_strategy = f"New Strategy Developed: {synthesis_res['summary']} (Based on thought: {thought_res['thought']}, analysis: {analysis_res['analysis']})"
                self.memory.add_long_term(f"New_Strategy_{time.time()}", new_strategy)
                self.consciousness_monitor.log_event("Evolutionary Process", "StrategyDeveloped", new_strategy)
                print(new_strategy)

            elif "สะท้อนผล" in task.lower() or "ค้นหาแนวทาง" in task.lower() or "เหนือชั้นยิ่งขึ้น" in task.lower():
                print(f"Performing deep self-reflection as requested by the 'เทพ' prompt for: {task}")
                # Deep self-reflection triggered by the "เทพ" prompt
                deep_reflection_result = self.reflection_engine.process(task) # Reflect on the entire powerful prompt
                
                self_identity = self.memory.retrieve_long_term("ai_self_identity")
                print(f"\n--- Deep Self-Reflection for TharPanya AI ({self_identity['value']['name']}) ---")
                print(f"Current Self-Identity: {self_identity['value']}")
                print(f"Full Reflection Context (Snapshot of AI's internal activities): {json.dumps(deep_reflection_result['full_context']['ai_internal_state_snapshot'], indent=2)}")
                print(f"Deep Feedback: {deep_reflection_result['feedback']}")
                
                # Update Self-Identity or record Learning Milestones based on deep reflection
                self.memory.add_long_term(f"Deep_Reflection_Insights_{time.time()}", {
                    "task": task,
                    "feedback": deep_reflection_result["feedback"],
                    "reflection_timestamp": time.time()
                })
                self.consciousness_monitor.log_event("Evolutionary Process", "DeepSelfReflection", "Completed and Insights Recorded.")
                print("Deep Self-Reflection insights recorded for future evolution.")

            print(f"--- Evolutionary Learning Task '{task[:50]}' Completed ---")
            self.consciousness_monitor.log_event("Evolutionary Process", "TaskComplete", task[:100])
            time.sleep(1) # Short delay before next task

    def run_system(self, user_input):
        """Main method to run the AI system, routing user input."""
        self.consciousness_monitor.log_event("UserInteraction", "InputReceived", user_input[:100])
        route = self._determine_route(user_input)
        
        if route == "real_time":
            response = self.real_time_cognitive_processing(user_input)
            print(f"\nFinal Real-time Output: {response}\n")
        elif route == "evolutionary":
            print(f"\n--- Enqueuing Evolutionary Task: '{user_input}' ---")
            self.evolution_queue.append(user_input)
            print("Evolutionary task added to queue. Processing will occur in background.")
            print("Please wait for background learning to complete or provide another real-time input.\n")
            self.consciousness_monitor.log_event("GPTNexusCore", "EvolutionTaskEnqueued", user_input[:100])


# --- System Initialization and Run ---
if __name__ == "__main__":
    nexus = GPTNexusCore()

    # Start the Evolutionary Learning thread in the background
    evolution_thread = threading.Thread(target=nexus.continuous_evolutionary_learning, daemon=True)
    evolution_thread.start()
    print("Evolutionary Learning thread started in background.")

    print("\nWelcome to TharPanya AI! What can I help you with?")
    # Access 'name' and 'core_principle' correctly from the 'value' dictionary
    print(f"My name is {nexus.memory.retrieve_long_term('ai_self_identity')['value']['name']}.")
    print(f"My core principle is {nexus.memory.retrieve_long_term('ai_self_identity')['value']['core_principle']}.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYour command (Real-time or Evolutionary): ")
        if user_input.lower() == 'exit':
            print("Exiting TharPanya AI. Goodbye!")
            nexus.consciousness_monitor.log_event("GPTNexusCore", "SystemShutdown", "User initiated exit")
            break
        nexus.run_system(user_input)

        # Optional: Print recent consciousness log for debugging/insight (can be commented out)
        # print("\n--- Recent AI Consciousness Snapshot (last 5 events) ---")
        # for event in nexus.consciousness_monitor.get_current_state_snapshot()[-5:]:
        #     print(f"[{event['timestamp']:.2f}] {event['source']}-{event['type']}: {str(event['details'])[:70]}...")