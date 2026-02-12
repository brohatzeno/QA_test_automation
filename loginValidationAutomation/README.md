# Login & Forgot-Password Automation (Selenium + Python)

A lightweight Selenium framework that tests login and forgot‑password OTP flows for a fintech admin app. It validates expected vs actual behavior and writes structured JSON logs for each run.

## Features
- Login validation with expected vs actual outcomes
- Forgot‑password OTP flow with error capture
- OOP structure for reusable flows
- JSON logging with summaries and per‑attempt details

## Project Structure
```
core/
  auth_flow.py        # Reusable browser actions and OTP/login helpers
  base_test.py        # Test lifecycle + registry
  assertions.py       # Business logic checks
  logger.py           # JSON logging

tests/
  login_automation.py # Login test cases
  forgot_password.py  # Forgot‑password + OTP test

results/
  login_attempts_logs.json
  forgot_password_logs.json

main.py               # Runs all registered tests
```

## Setup
1. Install dependencies:
```
pip install selenium
```
2. Ensure ChromeDriver matches your local Chrome version and is on PATH.

## Run
```
python3 main.py
```

## Logs
- `results/login_attempts_logs.json`
- `results/forgot_password_logs.json`

Each log file contains:
- `summary` totals
- `runs` with timestamped attempts

## Notes
- OTP input fields are matched by `aria-label` (e.g., “Please enter OTP character 1”).
- OTP errors are captured from visible error text and stored per attempt.

## Extending
Add new tests under `tests/`, register them with `@BaseTest.register`, and they will be picked up by `main.py`.
