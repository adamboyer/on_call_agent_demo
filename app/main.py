from pathlib import Path
import json

from app.clients.aws_client import AwsClient
from app.clients.slack_client import SlackClient
from app.clients.github_client import GitHubClient
from app.models.incident import Incident
from app.services.approval_service import ApprovalService
from app.services.incident_service import IncidentService
from app.routes.slack_actions import handle_restart_action


BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(path: Path):
    return json.loads(path.read_text())


def demo_known_issue() -> None:
    schedule = load_json(BASE_DIR / "examples" / "oncall_schedule.json")
    payload = load_json(BASE_DIR / "examples" / "incident_known.json")
    incident = Incident(**payload)

    service = IncidentService(
        slack_client=SlackClient(),
        aws_client=AwsClient(),
        github_client=GitHubClient(),
        approval_service=ApprovalService(),
    )

    service.handle_incident(
        incident=incident,
        schedule=schedule,
        slack_channel="demo-oncall-channel",
        restart_queue_url="https://sqs.example/restart-commands",
    )

    result = handle_restart_action(
        incident_service=service,
        incident_id=incident.incident_id,
        acting_slack_user_id="U_ONCALL_1",
        service_name=incident.service_name,
        restart_queue_url="https://sqs.example/restart-commands",
    )
    print(result)


if __name__ == "__main__":
    demo_known_issue()
