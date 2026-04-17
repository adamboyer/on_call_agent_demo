from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApprovalRecord:
    incident_id: str
    slack_user_id: str
    action: str
    expires_at: datetime
