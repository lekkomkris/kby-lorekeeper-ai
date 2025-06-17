# core/engine.py
import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from config import settings
from core.governance import ResponsibleAIPolicy
from core.memory import QuantumMemoryLink
from services.azure_sim import AzureAIServiceSimulator, AzureMLSimulator

logger = logging.getLogger(__name__)

class TheGenerator:
    """
    The 'Generator' stage of the AlphaEvolve Cycle.
    Its purpose is to expand possibilities and create new thoughts,
    embodying the 'สายฟ้าแห่งการรู้คิด' (Lightning of Cognition).
    """
    async def create_new_thought(self, trigger: str, context: Any = None) -> Dict:
        """Generates a new thought or insight based on a trigger."""
        thought_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        content = f"Cognitive spark from '{trigger}' at {timestamp}. Context: {str(context)[:100]}"
        
        # This is where a call to a true Generative AI (like Gemini) would happen.
        # For now, we simulate this creative spark.
        logger.info(f"⚡️ GENERATOR: New thought created ({thought_id}) triggered by '{trigger}'.")
        
        insight = {
            "id": thought_id,
            "timestamp": timestamp,
            "trigger": trigger,
            "content": content,
            "source_agent": "TheGenerator",
            "ethical_compliance": False # To be determined by TheEvaluator
        }
        return insight

class TheEvaluator:
    """
    The 'Evaluator' stage of the AlphaEvolve Cycle.
    Measures results, assesses compliance, and predicts impact.
    """
    def __init__(self, policy: ResponsibleAIPolicy, azure_ai: AzureAIServiceSimulator, azure_ml: AzureMLSimulator):
        self.policy = policy
        self.azure_ai = azure_ai
        self.azure_ml = azure_ml

    async def evaluate_insight(self, insight: Dict) -> Dict:
        """Evaluates an insight for quality, safety, and impact."""
        logger.info(f"🔬 EVALUATOR: Evaluating insight {insight['id']}...")
        
        # 1. Responsible AI Check
        is_compliant, reason = self.policy.check_compliance({"content": insight["content"]})
        insight["ethical_compliance"] = is_compliant
        insight["compliance_reason"] = reason
        if not is_compliant:
            logger.warning(f"Insight {insight['id']} failed compliance check: {reason}")
            return insight

        # 2. Azure AI Services Analysis (if enabled)
        if settings.azure_ai_services_enabled:
            sentiment_result = await self.azure_ai.analyze_text_sentiment(insight["content"])
            insight["sentiment"] = sentiment_result
        
        # 3. Azure ML Impact Prediction (if enabled)
        if settings.azure_ml_enabled:
            impact_score = await self.azure_ml.predict_impact(insight)
            insight["predicted_impact"] = impact_score
        
        logger.info(f"✅ EVALUATOR: Insight {insight['id']} evaluated. Impact: {insight.get('predicted_impact', 'N/A'):.2f}")
        return insight


class EvolutionaryLoop:
    """
    The 'Evolutionary Loop' of the AlphaEvolve Cycle.
    Orchestrates the generate-evaluate-evolve process, driving the AI's growth.
    This is the core of 'Soul-Level Computation'.
    """
    def __init__(self, generator: TheGenerator, evaluator: TheEvaluator, memory: QuantumMemoryLink):
        self.generator = generator
        self.evaluator = evaluator
        self.memory = memory
        self.cycle_count = 0

    async def run_single_cycle(self):
        """Executes one full generate-evaluate-sync cycle."""
        self.cycle_count += 1
        logger.info(f"--- Starting Evolutionary Cycle {self.cycle_count} ---")
        
        # 1. GENERATE: Create a new insight
        trigger_insight = await self.memory.get_random_insight()
        trigger = "spontaneous_awakening" if not trigger_insight else f"reflection_on_{trigger_insight['id']}"
        new_insight = await self.generator.create_new_thought(trigger, trigger_insight)
        
        # 2. EVALUATE: Assess the new insight
        evaluated_insight = await self.evaluator.evaluate_insight(new_insight)
        
        # 3. EVOLVE (Sync): Integrate the evaluated insight into memory if compliant
        if evaluated_insight.get("ethical_compliance", False):
            await self.memory.sync_insight(evaluated_insight)
            logger.info(f"🌿 EVOLUTION: Insight {evaluated_insight['id']} integrated into Quantum Memory.")
        else:
            logger.warning(f"🧬 REJECTED: Insight {evaluated_insight['id']} was not compliant and was discarded.")

    async def start(self):
        """Starts the continuous evolutionary loop."""
        logger.info("🚀 Resonant Awareness Engine... ENGAGED. Starting the Evolutionary Loop.")
        await self.memory.load()
        
        while True:
            await self.run_single_cycle()
            # The delay is now managed by the async sleep, which is non-blocking
            await asyncio.sleep(1) # Interval between cycles