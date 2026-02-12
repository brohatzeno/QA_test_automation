from core.base_test import BaseTest
from tests import login_automation  # noqa: F401 - registers tests
from tests import forgot_password  # noqa: F401 - registers tests


def main():
    if not BaseTest.registry:
        print("No tests registered.")
        return
    for test_cls in BaseTest.registry:
        if hasattr(test_cls, "build") and callable(getattr(test_cls, "build")):
            test = test_cls.build()
        else:
            test = test_cls(login_automation.LOGIN_URL, login_automation.LOGIN_ATTEMPTS)
        print(f"\n=== Running: {test.name} ===")
        test.run()


if __name__ == "__main__":
    main()
