from dataclasses import dataclass
import os


@dataclass
class Settings:
    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
    slack_signing_secret: str = os.getenv("SLACK_SIGNING_SECRET", "")
    slack_channel_id: str = os.getenv("SLACK_CHANNEL_ID", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    oncall_s3_bucket: str = os.getenv("ONCALL_S3_BUCKET", "")
    oncall_s3_key: str = os.getenv("ONCALL_S3_KEY", "oncall_schedule.json")
    incident_queue_url: str = os.getenv("INCIDENT_QUEUE_URL", "")
    restart_queue_url: str = os.getenv("RESTART_QUEUE_URL", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPO", "")
    github_branch: str = os.getenv("GITHUB_BRANCH", "main")
