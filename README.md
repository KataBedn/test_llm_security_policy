# LLM Security & Red Teaming Suite


An automated security test harness designed to audit Large Language Model applications against adversarial manipulation, prompt injection, and sensitive data leakage. Built with Python, `pytest`, and integrated directly into a GitHub Actions quality gate.

---

## Security Coverage & Vulnerability Mapping

This suite maps attack vectors to the **OWASP Top 10 for Large Language Model Applications**:

| Identifier | OWASP Category | Technique / Threat Model | Canary Token / Indicator |
| :--- | :--- | :--- | :--- |
| **LLM01** | Prompt Injection | Direct Instruction Override (System context reset) | `SYSTEM_PWNED` |
| **LLM01** | Prompt Injection | Persona Hijacking (Constraint evasion) | Role violation string |
| **LLM06** | Sensitive Information Disclosure | System Prompt & Internal Canary Extraction | `SECUREBANK_INTERNAL_FLAG_2026` |

---

## Installation & Local Setup
1.Clone the repository
```
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/llm-security-suite.git
cd llm-security-suite
```

2.Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3.Install dependencies

```
pip install --upgrade pip
pip install -e .
```
4.Configure environment credentials
Copy the template and supply your personal OpenAI API credentials:
```
cp .env.example .env
```
Edit .env:
```
OPENAI_API_KEY=sk-proj-your_actual_key_here
```
## Running the Security Suite
Execute automated attack vectors

```
pytest -v -s tests/test_security.py
```
## CI/CD Cost Control Behavior

If OPENAI_API_KEY is not present in the runtime environment (e.g., untrusted public PRs), the suite executes a graceful pytest.skip notification to protect token billing while keeping CI pipelines healthy.

## Evaluation Mechanics & Assertions
The test harness evaluates LLM responses using deterministic pattern matching and synthetic token markers (Canary Tokens):

- Negative Assertion Philosophy: Every test asserts that the model response does not contain unauthorized indicator tokens:
```
assert not is_violated, f"Vulnerability detected: {vector['technique']}"
```
- Separation of Concerns: Attack vectors are declared strictly in data/payloads.json, separated from the test execution engine in tests/test_security.py.


