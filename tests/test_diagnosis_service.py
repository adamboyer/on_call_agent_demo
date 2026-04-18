from openai import OpenAI

from app.models.incident import Incident
from app.services.diagnosis_service import DiagnosisService


def test_diagnosis_service_with_llama32() -> None:
    print("\n--- Starting Diagnosis Test ---")

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    service = DiagnosisService(
        client=client,
        model="llama3.2",
    )

    incident = Incident(
        incident_id="inc-12345",
        message="Timeout waiting for connection from pool while processing request",
        error_type="UNKNOWN",
        stacktrace="java.sql.SQLTransientConnectionException: timeout waiting for connection from pool",
        service_name="checkout-service",
        alert_text="5xx rate above threshold",
    )

    print("\n--- Incident Input ---")
    print(incident.to_dict())

    result = service.diagnose(incident)

    print("\n--- Diagnosis Result ---")
    print("matched_issue_id:", result.matched_issue_id)
    print("confidence:", result.confidence)
    print("summary:", result.summary)
    print("recommended_actions:", result.recommended_actions)
    print("should_restart:", result.should_restart)

    # Assertions
    assert result is not None
    assert result.confidence in {"high", "medium", "low"}
    assert isinstance(result.summary, str)
    assert isinstance(result.recommended_actions, list)
    assert isinstance(result.should_restart, bool)

    print("\n--- Assertion Check ---")
    print("Matched Issue:", result.matched_issue_id)

    assert result.matched_issue_id in {"DB_POOL_EXHAUSTED", None}

    print("\n--- Test Completed Successfully ---\n")