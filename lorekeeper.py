from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
import openai

# === โหลด BERT Model ===
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def load_and_process_lore(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def find_top_k_contexts(question: str, lore: List[str], k=3) -> List[str]:
    question_emb = embedder.encode(question, convert_to_tensor=True)
    lore_embs = embedder.encode(lore, convert_to_tensor=True)
    sim_scores = util.pytorch_cos_sim(question_emb, lore_embs)[0]
    top_k_idx = sim_scores.topk(k=k).indices
    return [lore[i] for i in top_k_idx]

def gpt_summarize(question: str, context: str, model="gpt-4", temperature=0.4) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "คุณคือผู้ช่วยอัจฉริยะที่ตอบคำถามจากคลังความรู้ KBY อย่างแม่นยำ"},
            {"role": "user", "content": f"บริบท:\n{context}\n\nคำถาม:\n{question}"}
        ]
    )
    return response["choices"][0]["message"]["content"]

def advanced_hybrid_answer(question: str, lore: List[str], model="gpt-4", temperature=0.4) -> Dict:
    contexts = find_top_k_contexts(question, lore, k=3)
    joined_context = "\n".join(contexts)
    answer = gpt_summarize(question, joined_context, model=model, temperature=temperature)
    return {
        "answer": answer,
        "contexts": contexts,
        "model_used": model,
        "raw_context": joined_context
    }
