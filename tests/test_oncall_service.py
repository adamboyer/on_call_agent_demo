from datetime import date
from app.services.oncall_service import OnCallService


def test_get_oncall_user_returns_matching_entry():
    schedule = [
        {
            "start_date": "2026-04-01",
            "end_date": "2026-04-20",
            "person_name": "Alex",
            "slack_user_id": "U1",
        }
    ]
    service = OnCallService(schedule)
    result = service.get_oncall_user(date(2026, 4, 17))

    assert result.person_name == "Alex"
    assert result.slack_user_id == "U1"
