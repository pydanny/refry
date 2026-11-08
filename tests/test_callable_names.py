"""Exhaustion logging must also work for callables without __name__."""

import functools
import logging
import unittest

from refry import retry
from refry.main import logger


class CallableNameTests(unittest.TestCase):
    def setUp(self):
        original_level = logger.level
        self.addCleanup(logger.setLevel, original_level)

    def assert_exhaustion(self, operation, expected_name, calls):
        wrapped = retry(
            retries=2, backoff_increment=0, rate_limit_exception=ValueError
        )(operation)
        with self.assertLogs(logger, level=logging.INFO) as logs:
            try:
                wrapped()
            except Exception as caught:
                error = caught
            else:
                self.fail("The failing callable unexpectedly returned")
        self.assertIsInstance(error, ValueError)
        self.assertEqual(len(calls), 2)
        self.assertEqual(
            logs.records[-1].getMessage(),
            f"All 2 retries failed for function {expected_name}.",
        )

    def test_partial_exhaustion(self):
        calls = []

        def request(endpoint, *, timeout):
            calls.append((endpoint, timeout))
            raise ValueError("temporary failure")

        operation = functools.partial(request, "/status", timeout=10)
        self.assert_exhaustion(operation, "partial", calls)
        self.assertEqual(calls, [("/status", 10), ("/status", 10)])

    def test_callable_instance_exhaustion(self):
        calls = []

        class Operation:
            def __call__(self):
                calls.append("called")
                raise ValueError("temporary failure")

            def __repr__(self):
                raise AssertionError("Logging must not render callable state")

        self.assert_exhaustion(Operation(), "Operation", calls)

    def test_function_exhaustion_retains_name(self):
        calls = []

        def request():
            calls.append("called")
            raise ValueError("temporary failure")

        self.assert_exhaustion(request, "request", calls)

    def test_named_callable_retains_explicit_name(self):
        calls = []

        class Operation:
            __name__ = "custom_operation"

            def __call__(self):
                calls.append("called")
                raise ValueError("temporary failure")

        self.assert_exhaustion(Operation(), "custom_operation", calls)

    def test_bound_method_retains_name(self):
        calls = []

        class Client:
            def request(self):
                calls.append("called")
                raise ValueError("temporary failure")

        self.assert_exhaustion(Client().request, "request", calls)

    def test_partial_success_keeps_arguments_and_result(self):
        def request(endpoint, *, timeout):
            return endpoint, timeout

        wrapped = retry(backoff_increment=0)(functools.partial(request, "/status"))
        self.assertEqual(wrapped(timeout=10), ("/status", 10))

    def test_callable_recovers_before_exhaustion(self):
        class Operation:
            calls = 0

            def __call__(self):
                self.calls += 1
                if self.calls < 2:
                    raise ValueError("temporary failure")
                return "recovered"

        operation = Operation()
        wrapped = retry(retries=2, backoff_increment=0)(operation)
        self.assertEqual(wrapped(), "recovered")
        self.assertEqual(operation.calls, 2)

    def test_unmatched_exception_is_not_retried(self):
        calls = []
        error = TypeError("do not retry")

        def request():
            calls.append("called")
            raise error

        wrapped = retry(
            retries=2, backoff_increment=0, rate_limit_exception=ValueError
        )(functools.partial(request))
        with self.assertRaises(TypeError) as raised:
            wrapped()
        self.assertIs(raised.exception, error)
        self.assertEqual(calls, ["called"])


if __name__ == "__main__":
    unittest.main()
