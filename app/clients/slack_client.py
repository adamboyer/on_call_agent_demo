class SlackClient:
    """Local stub for Slack calls. Replace with Slack SDK or Web API later."""

    def post_message(self, channel: str, text: str) -> None:
        print(f"[SLACK] channel={channel} text={text}")

    def post_restart_approval(self, channel: str, slack_user_id: str, service_name: str, incident_id: str) -> None:
        text = (
            f"<@{slack_user_id}> Incident `{incident_id}` looks restartable for `{service_name}`. "
            "Approve restart?"
        )
        self.post_message(channel, text)

    def post_diagnosis_summary(self, channel: str, slack_user_id: str, summary: str) -> None:
        self.post_message(channel, f"<@{slack_user_id}> {summary}")
