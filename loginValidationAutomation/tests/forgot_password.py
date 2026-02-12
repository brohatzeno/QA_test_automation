from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

from core.base_test import BaseTest
from core.auth_flow import AuthFlow
from core.logger import JsonLogger
from selenium.webdriver.common.by import By

EVENT_LOG = "results/forgot_password_events.log"
LOG_FILE = "results/forgot_password_logs.json"

FORGOT_PASSWORD_URL = "https://admin.dev.xuno.co/forgot-password"
VERIFY_OTP_URL = "https://admin.dev.xuno.co/verify-otp"
EMAIL = "aryan@xuno.co"
FAKE_OTP = "000000"
REAL_OTP = "121212"
WAIT_TIMEOUT = 10
PAGE_WAIT = 1


@BaseTest.register
class ForgotPasswordTest(BaseTest):
    def __init__(self, url):
        super().__init__(name="ForgotPasswordTest")
        self.url = url
        self.driver = None
        self.auth = None

    def setup(self):
        self.driver = webdriver.Chrome()
        self.auth = AuthFlow(self.driver, wait_timeout=WAIT_TIMEOUT)
        self.logger = JsonLogger(LOG_FILE)

    def execute(self):
        print("\n--- FORGOT PASSWORD PAGE OPENED ---\n")
        self.driver.get(self.url)
        time.sleep(PAGE_WAIT)
        # Reuse login flow helper to submit email on forgot-password page
        self.auth.run_forgot_password_attempt_on_current_page(EMAIL)
        # Wait for verify-otp URL before interacting with OTP fields
        WebDriverWait(self.driver, 10).until(
            lambda d: "verify-otp" in d.current_url
        )
        # Wait for OTP inputs to be enabled
        WebDriverWait(self.driver, 10).until(
            lambda d: all(el.is_enabled() for el in d.find_elements(
                By.CSS_SELECTOR, "input[aria-label*='OTP character' i]"
            ))
        )

        def dump_otp_values(tag):
            try:
                inputs = self.driver.find_elements(
                    By.CSS_SELECTOR, "input[aria-label*='OTP character' i]"
                )
                values = [el.get_attribute("value") for el in inputs]
                print(f"[OTP DEBUG] {tag}: {values}")
            except Exception as e:
                print(f"[OTP DEBUG] {tag}: error reading values: {e}")

        otp = self.auth.otp_flow()

        # First attempt: wrong OTP, submit, capture popup errors
        dump_otp_values("before fake fill")
        final_url, success = otp.fill_and_submit(FAKE_OTP, success_url=None)
        dump_otp_values("after fake submit")

        otp_errors = self.auth.get_otp_errors_on_current_page()
        if otp_errors:
            print("OTP errors:")
            for msg in otp_errors:
                print(f"   - {msg}")
                if "maximum" in msg.lower() and "reset" in msg.lower():
                    print("🚨 Reset limit reached detected.")
                    try:
                        with open(EVENT_LOG, "a") as f:
                            f.write("Reset limit reached on forgot-password flow.\n")
                    except Exception:
                        pass

        self.logger.add_attempt({
            "attempt_no": 1,
            "label": "WRONG OTP",
            "email": EMAIL,
            "otp": "******",
            "login_success": success,
            "expected_login": False,
            "test_case_success": (success is False),
            "error_messages": otp_errors,
            "url": final_url,
        })

        # Restart from email page if failed, then correct OTP and submit
        self.driver.get(self.url)
        time.sleep(PAGE_WAIT)
        self.auth.run_forgot_password_attempt_on_current_page(EMAIL)
        WebDriverWait(self.driver, 10).until(
            lambda d: "verify-otp" in d.current_url
        )
        WebDriverWait(self.driver, 10).until(
            lambda d: all(el.is_enabled() for el in d.find_elements(
                By.CSS_SELECTOR, "input[aria-label*='OTP character' i]"
            ))
        )

        dump_otp_values("before real fill")
        final_url, success = otp.fill_and_submit(REAL_OTP, success_url=None)
        dump_otp_values("after real submit")
        if success:
            print(f"✅ OTP success → {final_url}")

        otp_errors = self.auth.get_otp_errors_on_current_page()
        if otp_errors:
            print("OTP errors (real):")
            for msg in otp_errors:
                print(f"   - {msg}")

        self.logger.add_attempt({
            "attempt_no": 2,
            "label": "REAL OTP",
            "email": EMAIL,
            "otp": "******",
            "login_success": success,
            "expected_login": True,
            "test_case_success": (success is True),
            "error_messages": otp_errors,
            "url": final_url,
        })
        time.sleep(2)

        self.logger.save()

    def teardown(self):
        if self.driver:
            self.driver.quit()

    @classmethod
    def build(cls):
        return cls(FORGOT_PASSWORD_URL)


if __name__ == "__main__":
    ForgotPasswordTest.build().run()
