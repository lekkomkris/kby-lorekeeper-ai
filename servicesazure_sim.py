# services/azure_sim.py
import asyncio
import random
import logging
from typing import Dict

from config import settings

logger = logging.getLogger(__name__)

class AzureAIServiceSimulator:
    """Simulates calls to Azure AI Services like Text Analytics and Content Safety."""
    
    async def analyze_text_sentiment(self, text: str) -> Dict:
        await asyncio.sleep(settings.simulated_azure_ai_delay)
        sentiment = random.choice(["positive", "neutral", "negative"])
        logger.debug(f"Simulated Azure Sentiment for '{text[:20]}...': {sentiment}")
        return {"sentiment": sentiment, "score": random.uniform(0.5, 1.0)}

    async def moderate_content(self, text: str) -> bool:
        await asyncio.sleep(settings.simulated_azure_ai_delay)
        is_safe = "harmful" not in text.lower() and "toxic" not in text.lower()
        logger.debug(f"Simulated Azure Content Moderator on '{text[:20]}...': Safe={is_safe}")
        return is_safe

class AzureMLSimulator:
    """Simulates calls to a deployed Azure Machine Learning model endpoint."""

    async def predict_impact(self, insight_data: Dict) -> float:
        """Simulates an ML model predicting the 'impactfulness' of an insight."""
        await asyncio.sleep(settings.simulated_ml_inference_delay)
        # In a real scenario, this model would analyze complexity, relevance, novelty, etc.
        impact_score = random.uniform(0.1, 1.0)
        logger.debug(f"Simulated Azure ML Impact Prediction for insight {insight_data.get('id', '')}: {impact_score:.2f}")
        return impact_score