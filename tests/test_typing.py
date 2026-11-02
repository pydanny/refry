"""Check the callable contract exposed by the public decorator with real mypy."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


class TestRetryTyping(unittest.TestCase):
    def check_fixture(self, filename: str) -> subprocess.CompletedProcess:
        root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["MYPYPATH"] = str(root / "src")
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--no-incremental",
                "--show-error-codes",
                "--no-error-summary",
                str(root / "tests" / "typing" / filename),
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_valid_calls_keep_function_method_and_overload_signatures(self) -> None:
        result = self.check_fixture("valid_calls.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_arguments_and_return_assignments_are_rejected(self) -> None:
        result = self.check_fixture("invalid_calls.py")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        diagnostics = [
            line for line in result.stdout.splitlines() if ": error:" in line
        ]
        self.assertEqual(len(diagnostics), 7, result.stdout + result.stderr)
        self.assertEqual(sum("[arg-type]" in line for line in diagnostics), 2)
        self.assertEqual(sum("[call-arg]" in line for line in diagnostics), 2)
        self.assertEqual(sum("[misc]" in line for line in diagnostics), 1)
        self.assertEqual(sum("[assignment]" in line for line in diagnostics), 2)
