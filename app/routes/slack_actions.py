from app.services.incident_service import IncidentService


def handle_restart_action(
    incident_service: IncidentService,
    incident_id: str,
    acting_slack_user_id: str,
    service_name: str,
    restart_queue_url: str,
) -> dict:
    """Placeholder for a real Slack interactive callback route."""
    allowed = incident_service.approve_restart(
        incident_id=incident_id,
        slack_user_id=acting_slack_user_id,
        service_name=service_name,
        restart_queue_url=restart_queue_url,
    )

    if not allowed:
        return {"ok": False, "message": "You are not allowed to approve this action."}

    return {"ok": True, "message": "Restart approved and queued."}
