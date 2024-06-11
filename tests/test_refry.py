import unittest
from refry import retry

RETRIES = 3

class TestRefry(unittest.TestCase):
    """
    Unit tests for refry's @retry() decorator.
    """

    def test_retry_success(self) -> None:
        """
        Test that a function which always succeeds does not require retries.
        """
        @retry(retries=RETRIES)
        def always_succeeds() -> str:
            return "success"
        
        self.assertEqual(always_succeeds(), "success")

    def test_retry_eventual_success(self) -> None:
        """
        Test that a function eventually succeeds after a couple of failures.
        """
        attempts: int = 0

        @retry(retries=RETRIES)
        def succeeds_after_two_failures() -> str:
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise Exception("Failing")
            return "success"
        
        # Assert that the function returns success after retries
        self.assertEqual(succeeds_after_two_failures(), "success")
        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)

    def test_retry_exhausted(self) -> None:
        """
        Test that a function fails after the specified number of retries.
        """
        attempts: int = 0

        @retry(retries=RETRIES)
        def always_fails() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        try:
            always_fails()
        except Exception:
            pass

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)

    def test_retry_rate_limit_exception(self) -> None:
        """
        Test that the retry mechanism works correctly with a custom Exception.
        """
        attempts: int = 0

        class RateLimitException(Exception):
            pass

        @retry(retries=RETRIES, rate_limit_exception=RateLimitException)
        def fails_with_rate_limit() -> str:
            nonlocal attempts
            attempts += 1
            raise RateLimitException("Rate limit exceeded")
        
        try:
            fails_with_rate_limit()
        except RateLimitException:
            pass

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
