import json
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from app.models.incident import Incident


KNOWN_ISSUES = [
    {
        "id": "DB_POOL_EXHAUSTED",
        "summary": "Database connection pool is exhausted and requests cannot acquire a connection.",
        "symptoms": [
            "timeout waiting for connection from pool",
            "connection acquisition failed",
            "unable to get database connection",
            "could not acquire jdbc connection",
        ],
        "recommended_actions": [
            "Inspect database connection pool metrics",
            "Inspect recent deployment changes",
            "Inspect database health and latency",
            "Consider restarting the service if the issue appears transient",
        ],
    },
    {
        "id": "STALE_CONNECTION",
        "summary": "The service is using stale, broken, or reset backend connections.",
        "symptoms": [
            "stale connection",
            "broken pipe",
            "connection reset",
            "connection closed",
            "communications link failure",
        ],
        "recommended_actions": [
            "Inspect downstream dependency health",
            "Inspect connection lifecycle handling in code",
            "Inspect recent network or infrastructure instability",
            "Consider restarting the service",
        ],
    },
    {
        "id": "CACHE_DEADLOCK",
        "summary": "The service may be blocked by a cache lock, deadlock, or lock timeout issue.",
        "symptoms": [
            "deadlock detected",
            "cache lock timeout",
            "stuck waiting for lock",
            "timed out waiting for lock",
        ],
        "recommended_actions": [
            "Inspect cache health and lock contention",
            "Inspect recent code changes affecting concurrency",
            "Inspect thread dumps or request traces",
            "Consider restarting the service",
        ],
    },
]


@dataclass
class DiagnosisResult:
    matched_issue_id: str | None
    confidence: str
    summary: str
    recommended_actions: list[str]
    should_restart: bool


class DiagnosisService:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def diagnose(self, incident: Incident) -> DiagnosisResult:
        messages = self._build_messages(incident)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        raw_content = completion.choices[0].message.content or ""
        parsed = self._parse_llm_response(raw_content)

        matched_issue_id = parsed.get("matched_issue_id")
        if matched_issue_id == "UNKNOWN":
            matched_issue_id = None

        confidence = self._normalize_confidence(parsed.get("confidence"))
        summary = self._safe_str(
            parsed.get("summary"),
            default="Unable to determine a confident diagnosis from the known issues list.",
        )
        recommended_actions = self._normalize_actions(parsed.get("recommended_actions"))
        should_restart = bool(parsed.get("should_restart", False))

        return DiagnosisResult(
            matched_issue_id=matched_issue_id,
            confidence=confidence,
            summary=summary,
            recommended_actions=recommended_actions,
            should_restart=should_restart,
        )

    def _build_messages(self, incident: Incident) -> list[dict[str, str]]:
        incident_payload = {
            "error_type": getattr(incident, "error_type", None),
            "message": getattr(incident, "message", None),
            "stacktrace": getattr(incident, "stacktrace", None),
            "service_name": getattr(incident, "service_name", None),
            "alert_text": getattr(incident, "alert_text", None),
        }

        system_prompt = """
You are an incident diagnosis assistant.

You compare an incident against a fixed list of known issues and recommend next steps.

Rules:
- Only choose a matched_issue_id from the provided known issues.
- If the incident does not clearly match, return UNKNOWN.
- Do not invent new issue ids.
- Keep the summary short and practical.
- Recommended actions should be concrete and operational.
- Restart is only a recommendation, not an execution step.
- Return valid JSON only.
""".strip()

        user_prompt = f"""
Known issues:
{json.dumps(KNOWN_ISSUES, indent=2)}

Incident:
{json.dumps(incident_payload, indent=2)}

Return JSON in exactly this shape:
{{
  "matched_issue_id": "DB_POOL_EXHAUSTED" | "STALE_CONNECTION" | "CACHE_DEADLOCK" | "UNKNOWN",
  "confidence": "high" | "medium" | "low",
  "summary": "short explanation",
  "recommended_actions": ["action 1", "action 2"],
  "should_restart": true | false
}}
""".strip()

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _parse_llm_response(self, raw_response: str) -> dict[str, Any]:
        cleaned = raw_response.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1 and end > start:
            possible_json = cleaned[start:end + 1]
            try:
                return json.loads(possible_json)
            except json.JSONDecodeError:
                pass

        return {
            "matched_issue_id": "UNKNOWN",
            "confidence": "low",
            "summary": "Model response could not be parsed as valid JSON.",
            "recommended_actions": [
                "Inspect the raw incident details manually",
                "Review the model output and prompt formatting",
            ],
            "should_restart": False,
        }

    def _normalize_confidence(self, value: Any) -> str:
        normalized = str(value).strip().lower()
        if normalized in {"high", "medium", "low"}:
            return normalized
        return "low"

    def _normalize_actions(self, value: Any) -> list[str]:
        if not isinstance(value, list):
            return []

        actions: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                actions.append(text)
        return actions

    def _safe_str(self, value: Any, default: str) -> str:
        text = str(value).strip() if value is not None else ""
        return text or default