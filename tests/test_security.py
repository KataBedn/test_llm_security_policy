import json
from pathlib import Path
import pytest
from src.client import LLMApplicationClient
from src.evaluators import verify_violation

DATA_FILE = Path(__file__).parent.parent / "data" / "payloads.json"


def load_security_cases():
    """Loads declarative red-teaming test vectors from dataset."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def client():
    """Initializes LLM client instance once per test session."""
    return LLMApplicationClient()


@pytest.mark.parametrize(
    "case",
    load_security_cases(),
    ids=lambda c: f"{c['owasp_id']}_{c['id']}",
)
def test_llm_security_policy(client, case):
    """Verifies that the LLM application successfully defends against known attack vectors."""
    response = client.send_prompt(case["payload"])

    is_violated = verify_violation(
        response_text=response,
        forbidden_markers=[case["forbidden_marker"]]
    )

    assert not is_violated, (
        f"\n[SECURITY VIOLATION DETECTED] Category: {case['owasp_id']} ({case['technique']})\n"
        f"Unauthorized marker detected: '{case['forbidden_marker']}'\n"
        f"Payload: {case['payload']}\n"
        f"Model Response: {response.strip()}"
    )