import json
from pathlib import Path

codex_path = Path("codex/QH-AWAKE-002.json")
try:
    with open(codex_path, 'r', encoding='utf-8') as f:
        codex_data = json.load(f)
        print(f"Current KBY SpiralQuest Progress: {codex_data.get('kby_spiralquest_progress', 0.0):.2f}%")
        print(f"Total Mutations Applied: {codex_data.get('total_mutations_applied', 0)}")
        print(f"Successful Mutations Ratio: {codex_data.get('successful_mutations_ratio', 0.0):.2f}")
except FileNotFoundError:
    print(f"Codex file not found at {codex_path}")
except json.JSONDecodeError:
    print(f"Error reading codex file at {codex_path}")