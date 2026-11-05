"""Retry logging must respect application configuration across calls."""

import logging
import unittest
from unittest.mock import patch

from refry import retry
from refry.main import logger


class RecordHandler(logging.Handler):
    """Collect real log records without configuring a logger implicitly."""

    def __init__(self) -> None:
        super().__init__()
        self.records = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


class TestLogging(unittest.TestCase):
    """Exercise logging boundaries through the public retry decorator."""

    def setUp(self) -> None:
        """Isolate logger configuration and avoid retry delays."""
        self.handler = RecordHandler()
        self.parent = logging.getLogger("refry")
        for configured_logger in (logger, self.parent):
            original = (
                configured_logger.level,
                configured_logger.handlers[:],
                configured_logger.propagate,
                configured_logger.disabled,
            )
            self.addCleanup(self.restore_logger, configured_logger, original)
            configured_logger.handlers = []
            configured_logger.disabled = False
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)
        logger.propagate = False
        sleep = patch("refry.main.time.sleep")
        sleep.start()
        self.addCleanup(sleep.stop)

    @staticmethod
    def restore_logger(configured_logger, original) -> None:
        """Restore all configuration changed by a test."""
        level, handlers, propagate, disabled = original
        configured_logger.setLevel(level)
        configured_logger.handlers = handlers
        configured_logger.propagate = propagate
        configured_logger.disabled = disabled

    def test_success_respects_application_threshold(self) -> None:
        """A DEBUG call must not override an application's WARNING filter."""
        logger.setLevel(logging.WARNING)

        @retry(log_level=logging.DEBUG)
        def succeeds():
            return "result"

        self.assertEqual(succeeds(), "result")
        self.assertEqual(self.handler.records, [])
        self.assertEqual(logger.level, logging.WARNING)

    def test_exhaustion_preserves_application_threshold(self) -> None:
        """A failed call must retain the caller's filter and final error log."""
        logger.setLevel(logging.WARNING)

        @retry(retries=1, log_level=logging.DEBUG, rate_limit_exception=ValueError)
        def fails():
            raise ValueError("temporary")

        with self.assertRaises(ValueError):
            fails()
        self.assertEqual([r.levelno for r in self.handler.records], [logging.ERROR])
        self.assertEqual(logger.level, logging.WARNING)

    def test_nested_call_does_not_suppress_outer_retry_logs(self) -> None:
        """An inner ERROR-level call must not hide an outer INFO retry."""

        @retry(log_level=logging.ERROR)
        def inner():
            return "inner"

        attempts = 0

        @retry(retries=2, log_level=logging.INFO, rate_limit_exception=ValueError)
        def outer():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                inner()
                raise ValueError("temporary")
            return "recovered"

        self.assertEqual(outer(), "recovered")
        self.assertEqual(attempts, 2)
        self.assertEqual(
            [r.levelno for r in self.handler.records],
            [logging.INFO, logging.ERROR, logging.INFO],
        )
        self.assertEqual(logger.level, logging.DEBUG)

    def test_inherited_application_threshold_is_respected(self) -> None:
        """An inherited WARNING threshold must still filter DEBUG records."""
        logger.setLevel(logging.NOTSET)
        logger.handlers = []
        logger.propagate = True
        self.parent.setLevel(logging.WARNING)
        self.parent.addHandler(self.handler)
        self.parent.propagate = False

        @retry(log_level=logging.DEBUG)
        def succeeds():
            return 7

        self.assertEqual(succeeds(), 7)
        self.assertEqual(self.handler.records, [])
        self.assertEqual(logger.level, logging.NOTSET)

    def test_log_level_still_selects_record_severity(self) -> None:
        """A configured logger receives the requested severity unchanged."""

        @retry(log_level=logging.WARNING)
        def succeeds():
            return 42

        self.assertEqual(succeeds(), 42)
        self.assertEqual([r.levelno for r in self.handler.records], [logging.WARNING])

    def test_unmatched_exception_is_not_retried(self) -> None:
        """Logging changes must not broaden the exception retry contract."""
        attempts = 0

        @retry(retries=3, rate_limit_exception=ValueError)
        def fails():
            nonlocal attempts
            attempts += 1
            raise TypeError("not retriable")

        with self.assertRaisesRegex(TypeError, "not retriable"):
            fails()
        self.assertEqual(attempts, 1)
        self.assertEqual([r.levelno for r in self.handler.records], [logging.INFO])
