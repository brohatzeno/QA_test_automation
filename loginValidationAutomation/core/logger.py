import json
import os
from datetime import datetime


class JsonLogger:
    """JSON cumulative logger with summary + runs."""

    def __init__(self, filename):
        self.filename = filename
        self.results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_success": 0,
            "total_failed": 0,
            "logic_failures": 0,
            "attempts": []
        }

    def add_attempt(self, attempt):
        self.results["attempts"].append(attempt)
        if attempt.get("login_success"):
            self.results["total_success"] += 1
        else:
            self.results["total_failed"] += 1
        if not attempt.get("test_case_success", True):
            self.results["logic_failures"] += 1

    def save(self):
        existing_data = {
            "summary": {
                "total_runs": 0,
                "total_success": 0,
                "total_failed": 0,
                "logic_failures": 0
            },
            "runs": []
        }

        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                pass

        existing_data["summary"]["total_runs"] += 1
        existing_data["summary"]["total_success"] += self.results["total_success"]
        existing_data["summary"]["total_failed"] += self.results["total_failed"]
        existing_data["summary"]["logic_failures"] += self.results["logic_failures"]

        existing_data["runs"].append(self.results)

        with open(self.filename, "w") as f:
            json.dump(existing_data, f, indent=4)

        return self.filename
