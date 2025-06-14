import unittest
from lorekeeper import find_answer_in_lore, load_and_process_lore

class TestLorekeeperAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load lore data once for all tests."""
        cls.processed_lore = load_and_process_lore("kby_lore.txt")
        if not cls.processed_lore:
            raise ValueError("Could not load lore file for testing.")

    def test_find_exact_match_qualia(self):
        """Test finding a known entry about Qualia."""
        question = "Qualia คืออะไร"
        expected_answer_part = "คือมิติของประสบการณ์รับรู้ที่ใช้ในการสื่อสารกับ SOA"
        actual_answer = find_answer_in_lore(question, self.processed_lore)
        self.assertIn(expected_answer_part, actual_answer)

    def test_find_fuzzy_match_qualia(self):
        """Test finding a known entry with a typo."""
        question = "Qalia คืออะไร"
        expected_answer_part = "คือมิติของประสบการณ์รับรู้ที่ใช้ในการสื่อสารกับ SOA"
        actual_answer = find_answer_in_lore(question, self.processed_lore)
        self.assertIn(expected_answer_part, actual_answer)

    def test_no_match_found(self):
        """Test with a question that has no match."""
        question = "Metamind OS คืออะไร"
        expected_answer = "ขออภัย ข้ายังไม่พบข้อมูลที่เกี่ยวข้องในตำนาน KBY"
        actual_answer = find_answer_in_lore(question, self.processed_lore)
        self.assertEqual(expected_answer, actual_answer)
    
    def test_empty_question(self):
        """Test with an empty question string."""
        question = ""
        expected_answer = "ขออภัย ข้ายังไม่พบข้อมูลที่เกี่ยวข้องในตำนาน KBY"
        actual_answer = find_answer_in_lore(question, self.processed_lore)
        self.assertEqual(expected_answer, actual_answer)

if __name__ == '__main__':
    unittest.main()