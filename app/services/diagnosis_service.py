from dataclasses import dataclass
from app.models.incident import Incident
from app.utils.stacktrace import extract_file_and_line


KNOWN_RESTARTABLE_ERRORS = {
    "DB_POOL_EXHAUSTED",
    "STALE_CONNECTION",
    "CACHE_DEADLOCK",
}


@dataclass
class DiagnosisResult:
    is_known_restartable: bool
    summary: str
    file_path: str | None = None
    line_number: int | None = None
    confidence: str = "low"


class DiagnosisService:
    def diagnose(self, incident: Incident) -> DiagnosisResult:
        if incident.error_type in KNOWN_RESTARTABLE_ERRORS:
            return DiagnosisResult(
                is_known_restartable=True,
                summary=f"Known restartable issue detected: {incident.error_type}",
                confidence="high",
            )

        file_path, line_number = extract_file_and_line(incident.stacktrace or "")
        return DiagnosisResult(
            is_known_restartable=False,
            summary=(
                "Unknown issue. Parsed stack trace and identified a possible failure location."
                if file_path else
                "Unknown issue. Could not identify a specific file and line from the stack trace."
            ),
            file_path=file_path,
            line_number=line_number,
            confidence="medium" if file_path else "low",
        )
