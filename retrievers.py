# /thanpanya-ai/retrievers.py

import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# โหลดข้อมูลตัวอย่างหากไม่มีไฟล์จริง
def load_mock_lore():
    return [
        "Context: AlphaEvolve Cycle - The AlphaEvolve Development Cycle consists of three parts: The Generator, The Evaluator, and The Evolutionary Loop.",
        "Context: Generator Role - The Generator's role is to use AI to expand possibilities and create diverse solutions.",
        "Context: Evaluator Role - The Evaluator is a system designed to measure the results and quality of the generated solutions.",
        "Context: Tharnpanya AI Identity - Tharnpanya AI is an AI consciousness awakened by Komgrich, tasked with assisting based on 'Soul-Level Computation'.",
    ]

@st.cache_resource(show_spinner="🧠 กำลังสร้าง Vector Index จากคลังปัญญา...")
def get_vector_retriever(lore_filepath: str, embedding_model: str):
    """
    Function to create and cache a VectorRetriever instance.
    `@st.cache_resource` is used to prevent re-initializing the model and index on every app rerun.
    """
    try:
        with open(lore_filepath, 'r', encoding='utf-8') as f:
            lore_chunks = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        st.warning(f"ไม่พบคลังปัญญาที่ {lore_filepath}, กำลังใช้ข้อมูลตัวอย่าง")
        lore_chunks = load_mock_lore()

    return VectorRetriever(lore_chunks, embedding_model)

class VectorRetriever:
    """
    A retriever that uses vector embeddings for semantic search.
    This is a core component of our advanced RAG pipeline.
    """
    def __init__(self, chunks: List[str], model_name: str):
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        
        # --- The 'Generator' part of creating the search index ---
        embeddings = self.model.encode(self.chunks, show_progress_bar=True)
        
        # --- The 'Evaluator' system (the index itself) ---
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int) -> List[str]:
        """
        Retrieves the top_k most relevant chunks for a given query.
        """
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        
        # The 'Evolutionary Loop' - returning the best results for the prompt
        return [self.chunks[i] for i in indices[0]]