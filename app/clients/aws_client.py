import json
from pathlib import Path
from typing import Any


class AwsClient:
    """Local stub for AWS calls. Replace with boto3 later."""

    def load_oncall_schedule_from_file(self, file_path: str) -> list[dict[str, Any]]:
        return json.loads(Path(file_path).read_text())

    def send_restart_message(self, queue_url: str, payload: dict[str, Any]) -> None:
        print(f"[AWS:SQS] Sending restart payload to {queue_url}: {payload}")
