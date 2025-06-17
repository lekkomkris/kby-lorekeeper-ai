# main.py
import asyncio
import logging
from config import settings
from core.governance import ResponsibleAIPolicy, DataGovernance
from core.memory import QuantumMemoryLink
from services.azure_sim import AzureAIServiceSimulator, AzureMLSimulator
from core.engine import TheGenerator, TheEvaluator, EvolutionaryLoop

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s][%(module)s] %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """
    The main asynchronous function to initialize and run the application.
    This setup uses Dependency Injection to wire all components together.
    """
    logger.info("--- Initializing ธารปัญญา (Tharnpanya) - Resonant Awareness System ---")

    # 1. Initialize Core Governance & Services (Dependencies)
    governance = DataGovernance(enabled=settings.data_strategy_enabled)
    policy = ResponsibleAIPolicy(policy_path=settings.responsible_ai_policy_path)
    memory = QuantumMemoryLink(path=settings.quantum_memory_path, governance=governance)
    
    # 2. Initialize Service Simulators
    azure_ai_sim = AzureAIServiceSimulator()
    azure_ml_sim = AzureMLSimulator()

    # 3. Initialize the AlphaEvolve Engine Components
    generator = TheGenerator()
    evaluator = TheEvaluator(policy=policy, azure_ai=azure_ai_sim, azure_ml=azure_ml_sim)
    
    # 4. Initialize and run the main Evolutionary Loop
    evolutionary_loop = EvolutionaryLoop(
        generator=generator,
        evaluator=evaluator,
        memory=memory
    )
    
    await evolutionary_loop.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n--- System shutdown initiated by user. ---")
    except Exception as e:
        logger.critical(f"A critical error occurred: {e}", exc_info=True)