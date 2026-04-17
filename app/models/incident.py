from dataclasses import dataclass
from typing import Optional


@dataclass
class Incident:
    incident_id: str
    service_name: str
    timestamp: str
    error_type: str
    message: str
    stacktrace: Optional[str] = None
    repo: Optional[str] = None
    branch: Optional[str] = None
