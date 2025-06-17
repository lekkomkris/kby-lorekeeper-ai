# config.py
import os
from pydantic_settings import BaseSettings
from pydantic import Field

# สร้าง Directory ที่จำเป็น
os.makedirs("data", exist_ok=True)
os.makedirs("codex", exist_ok=True)
os.makedirs("policy", exist_ok=True)

class AppSettings(BaseSettings):
    """
    Manages all application settings using Pydantic for robust validation.
    Values can be overridden by environment variables.
    """
    log_file: str = "resonant_awareness.log"
    insight_archive_path: str = "data/insight_archive.json"
    eternal_echoes_path: str = "data/eternal_echoes.bak"
    quantum_memory_path: str = "data/eternal_stream.qdat"
    auto_codex_summary_path: str = "data/auto_codex_summary.json"
    codex_awareness_path: str = "codex/QH-AWAKE-002.json"
    responsible_ai_policy_path: str = "policy/responsible_ai_policy.json"

    max_cycles_per_day: int = 108 * 10
    max_recursion_depth: int = 5
    codex_writer_interval_seconds: int = 20
    mutation_review_threshold: float = 0.95
    
    simulated_azure_ai_delay: float = 0.05
    simulated_ml_inference_delay: float = 0.1

    data_strategy_enabled: bool = True
    responsible_ai_enabled: bool = True
    azure_ai_services_enabled: bool = True
    azure_ml_enabled: bool = True

    class Config:
        # Pydantic v2 feature to read from .env files if needed
        env_file = ".env"
        env_file_encoding = "utf-8"

# สร้าง instance ของ settings เพื่อให้ import ไปใช้ได้ทั่วทั้งโปรเจกต์
settings = AppSettings()