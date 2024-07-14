import math
import time
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


    def test_sequential_backoff(self) -> None:
        """
        Test that the sequential backoff strategy works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="sequential")
        def fails_sequential() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_sequential()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Assert that the total wait time is correct
        expected_wait_time = sum(range(1, RETRIES + 1))
        self.assertAlmostEqual(end_time - start_time, expected_wait_time, delta=1)

    def test_logarithmic_backoff(self) -> None:
        """
        Test that the logarithmic backoff strategy works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="logarithmic")
        def fails_logarithmic() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_logarithmic()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Calculate expected wait time using logarithmic backoff
        expected_wait_time = sum(math.log(i + 2) for i in range(RETRIES))
        self.assertAlmostEqual(end_time - start_time, expected_wait_time, delta=1)

    def test_exponential_backoff(self) -> None:
        """
        Test that the exponential backoff strategy works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="exponential")
        def fails_exponential() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_exponential()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Calculate expected wait time using exponential backoff
        expected_wait_time = sum(2 ** i for i in range(RETRIES))
        self.assertAlmostEqual(end_time - start_time, expected_wait_time, delta=1)

    def test_sequential_backoff_with_jitter(self) -> None:
        """
        Test that the sequential backoff strategy with jitter works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="sequential", jitter=True)
        def fails_sequential_jitter() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_sequential_jitter()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Since jitter adds a random time, we cannot assert the exact wait time.
        # We will assert the minimum expected wait time instead.
        min_expected_wait_time = sum(range(1, RETRIES + 1))
        self.assertGreaterEqual(end_time - start_time, min_expected_wait_time)

    def test_logarithmic_backoff_with_jitter(self) -> None:
        """
        Test that the logarithmic backoff strategy with jitter works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="logarithmic", jitter=True)
        def fails_logarithmic_jitter() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_logarithmic_jitter()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Since jitter adds a random time, we cannot assert the exact wait time.
        # We will assert the minimum expected wait time instead.
        min_expected_wait_time = sum(math.log(i + 2) for i in range(RETRIES))
        self.assertGreaterEqual(end_time - start_time, min_expected_wait_time)

    def test_exponential_backoff_with_jitter(self) -> None:
        """
        Test that the exponential backoff strategy with jitter works correctly.
        """
        attempts: int = 0

        @retry(retries=RETRIES, backoff_increment=1, backoff_type="exponential", jitter=True)
        def fails_exponential_jitter() -> str:
            nonlocal attempts
            attempts += 1
            raise Exception("Failing")
        
        start_time = time.time()
        try:
            fails_exponential_jitter()
        except Exception:
            pass
        end_time = time.time()

        # Assert that the function was attempted the correct number of times
        self.assertEqual(attempts, RETRIES)
        # Since jitter adds a random time, we cannot assert the exact wait time.
        # We will assert the minimum expected wait time instead.
        min_expected_wait_time = sum(2 ** i for i in range(RETRIES))
        self.assertGreaterEqual(end_time - start_time, min_expected_wait_time)
