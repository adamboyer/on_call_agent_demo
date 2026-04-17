from datetime import date
from app.models.oncall import OnCallEntry


class OnCallService:
    def __init__(self, schedule: list[dict]):
        self.schedule = [OnCallEntry(**item) for item in schedule]

    def get_oncall_user(self, target_date: date) -> OnCallEntry:
        target = target_date.isoformat()
        for entry in self.schedule:
            if entry.start_date <= target <= entry.end_date:
                return entry
        raise ValueError(f"No on-call user found for {target}")
