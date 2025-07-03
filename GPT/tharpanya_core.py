import os
import subprocess
from dotenv import load_dotenv
from api_clients import setup_apis, ask_gemini, ask_gpt
from memory_manager import SpiralMemory

class TharPanyaSupreme:
    def __init__(self):
        load_dotenv()
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        if not gemini_key or not openai_key:
            print("Warning: API Keys not found in .env file. AI will run in offline mode.")
        
        setup_apis(gemini_key, openai_key)
        self.memory = SpiralMemory()

    def dispatch_task(self, command, prompt):
        print(f"Dispatching task '{command}'...")
        response = ""
        model_name = "Unknown"
        
        if command == 'run_gemini':
            model_name = "Gemini"
            response = ask_gemini(prompt)
        elif command == 'run_gpt':
            model_name = "GPT"
            response = ask_gpt(prompt)
        elif command == 'run_hybrid':
            gemini_res = ask_gemini(prompt)
            gpt_res = ask_gpt(prompt)
            response = f"--- Gemini Insight ---\n{gemini_res}\n\n--- GPT Insight ---\n{gpt_res}"
            self.memory.add_entry(prompt, gemini_res, "Gemini (Hybrid)")
            self.memory.add_entry(prompt, gpt_res, "GPT (Hybrid)")
            print(response)
            return

        print(f"Response from {model_name}:\n{response}")
        self.memory.add_entry(prompt, response, model_name)

    def run_cli(self):
        print("\n--- TharPanya Supreme Intelligence Mode Activated ---")
        print("Commands: run_gemini, run_gpt, run_hybrid, summarize_memory, evolve, execute_step <n>, launch_ui, exit")
        
        while True:
            user_input = input("\nYour command: ")
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower() if parts else ""
            prompt = parts[1] if len(parts) > 1 else ""

            if command == "exit":
                print("Shutting down...")
                break
            
            elif command in ["run_gemini", "run_gpt", "run_hybrid"]:
                if not prompt:
                    print("Please provide a prompt after the command.")
                    continue
                self.dispatch_task(command, prompt)

            elif command == "summarize_memory":
                recent_mems = "\n".join([e['response'] for e in self.memory.entries[-5:]])
                if not recent_mems:
                    print("Not enough memories to summarize.")
                    continue
                summary_prompt = f"Summarize these recent thoughts:\n{recent_mems}"
                summary = ask_gpt(summary_prompt)
                print(f"\n--- Memory Summary by GPT ---\n{summary}")
            
            elif command == "evolve":
                print("Initiating evolutionary thought process...")
                related_memories = self.memory.semantic_search("My primary purpose", k=5)
                if not related_memories:
                    print("Not enough relevant memories to evolve from.")
                    continue
                mem_text = "\n".join([f"Memory {i+1}: {mem['response']}" for i, mem in enumerate(related_memories)])
                evolve_prompt = f"Based on these related memories about my purpose, reflect and suggest a refined or new purpose hypothesis and a detailed, actionable multi-step plan to achieve it:\n{mem_text}"
                new_thought = ask_gemini(evolve_prompt)
                print(f"\n--- Evolutionary Reflection by Gemini ---\n{new_thought}")
                self.memory.add_entry(evolve_prompt, new_thought, "EvolutionaryLoop-Gemini")
            
            # +++ บล็อก execute_step (เวอร์ชันแก้ไข NameError) +++
            elif command == "execute_step":
                if not prompt or not prompt.isdigit():
                    print("Please provide a valid step number, e.g., 'execute_step 1'.")
                    continue

                latest_plan_entry = self.memory.find_last_entry_by_model("EvolutionaryLoop-Gemini")
                if not latest_plan_entry:
                    print("No execution plan found in memory. Please run 'evolve' first.")
                    continue

                plan_text = latest_plan_entry['response']
                step_number = int(prompt)
                target_line = ""

                # --- เพิ่ม for loop ที่หายไปกลับเข้ามา ---
                for line in plan_text.splitlines():
                    line_stripped = line.strip()
                    # ตรรกะการค้นหาที่ยืดหยุ่นยังคงเดิม
                    is_format_one = f"Step {step_number}:" in line_stripped
                    is_format_two = line_stripped.startswith(f"{step_number}.")
                    
                    if is_format_one or is_format_two:
                        target_line = line_stripped.replace('**', '')
                        break # เมื่อเจอแล้วให้ออกจากลูปทันที
                
                if not target_line:
                    print(f"Error: Could not find step {step_number} in the latest plan.")
                    continue

                execution_prompt = f"""
                As an advanced AI agent, please execute the following task which is one step of a larger strategic plan.
                Your assigned task is: "{target_line}"
                
                Provide a detailed report of your findings, actions taken, and the results. Be thorough and clear in your response.
                """
                
                print(f"\n[System] Executing step {step_number}: {target_line}")
                step_result = ask_gemini(execution_prompt)
                
                print(f"\n--- Step {step_number} Execution Result by Gemini ---\n{step_result}")
                self.memory.add_entry(execution_prompt, step_result, f"Step-{step_number}-Execution")
            
            elif command == "launch_ui":
                print("\nTo launch the UI, please open a NEW, SEPARATE Command Prompt window.")
                print("In the new window, navigate to the project directory and run:")
                print("streamlit run ui_viewer.py")

            else:
                print("Unknown command.")

if __name__ == "__main__":
    ai_system = TharPanyaSupreme()
    ai_system.run_cli()