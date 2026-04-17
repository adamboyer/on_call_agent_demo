from dataclasses import dataclass


@dataclass
class OnCallEntry:
    start_date: str
    end_date: str
    person_name: str
    slack_user_id: str
