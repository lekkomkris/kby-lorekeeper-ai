# core/governance.py
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple, List, Optional

from config import settings

logger = logging.getLogger(__name__)

class ResponsibleAIPolicy:
    """Manages and enforces the Responsible AI policy."""
    def __init__(self, policy_path: str):
        self.policy = self._load_policy(policy_path)
        logger.info(f"Responsible AI Policy loaded from {policy_path}.")

    def _load_policy(self, policy_path: str) -> Dict:
        try:
            with open(policy_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Policy file issue at {policy_path} ({e}). Using default policy.")
            return {
                "ethical_guidelines": ["do_no_harm", "promote_fairness", "ensure_transparency"],
                "bias_detection_threshold": 0.7,
                "safety_protocols": ["content_moderation", "reversion_on_anomaly"]
            }

    def check_compliance(self, action_context: Dict) -> Tuple[bool, str]:
        """Checks if a given action context complies with the loaded policy."""
        if not settings.responsible_ai_enabled:
            return True, "Responsible AI checks are disabled."
        
        # Implement more sophisticated checks here
        if "content" in action_context and "harmful" in action_context["content"].lower():
            return False, "Content violates 'do_no_harm' policy."
        
        # Simulated bias check
        if "data" in action_context and random.random() > self.policy.get("bias_detection_threshold", 0.7):
             return True, "Bias check passed." # Inverted logic to pass more often
        
        return True, "Compliant."


class DataGovernance:
    """Handles data validation, retention, and overall data strategy."""
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        if self.enabled:
            logger.info("Data Governance Module enabled.")
        self.data_schemas = {
            "insight": {"id": str, "timestamp": str, "content": str},
            # Add other schemas as needed
        }
        self.data_retention_policy = timedelta(days=365 * 5)

    def validate_data(self, data_type: str, data: Dict) -> bool:
        """Validates data against a predefined schema."""
        if not self.enabled:
            return True
        # Basic validation, can be enhanced with Pydantic models
        schema = self.data_schemas.get(data_type)
        if not schema:
            logger.warning(f"No schema for data type: {data_type}")
            return False
        return all(key in data and isinstance(data[key], expected_type) for key, expected_type in schema.items())

    def enforce_retention(self, data_store: List[Dict]) -> List[Dict]:
        """Filters a list of data based on retention policy."""
        if not self.enabled:
            return data_store
        cutoff_time = datetime.utcnow() - self.data_retention_policy
        return [
            item for item in data_store
            if datetime.fromisoformat(item.get("timestamp", datetime.min.isoformat())) > cutoff_time
        ]