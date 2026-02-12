from selenium import webdriver
import time

from core.base_test import BaseTest
from core.auth_flow import AuthFlow
from core.logger import JsonLogger
from core.assertions import evaluate_login

# -------- CONFIGURATION --------
LOGIN_URL = "https://admin.dev.xuno.co/"
CORRECT_EMAIL = "Aryan@xuno.co"
CORRECT_PASSWORD = "Admin@123"

WRONG_EMAIL = "fakeuser@test.com"
WRONG_PASSWORD = "wrongpass123"

LOGIN_ATTEMPTS = [
    {
        "label": "WRONG email + WRONG password",
        "email": WRONG_EMAIL,
        "password": WRONG_PASSWORD,
        "expected_login": False
    },
    {
        "label": "REAL email + WRONG password",
        "email": CORRECT_EMAIL,
        "password": WRONG_PASSWORD,
        "expected_login": False
    },
    {
        "label": "REAL email + REAL password",
        "email": CORRECT_EMAIL,
        "password": CORRECT_PASSWORD,
        "expected_login": True
    },
]

LOG_FILE = "results/login_attempts_logs.json"
DASHBOARD_WAIT = 3  # seconds to stay on dashboard after successful login
WAIT_TIMEOUT = 10
FINAL_INSPECTION_WAIT = 3  # seconds to keep browser on last page before exit
CONTINUE_ON_LOCK = True  # matches previous behavior


@BaseTest.register
class LoginAutomationTest(BaseTest):
    def __init__(self, login_url, attempts):
        super().__init__(name="LoginAutomationTest")
        self.login_url = login_url
        self.attempts = attempts
        self.driver = None
        self.auth = None
        self.logger = JsonLogger(LOG_FILE)

    def setup(self):
        self.driver = webdriver.Chrome()
        self.auth = AuthFlow(self.driver, wait_timeout=WAIT_TIMEOUT, dashboard_wait=DASHBOARD_WAIT)

    def execute(self):
        print("\n--- LOGIN TEST STARTED ---\n")

        for idx, attempt in enumerate(self.attempts, start=1):
            print(f"\nAttempt {idx}: {attempt['label']}")
            print(f"Using → {attempt['email']} / ******")

            result, locked = self.auth.run_login_attempt(self.login_url, attempt)

            login_success = result["login_success"]
            errors = result["error_messages"]
            final_url = result["url"]

            expected_login = attempt["expected_login"]
            test_case_success = evaluate_login(expected_login, login_success)

            if login_success:
                print(f"✅ Login successful → {final_url}")
                time.sleep(DASHBOARD_WAIT)
            else:
                print("❌ Login failed")
                for msg in errors:
                    print(f"   - {msg}")

            if not test_case_success:
                print("🚨 LOGIC BREAK DETECTED — unexpected authentication behavior")

            self.logger.add_attempt({
                "attempt_no": idx,
                "label": attempt["label"],
                "email": attempt["email"],
                "password": "******",

                "login_success": login_success,
                "expected_login": expected_login,
                "test_case_success": test_case_success,

                "error_messages": errors,
                "url": final_url
            })

            if locked and not CONTINUE_ON_LOCK:
                print("🚫 Account locked detected. Stopping further attempts.")
                break

        print("\n--- LOGIN TEST FINISHED ---\n")
        print(f"Run Timestamp: {self.logger.results['timestamp']}")
        print(f"Total Attempts: {len(self.logger.results['attempts'])}")
        print(f"Login Successes: {self.logger.results['total_success']}")
        print(f"Login Failures: {self.logger.results['total_failed']}")
        print(f"🚨 Logic Failures: {self.logger.results['logic_failures']}")
        print("\n🟢 Browser left open for inspection.")

        # Give time to inspect the final page state before exiting
        if FINAL_INSPECTION_WAIT and FINAL_INSPECTION_WAIT > 0:
            time.sleep(FINAL_INSPECTION_WAIT)

        self.logger.save()

    def teardown(self):
        if self.driver:
            self.driver.quit()


    @classmethod
    def build(cls):
        return cls(LOGIN_URL, LOGIN_ATTEMPTS)


if __name__ == "__main__":
    LoginAutomationTest.build().run()
