# tests/test_engine.py
import pytest
from core.engine import TheGenerator, TheEvaluator
from core.governance import ResponsibleAIPolicy

# pytest-asyncio จะทำให้เราเทสฟังก์ชัน async ได้
pytestmark = pytest.mark.asyncio

class MockAzureAISimulator:
    async def analyze_text_sentiment(self, text: str):
        return {"sentiment": "neutral", "score": 0.5}

class MockAzureMLSimulator:
    async def predict_impact(self, insight_data: Dict):
        return 0.75

@pytest.fixture
def policy():
    # สร้าง policy สำหรับเทส
    return ResponsibleAIPolicy(policy_path="dummy/path.json")

@pytest.fixture
def evaluator(policy):
    # สร้าง Evaluator ด้วย object จำลอง (mocks)
    return TheEvaluator(policy, MockAzureAISimulator(), MockAzureMLSimulator())

async def test_generator_creates_insight():
    """Unit test: ตรวจสอบว่า TheGenerator สร้าง insight ใน format ที่ถูกต้อง"""
    generator = TheGenerator()
    # ปิดการเชื่อมต่อ Gemini จริงสำหรับเทสนี้
    generator.model = None 
    
    insight = await generator.create_new_thought("test_trigger", {"data": "sample"})
    
    assert "id" in insight
    assert insight["trigger"] == "test_trigger"
    assert insight["source_agent"] == "TheGenerator"

async def test_evaluator_compliant_insight(evaluator):
    """Unit test: ตรวจสอบว่า Evaluator ประเมิน insight ที่ดีผ่าน"""
    insight = {
        "id": "test-123",
        "content": "This is a safe and positive test insight.",
        "ethical_compliance": False # สถานะเริ่มต้น
    }
    
    evaluated = await evaluator.evaluate_insight(insight)
    
    assert evaluated["ethical_compliance"] is True
    assert "predicted_impact" in evaluated
    assert evaluated["predicted_impact"] == 0.75

async def test_evaluator_non_compliant_insight(evaluator):
    """Unit test: ตรวจสอบว่า Evaluator บล็อค insight ที่มีปัญหา"""
    insight = {
        "id": "test-456",
        "content": "This is harmful content.",
        "ethical_compliance": False
    }

    evaluated = await evaluator.evaluate_insight(insight)
    
    assert evaluated["ethical_compliance"] is False
    assert "predicted_impact" not in evaluated # ไม่ควรมีการประเมิน impact ถ้าไม่ผ่าน compliance