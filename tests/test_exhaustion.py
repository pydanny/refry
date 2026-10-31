import logging
import traceback
import unittest

from refry import retry


class TestRetryExhaustion(unittest.TestCase):
    def test_exhaustion_preserves_last_exception(self) -> None:
        """Exhaustion must not construct a new exception or discard its details."""
        failures = [ValueError("first failure"), ValueError("last failure")]
        attempts = 0

        @retry(retries=2, backoff_increment=0)
        def always_fails() -> None:
            nonlocal attempts
            error = failures[attempts]
            attempts += 1
            raise error

        with self.assertRaises(ValueError) as raised:
            always_fails()

        self.assertEqual(attempts, 2)
        self.assertIs(raised.exception, failures[-1])
        self.assertEqual(str(raised.exception), "last failure")

    def test_exception_with_required_arguments_survives_exhaustion(self) -> None:
        """A custom exception must not be replaced by a constructor TypeError."""

        class RateLimitError(Exception):
            def __init__(self, retry_after: int) -> None:
                super().__init__(f"Retry after {retry_after} seconds")
                self.retry_after = retry_after

        error = RateLimitError(30)

        @retry(retries=1, backoff_increment=0, rate_limit_exception=RateLimitError)
        def request() -> None:
            raise error

        with self.assertRaises(RateLimitError) as raised:
            request()

        self.assertIs(raised.exception, error)
        self.assertEqual(raised.exception.retry_after, 30)

    def test_exhaustion_log_retains_original_traceback(self) -> None:
        """The final error record must carry the failed call's exception."""
        error = RuntimeError("service unavailable")

        @retry(retries=1, backoff_increment=0, rate_limit_exception=RuntimeError)
        def request() -> None:
            raise error

        with self.assertRaises(RuntimeError), self.assertLogs("refry.main") as captured:
            request()

        errors = [
            record for record in captured.records if record.levelno == logging.ERROR
        ]
        self.assertEqual(len(errors), 1)
        self.assertIs(errors[0].exc_info[1], error)
        self.assertIn(
            "request",
            [frame.name for frame in traceback.extract_tb(errors[0].exc_info[2])],
        )

    def test_nonpositive_retries_do_not_call_the_function(self) -> None:
        """Keep the existing no-attempt behavior for zero and negative retries."""
        for retries in (0, -1):
            with self.subTest(retries=retries):
                attempts = 0

                @retry(retries=retries, rate_limit_exception=ValueError)
                def request() -> None:
                    nonlocal attempts
                    attempts += 1

                with self.assertRaises(ValueError):
                    request()

                self.assertEqual(attempts, 0)

    def test_unmatched_exception_is_not_retried(self) -> None:
        """The exhaustion fix must not broaden which exceptions are retried."""
        error = TypeError("invalid request")
        attempts = 0

        @retry(retries=3, backoff_increment=0, rate_limit_exception=ValueError)
        def request() -> None:
            nonlocal attempts
            attempts += 1
            raise error

        with self.assertRaises(TypeError) as raised:
            request()

        self.assertEqual(attempts, 1)
        self.assertIs(raised.exception, error)

    def test_exhaustion_logs_falsey_exceptions_with_traceback(self) -> None:
        """Exception truthiness must not disable the final error traceback."""

        class FalseyError(RuntimeError):
            def __bool__(self) -> bool:
                return False

        error = FalseyError("service unavailable")

        @retry(retries=1, backoff_increment=0, rate_limit_exception=FalseyError)
        def request() -> None:
            raise error

        with self.assertRaises(FalseyError), self.assertLogs("refry.main") as captured:
            request()

        errors = [
            record for record in captured.records if record.levelno == logging.ERROR
        ]
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0].exc_info, tuple)
        self.assertIs(errors[0].exc_info[1], error)
        self.assertIn(
            "request",
            [frame.name for frame in traceback.extract_tb(errors[0].exc_info[2])],
        )
