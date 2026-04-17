from datetime import datetime, timedelta, UTC
from app.models.approval import ApprovalRecord


class ApprovalService:
    def __init__(self):
        self._records: dict[str, ApprovalRecord] = {}

    def create_approval(self, incident_id: str, slack_user_id: str, action: str, ttl_minutes: int = 15) -> ApprovalRecord:
        record = ApprovalRecord(
            incident_id=incident_id,
            slack_user_id=slack_user_id,
            action=action,
            expires_at=datetime.now(UTC) + timedelta(minutes=ttl_minutes),
        )
        self._records[self._key(incident_id, action)] = record
        return record

    def is_allowed(self, incident_id: str, slack_user_id: str, action: str) -> bool:
        record = self._records.get(self._key(incident_id, action))
        if not record:
            return False
        if datetime.now(UTC) > record.expires_at:
            return False
        return record.slack_user_id == slack_user_id

    @staticmethod
    def _key(incident_id: str, action: str) -> str:
        return f"{incident_id}:{action}"
