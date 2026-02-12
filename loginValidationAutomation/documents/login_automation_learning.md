# Learning Journey: Building a Login & Forgot‑Password Automation System (Selenium + Python)

## Introduction
This project started as a simple login automation script and evolved into a small, reusable framework that tests both login and forgot‑password OTP flows. The key learning was not just checking if an action succeeded, but validating whether the system behaved correctly.

## Tools and Setup
- Python 3.9+
- Selenium WebDriver
- ChromeDriver (matching local Chrome)
- JSON for structured run logs
- Explicit waits to avoid race conditions

## Current Architecture
The project is now split into reusable core logic and test scenarios:

```
core/
  base_test.py      # test lifecycle + registry
  auth_flow.py      # login + OTP actions
  assertions.py     # business logic checks
  logger.py         # JSON logging

tests/
  login_automation.py
  forgot_password.py

results/
  login_attempts_logs.json
  forgot_password_logs.json
```

### Why this split helps
- `core/` holds reusable building blocks.
- `tests/` holds scenario data and orchestration.
- Adding a new test means creating a new file in `tests/` without touching core logic.

## Login Flow (Validation‑Focused)
Login scenarios are defined as structured data with expected outcomes:

```python
LOGIN_ATTEMPTS = [
    {"label": "WRONG email + WRONG password", "email": WRONG_EMAIL, "password": WRONG_PASSWORD, "expected_login": False},
    {"label": "REAL email + WRONG password", "email": CORRECT_EMAIL, "password": WRONG_PASSWORD, "expected_login": False},
    {"label": "REAL email + REAL password", "email": CORRECT_EMAIL, "password": CORRECT_PASSWORD, "expected_login": True},
]
```

Each attempt records:
- `login_success` (what actually happened)
- `expected_login` (what should happen)
- `test_case_success` (whether behavior was correct)

## Forgot‑Password + OTP Flow
The forgot‑password test follows a two‑step OTP validation:

1. Submit email on `/forgot-password`
2. On `/verify-otp`, submit a wrong OTP and capture errors
3. Return to `/forgot-password`, submit email again
4. On `/verify-otp`, submit the correct OTP
5. If the URL changes, mark success

This keeps the flow realistic and avoids carrying state between OTP attempts.

## Error Capture
Errors are captured by scanning visible page text for key phrases such as:
- `Invalid`
- `Incorrect`
- `expired`
- `OTP`

These are stored per attempt in JSON logs to support debugging and audits.

## JSON Log Format
Each run is appended to a cumulative log file:

```json
{
  "summary": {"total_runs": 2, "total_success": 1, "total_failed": 3},
  "runs": [
    {
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "attempts": [ ... ]
    }
  ]
}
```

## Key Takeaways
- Automation is not just about clicking buttons — it’s about validating system behavior.
- Separating reusable logic from test scenarios makes scaling easy.
- Structured logs make failures traceable without manual re‑runs.

## Future Improvements
- Screenshot capture on failure
- Externalized secrets (env vars)
- OTP retry strategies based on backend rate limits
- HTML report generation from JSON logs
