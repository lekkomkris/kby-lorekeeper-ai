import timeit

setup_code = '''
from lorekeeper import find_answer_in_lore, load_and_process_lore
processed_lore = load_and_process_lore("kby_lore.txt")
question = "KBY SpiralQuest คืออะไร?"
'''

statement_to_test = '''
find_answer_in_lore(question, processed_lore)
'''

print("กำลังวัดประสิทธิภาพของโค้ด...")
number_of_runs = 10000
total_time = timeit.timeit(stmt=statement_to_test, setup=setup_code, number=number_of_runs)
average_time_microseconds = (total_time / number_of_runs) * 1_000_000

print("\n--- ผลการประเมินประสิทธิภาพ ---")
print(f"จำนวนการทดสอบ: {number_of_runs:,} ครั้ง")
print(f"เวลาเฉลี่ยต่อการทำงานหนึ่งครั้ง: {average_time_microseconds:.4f} ไมโครวินาที (µs)")
print("--------------------------------")