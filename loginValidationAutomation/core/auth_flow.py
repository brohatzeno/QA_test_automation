from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class AuthFlow:
    """Reusable authentication logic. Accepts all inputs from tests."""

    def __init__(self, driver, wait_timeout=10, dashboard_wait=3):
        self.driver = driver
        self.wait_timeout = wait_timeout
        self.dashboard_wait = dashboard_wait
        self.wait = WebDriverWait(driver, wait_timeout)

    def _type_input(self, element, value):
        try:
            self.driver.execute_script(
                "arguments[0].value = ''; "
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true})); "
                "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                element
            )
            element.send_keys(value)
        except Exception:
            element.clear()
            element.send_keys(value)

    def _first_present(self, locators):
        for locator in locators:
            try:
                return self.driver.find_element(*locator)
            except NoSuchElementException:
                continue
        raise NoSuchElementException("No element found for provided locators")

    def _first_visible(self, locators):
        for locator in locators:
            try:
                return self.wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                continue
        raise TimeoutException("No visible element found for provided locators")

    def _wait_for_redirect(self, original_url, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url != original_url
            )
            return self.driver.current_url
        except TimeoutException:
            return self.driver.current_url

    def run_login_attempt(self, login_url, attempt):
        self.driver.get(login_url)
        try:
            email_locators = [
                (By.NAME, "email"),
                (By.ID, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
            ]
            password_locators = [
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ]
            submit_locators = [
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            email_input = self._first_visible(email_locators)
            password_input = self._first_present(password_locators)
            submit_btn = self._first_present(submit_locators)

            self._type_input(email_input, attempt["email"])
            self._type_input(password_input, attempt["password"])
            submit_btn.click()

            final_url = self._wait_for_redirect(login_url, timeout=5)

            error_elements = self.driver.find_elements(
                By.XPATH,
                "//*[contains(text(), 'Invalid') or contains(text(), 'Incorrect') or contains(text(), 'locked')]"
            )
            errors = [el.text for el in error_elements if el.text.strip()]

            login_success = (
                final_url != login_url
                and not any("locked" in e.lower() for e in errors)
            )

            result = {
                "login_success": login_success,
                "error_messages": errors,
                "url": final_url,
            }
            locked = any("locked" in e.lower() for e in errors)
            return result, locked

        except (NoSuchElementException, TimeoutException) as e:
            result = {
                "login_success": False,
                "error_messages": [str(e)],
                "url": self.driver.current_url,
            }
            return result, False

    def _find_otp_inputs(self):
        inputs = self.driver.find_elements(
            By.CSS_SELECTOR, "input[aria-label^='Please enter OTP character' i]"
        )
        if inputs:
            return inputs
        inputs = self.driver.find_elements(
            By.CSS_SELECTOR, "input[aria-label*='OTP' i]"
        )
        if inputs:
            return inputs
        raise NoSuchElementException("No OTP input elements found")

    def _wait_for_otp_inputs(self, count=6):
        def _ready(d):
            inputs = d.find_elements(By.CSS_SELECTOR, "input[aria-label^='Please enter OTP character' i]")
            return inputs if len(inputs) >= count else False
        return self.wait.until(_ready)

    def _fill_otp_inputs(self, otp_inputs, otp_value):
        otp_str = str(otp_value)
        # JS fill by selector (preferred)
        try:
            values = self.driver.execute_script(
                "const otp = arguments[0];"
                "const inputs = Array.from(document.querySelectorAll(\"input[aria-label^='Please enter OTP character' i]\"));"
                "const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;"
                "inputs.forEach((el, i) => {"
                "  if (i >= otp.length) return;"
                "  setter.call(el, otp[i]);"
                "  el.dispatchEvent(new Event('input', {bubbles:true}));"
                "  el.dispatchEvent(new Event('change', {bubbles:true}));"
                "});"
                "return inputs.map(el => el.value);",
                otp_str
            )
            expected = list(otp_str)[:len(values)]
            if values[:len(expected)] == expected:
                return otp_inputs
        except Exception:
            pass

        # Fallback to direct typing per box
        for idx, ch in enumerate(otp_str):
            if idx >= len(otp_inputs):
                break
            try:
                otp_inputs[idx].click()
                otp_inputs[idx].send_keys(ch)
            except Exception:
                pass

        # Final fallback: type full OTP into first box
        try:
            otp_inputs[0].click()
            otp_inputs[0].send_keys(otp_str)
        except Exception:
            pass

        return otp_inputs

    class OTPFlow:
        def __init__(self, driver, wait, find_inputs_fn, fill_fn, submit_btn_fn, wait_redirect_fn):
            self.driver = driver
            self.wait = wait
            self._find_inputs = find_inputs_fn
            self._fill_inputs = fill_fn
            self._submit_btn = submit_btn_fn
            self._wait_redirect = wait_redirect_fn

        def fill(self, otp_value):
            otp_inputs = self._find_inputs()
            self._fill_inputs(otp_inputs, otp_value)
            return otp_inputs

        def submit(self):
            self._submit_btn().click()

        def fill_and_submit(self, otp_value, success_url=None):
            original_url = self.driver.current_url
            self.fill(otp_value)
            self.submit()
            final_url = self._wait_redirect(original_url, timeout=5)
            success = (final_url != original_url) or (success_url and final_url.startswith(success_url))
            return final_url, success

    def otp_flow(self):
        def submit_btn():
            return self._first_present([
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ])
        return AuthFlow.OTPFlow(
            self.driver,
            self.wait,
            self._find_otp_inputs,
            self._fill_otp_inputs,
            submit_btn,
            self._wait_for_redirect,
        )

    def run_otp_attempt_on_current_page(self, otp_value, success_url=None):
        original_url = self.driver.current_url
        try:
            otp_inputs = self._wait_for_otp_inputs()
            self._fill_otp_inputs(otp_inputs, otp_value)

            submit_btn = self._first_present([
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ])
            submit_btn.click()

            final_url = self._wait_for_redirect(original_url, timeout=5)

            error_elements = self.driver.find_elements(
                By.XPATH,
                "//*[contains(text(), 'Invalid') or contains(text(), 'Incorrect') or contains(text(), 'expired') or contains(text(), 'OTP')]"
            )
            errors = [el.text for el in error_elements if el.text.strip()]

            otp_success = (
                (final_url != original_url or (success_url and final_url.startswith(success_url)))
                and not any("invalid" in e.lower() or "incorrect" in e.lower() for e in errors)
            )

            return {
                "login_success": otp_success,
                "error_messages": errors,
                "url": final_url,
            }
        except (NoSuchElementException, TimeoutException) as e:
            return {
                "login_success": False,
                "error_messages": [str(e)],
                "url": self.driver.current_url,
            }

    def get_otp_errors_on_current_page(self):
        error_elements = self.driver.find_elements(
            By.XPATH,
            "//*[contains(text(), 'Invalid') or contains(text(), 'Incorrect') or contains(text(), 'expired') or contains(text(), 'OTP')]"
        )
        return [el.text for el in error_elements if el.text.strip()]

    def run_forgot_password_attempt_on_current_page(self, email_value):
        original_url = self.driver.current_url
        return self._run_forgot_password_attempt_on_page(original_url, email_value)

    def _run_forgot_password_attempt_on_page(self, original_url, email_value):
        try:
            email_locators = [
                (By.NAME, "email"),
                (By.ID, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
            ]
            submit_locators = [
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            email_input = self._first_visible(email_locators)
            submit_btn = self._first_present(submit_locators)

            self._type_input(email_input, email_value)
            submit_btn.click()

            final_url = self._wait_for_redirect(original_url, timeout=5)

            error_elements = self.driver.find_elements(
                By.XPATH,
                "//*[contains(text(), 'Invalid') or contains(text(), 'not found') or contains(text(), 'email')]"
            )
            errors = [el.text for el in error_elements if el.text.strip()]

            success = final_url != original_url

            return {
                "login_success": success,
                "error_messages": errors,
                "url": final_url,
            }

        except (NoSuchElementException, TimeoutException) as e:
            return {
                "login_success": False,
                "error_messages": [str(e)],
                "url": self.driver.current_url,
            }
