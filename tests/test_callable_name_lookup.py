"""Resolve a fallback only for a missing name, not for other logging failures."""

import unittest
from unittest.mock import patch

from refry import retry
from refry.main import logger


class CallableNameLookupTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(logger.setLevel, logger.level)

    def test_existing_name_does_not_read_class_name(self):
        class NoClassName(type):
            def __getattribute__(cls, name):
                if name == "__name__":
                    raise RuntimeError("class name lookup forbidden")
                return super().__getattribute__(name)

        class NamedOperation(metaclass=NoClassName):
            __name__ = "ordinary_instance_name"

            def __call__(self):
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(NamedOperation())
        with self.assertLogs(logger) as records:
            try:
                operation()
            except Exception as caught:
                error = caught
            else:
                self.fail("The failing operation unexpectedly returned")
        self.assertIsInstance(error, ValueError)
        self.assertEqual(
            records.records[-1].getMessage(),
            "All 1 retries failed for function ordinary_instance_name.",
        )

    def test_empty_name_is_not_replaced(self):
        class EmptyName:
            __name__ = ""

            def __call__(self):
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(EmptyName())
        with self.assertLogs(logger) as records:
            with self.assertRaises(ValueError):
                operation()
        self.assertEqual(
            records.records[-1].getMessage(),
            "All 1 retries failed for function .",
        )

    def test_dynamic_none_name_is_not_replaced(self):
        class ChangingName:
            __name__ = "valid_during_decoration"

            def __call__(self):
                self.__name__ = None
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(ChangingName())
        with self.assertLogs(logger) as records:
            with self.assertRaises(ValueError):
                operation()
        self.assertEqual(
            records.records[-1].getMessage(),
            "All 1 retries failed for function None.",
        )

    def test_nonattribute_name_error_is_not_replaced(self):
        error = RuntimeError("name lookup failed")

        class FailingName:
            failed = False

            @property
            def __name__(self):
                if self.failed:
                    raise error
                return "valid_during_decoration"

            def __call__(self):
                self.failed = True
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(FailingName())
        with self.assertRaises(RuntimeError) as raised:
            operation()
        self.assertIs(raised.exception, error)

    def test_name_formatting_attributeerror_is_not_replaced(self):
        error = AttributeError("name formatting failed")

        class FailingFormat:
            def __format__(self, format_spec):
                raise error

        class ChangingName:
            __name__ = "valid_during_decoration"

            def __call__(self):
                self.__name__ = FailingFormat()
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(ChangingName())
        with self.assertRaises(AttributeError) as raised:
            operation()
        self.assertIs(raised.exception, error)

    def test_logger_attributeerror_is_not_replaced(self):
        error = AttributeError("logging failed")

        class NamedOperation:
            __name__ = "operation"

            def __call__(self):
                raise ValueError("failure")

        operation = retry(
            retries=1, backoff_increment=0, rate_limit_exception=ValueError
        )(NamedOperation())
        with patch.object(logger, "error", side_effect=error):
            with self.assertRaises(AttributeError) as raised:
                operation()
        self.assertIs(raised.exception, error)


if __name__ == "__main__":
    unittest.main()
