# /thanpanya-ai/core.py

import openai
import tiktoken
from typing import List, Dict, Any

from retrievers import VectorRetriever
from config import SYSTEM_PROMPT, TOKEN_COSTS

class TharnpanyaKernel:
    """
    The evolved core of Tharnpanya AI. Now with conversational memory and cost tracking.
    """
    def __init__(self, retriever: VectorRetriever):
        self.retriever = retriever
        # Initialize token encoder for cost calculation
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def _build_prompt(self, question: str, chat_history: List[Dict], contexts: List[str]) -> str:
        """Constructs the final prompt for the LLM."""
        context_str = "\n\n".join(contexts)
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        
        prompt = f"""{SYSTEM_PROMPT}

        --- ประวัติการสนทนาก่อนหน้า ---
        {history_str}

        --- Context ที่เกี่ยวข้องจากคลังปัญญา ---
        {context_str}

        --- คำถามล่าสุดจากผู้ใช้ ---
        user: {question}

        --- คำตอบจาก ธารปัญญา AI ---
        assistant:"""
        return prompt

    def query(self, question: str, chat_history: List[Dict], model: str, temp: float, top_k: int) -> Dict[str, Any]:
        """
        The main query function. It now orchestrates retrieval, prompt construction,
        API call, and cost calculation.
        """
        # 1. Retrieve relevant contexts
        contexts = self.retriever.retrieve(question, top_k=top_k)

        # 2. Build the full prompt
        full_prompt = self._build_prompt(question, chat_history, contexts)

        # 3. Call OpenAI API
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *chat_history,
                    {"role": "user", "content": f"Based on the following context, answer my question.\n\nContext:\n{'/n'.join(contexts)}\n\nQuestion: {question}"}
                ],
                temperature=temp,
                stream=True # We will use streaming response
            )
            
            # 4. Prepare results
            prompt_tokens = len(self.encoder.encode(full_prompt))
            
            return {
                "response_stream": response,
                "contexts": contexts,
                "prompt_tokens": prompt_tokens,
            }

        except Exception as e:
            return {"error": str(e)}

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculates the estimated cost of an API call."""
        cost_info = TOKEN_COSTS.get(model, TOKEN_COSTS["gpt-4o"]) # Default to gpt-4o if model not found
        cost = (prompt_tokens * cost_info["prompt"]) + (completion_tokens * cost_info["completion"])
        return cost