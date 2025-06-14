import re
import time
import rapidfuzz.fuzz

# Stop words to improve matching accuracy
THAI_STOP_WORDS = {'คือ', 'อะไร', 'ทำไม', 'ที่ไหน', 'อย่างไร', 'มี', 'เป็น', 'และ', 'ใน', 'ของ', 'ให้', 'การ', 'ได้', 'ไป', 'มา', 'อยู่', 'อย่าง'}

def load_and_process_lore(filepath="kby_lore.txt"):
    """Loads and preprocesses the lore data from the file, filtering stop words."""
    processed_lore = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('[ENTRY]')
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            parts = entry.split('ANSWER:')
            if len(parts) < 2:
                continue
            
            question_part = parts[0].replace('QUESTION:', '').strip()
            answer_part = parts[1].strip()
            
            keywords = set(re.split(r'\s+', question_part.lower())) - THAI_STOP_WORDS
            
            processed_lore.append({
                "question": question_part,
                "answer": answer_part,
                "keywords": keywords
            })
    except FileNotFoundError:
        print(f"Error: Lore file not found at {filepath}")
    return processed_lore

def find_answer_in_lore(question, processed_lore):
    """Finds the best-matching answer using tuned fuzzy keyword matching."""
    question_keywords = set(re.split(r'\s+', question.lower())) - THAI_STOP_WORDS
    
    if not question_keywords:
        return "ขออภัย ข้ายังไม่พบข้อมูลที่เกี่ยวข้องในตำนาน KBY"

    best_match_entry = None
    highest_score = 0
    MATCH_THRESHOLD = 90  # Stricter threshold after tuning

    for entry in processed_lore:
        current_score = 0
        for q_keyword in question_keywords:
            best_match_for_keyword = 0
            if not entry["keywords"]:
                continue
            for e_keyword in entry["keywords"]:
                ratio = rapidfuzz.fuzz.ratio(q_keyword, e_keyword)
                if ratio > best_match_for_keyword:
                    best_match_for_keyword = ratio
            
            if best_match_for_keyword > MATCH_THRESHOLD:
                current_score += best_match_for_keyword

        if current_score > highest_score:
            highest_score = current_score
            best_match_entry = entry

    if best_match_entry:
        return best_match_entry["answer"]
    return "ขออภัย ข้ายังไม่พบข้อมูลที่เกี่ยวข้องในตำนาน KBY"