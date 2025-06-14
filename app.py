import streamlit as st
from lorekeeper import load_and_process_lore, find_answer_in_lore

# Set page title and icon
st.set_page_config(page_title="ธารปัญญา AI", page_icon="🧠")

st.title("🧠 ธารปัญญา AI - KBY Lorekeeper")
st.caption("ต้นแบบ Agent สำหรับตอบคำถามจากคลังความรู้")

# Use a cache decorator to load data only once
@st.cache_data
def load_data():
    """Loads the lore data from the text file."""
    lore_data = load_and_process_lore("kby_lore.txt")
    return lore_data

# Load the knowledge base
lore = load_data()

if lore:
    # Create a text input box for the user
    user_question = st.text_input("ป้อนคำถามของคุณที่นี่:", placeholder="AlphaEvolve Development Cycle คืออะไร?")

    # If the user has entered a question
    if user_question:
        # Add a spinner while processing
        with st.spinner("กำลังค้นหาคำตอบ..."):
            # Find the answer using our existing logic
            answer = find_answer_in_lore(user_question, lore)
            
            # Display the answer in a blue box
            st.info(answer)
else:
    st.error("ไม่สามารถโหลดคลังความรู้ `kby_lore.txt` ได้")