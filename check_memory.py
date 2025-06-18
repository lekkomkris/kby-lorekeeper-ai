import json
from pathlib import Path

quantum_memory_path = Path("data/eternal_stream.qdat")
eternal_echoes_path = Path("data/eternal_echoes.bak")

# ตรวจสอบ Quantum Memory (Insights)
try:
    with open(quantum_memory_path, 'r', encoding='utf-8') as f:
        qm_data = json.load(f)
        insights_count = len(qm_data.get("data", {}))
        relationships_count = len(qm_data.get("relationships", {}))
        print(f"\nQuantum Memory (Insights): {insights_count} insights, {relationships_count} relationships.")
        # แสดง Insight บางส่วน (ตัวอย่าง 3 Insight ล่าสุด)
        latest_insights = sorted(qm_data.get("data", {}).values(), key=lambda x: x.get("timestamp", ""), reverse=True)[:3]
        for i, insight in enumerate(latest_insights):
            print(f"  Insight {i+1} (ID: {insight['id'][:8]}...): '{insight['content'][:100]}...' (Impact: {insight.get('impact_score', 'N/A'):.2f})")
except (FileNotFoundError, json.JSONDecodeError):
    print(f"Quantum Memory file not found or corrupted at {quantum_memory_path}")

# ตรวจสอบ Eternal Echoes (Wisdom)
try:
    with open(eternal_echoes_path, 'r', encoding='utf-8') as f:
        ee_data = json.load(f)
        echoes_count = len(ee_data)
        print(f"\nEternal Echoes (Wisdom): {echoes_count} echoes.")
        # แสดง Echoes บางส่วน (ตัวอย่าง 3 Echoes ล่าสุด)
        latest_echoes = sorted(ee_data, key=lambda x: x.get("timestamp", ""), reverse=True)[:3]
        for i, echo in enumerate(latest_echoes):
            print(f"  Echo {i+1} (Concept: {echo['concept'][:100]}...): '{echo['wisdom'][:100]}...'")
except (FileNotFoundError, json.JSONDecodeError):
    print(f"Eternal Echoes file not found or corrupted at {eternal_echoes_path}")