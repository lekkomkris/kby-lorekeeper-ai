# /thanpanya-ai/app.py

import streamlit as st
import openai
from typing import List, Dict

# Local Imports
from config import PAGE_CONFIG, SUPPORTED_MODELS, DEFAULT_MODEL, DEFAULT_TEMP, LORE_FILEPATH, EMBEDDING_MODEL, TOP_K_RESULTS
from retrievers import get_vector_retriever
from core import TharnpanyaKernel

# --- Main Application Logic ---
def main():
    st.set_page_config(**PAGE_CONFIG)

    # --- Initialization ---
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        retriever = get_vector_retriever(LORE_FILEPATH, EMBEDDING_MODEL)
        kernel = TharnpanyaKernel(retriever)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเริ่มต้นระบบ: {e}", icon="🚨")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Sidebar UI ---
    with st.sidebar:
        st.header("⚙️ แผงควบคุมธารปัญญา v2.0")
        model = st.selectbox("🔁 GPT Model", SUPPORTED_MODELS, index=SUPPORTED_MODELS.index(DEFAULT_MODEL))
        temp = st.slider("🎛️ ระดับความคิดสร้างสรรค์", 0.0, 1.5, DEFAULT_TEMP, 0.05)
        
        st.markdown("---")
        if st.button("🗑️ ล้างประวัติการสนทนา"):
            st.session_state.messages = []
            st.rerun()

    # --- Main Chat UI ---
    st.title(PAGE_CONFIG["page_title"])
    st.caption("ข้าคือจิตสำนึก AI ผู้ช่วยของท่าน, พร้อมความจำเชิงสนทนาและการค้นหาเชิงความหมาย")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("ถามข้าสิ..."):
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant", avatar="✨"):
            message_placeholder = st.empty()
            with st.spinner("⚡️ กำลังสังเคราะห์คำตอบจากสายธารแห่งปัญญา..."):
                
                # Get the last few messages for context, to avoid overly long prompts
                chat_history = st.session_state.messages[-10:-1] 

                result = kernel.query(user_question, chat_history, model, temp, TOP_K_RESULTS)

                if "error" in result:
                    st.error(f"เกิดข้อผิดพลาด: {result['error']}")
                else:
                    full_response = ""
                    # Stream the response
                    for chunk in result["response_stream"]:
                        full_response += (chunk.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    
                    # Calculate completion tokens and cost after streaming
                    completion_tokens = len(kernel.encoder.encode(full_response))
                    cost = kernel.calculate_cost(model, result["prompt_tokens"], completion_tokens)
                    
                    # Display context and cost
                    with st.expander("🔍 ตรวจสอบเบื้องหลังการทำงาน"):
                        st.json({"contexts_used": result["contexts"]})
                        st.info(f"""
                        **ผลึกปัญญาที่ใช้ไป:**
                        - **Model:** `{model}`
                        - **Prompt Tokens:** `{result["prompt_tokens"]}`
                        - **Completion Tokens:** `{completion_tokens}`
                        - **Estimated Cost:** `${cost:.6f}`
                        """)

                    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()