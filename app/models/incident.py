from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Incident:
    # Required: every incident should have an ID + at least a message
    incident_id: str
    message: str

    # Core diagnostic signals (optional but commonly present)
    error_type: Optional[str] = None
    stacktrace: Optional[str] = None
    alert_text: Optional[str] = None

    # Metadata (useful later, not required for diagnosis)
    service_name: Optional[str] = None
    timestamp: Optional[str] = None
    repo: Optional[str] = None
    branch: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Converts the incident into a clean dictionary for LLM prompts.
        Removes None values to reduce prompt noise.
        """
        return {k: v for k, v in asdict(self).items() if v is not None}