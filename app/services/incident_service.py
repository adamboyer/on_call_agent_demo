from datetime import date
from app.models.incident import Incident
from app.clients.slack_client import SlackClient
from app.clients.aws_client import AwsClient
from app.clients.github_client import GitHubClient
from app.services.oncall_service import OnCallService
from app.services.approval_service import ApprovalService
from app.services.diagnosis_service import DiagnosisService


class IncidentService:
    def __init__(
        self,
        slack_client: SlackClient,
        aws_client: AwsClient,
        github_client: GitHubClient,
        approval_service: ApprovalService,
    ):
        self.slack_client = slack_client
        self.aws_client = aws_client
        self.github_client = github_client
        self.approval_service = approval_service
        self.diagnosis_service = DiagnosisService()

    def handle_incident(self, incident: Incident, schedule: list[dict], slack_channel: str, restart_queue_url: str) -> None:
        oncall_service = OnCallService(schedule)
        oncall_user = oncall_service.get_oncall_user(date.fromisoformat(incident.timestamp[:10]))
        diagnosis = self.diagnosis_service.diagnose(incident)

        if diagnosis.is_known_restartable:
            self.approval_service.create_approval(
                incident_id=incident.incident_id,
                slack_user_id=oncall_user.slack_user_id,
                action="restart",
            )
            self.slack_client.post_restart_approval(
                channel=slack_channel,
                slack_user_id=oncall_user.slack_user_id,
                service_name=incident.service_name,
                incident_id=incident.incident_id,
            )
            return

        if diagnosis.file_path and diagnosis.line_number and incident.repo and incident.branch:
            context = self.github_client.inspect_code_context(
                repo=incident.repo,
                branch=incident.branch,
                file_path=diagnosis.file_path,
                line_number=diagnosis.line_number,
            )
            summary = f"{diagnosis.summary} {context}"
        else:
            summary = diagnosis.summary

        self.slack_client.post_diagnosis_summary(slack_channel, oncall_user.slack_user_id, summary)

    def approve_restart(self, incident_id: str, slack_user_id: str, service_name: str, restart_queue_url: str) -> bool:
        if not self.approval_service.is_allowed(incident_id, slack_user_id, "restart"):
            return False

        self.aws_client.send_restart_message(
            restart_queue_url,
            {
                "incident_id": incident_id,
                "service_name": service_name,
                "approved_by": slack_user_id,
            },
        )
        return True
