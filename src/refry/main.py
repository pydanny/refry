import functools
import logging
import math
import random
import time
from typing import Any
from typing import Callable
from typing import Type

# Logger's log level is configurable with `log_level`
logger = logging.getLogger(__name__)


def retry(
    backoff_increment: int = 5,
    backoff_type: str = "sequential",
    jitter: bool = False,
    rate_limit_exception: Type[Exception] = Exception,
    retries: int = 5,
    log_level: int = logging.INFO,
) -> Callable:
    """
    Decorator to retry a function if it raises a custom exception.
    """

    def calculate_backoff(attempt: int) -> float:
        backoff_strategies = {
            "sequential": backoff_increment * (attempt + 1),
            "logarithmic": math.log(attempt + 2) * backoff_increment,
            "exponential": (2**attempt) * backoff_increment,
        }
        backoff = backoff_strategies.get(
            backoff_type, backoff_increment * (attempt + 1)
        )
        return backoff + random.uniform(0, backoff_increment) if jitter else backoff

    def _outer_wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def _wrapper(*args: list[Any], **kwargs: list[Any]) -> Any:
            logger.setLevel(log_level)
            logger.log(
                log_level,
                f"Applying retry decorator with backoff_type='{backoff_type}', "
                f"backoff_increment={backoff_increment}, jitter={jitter}, retries={retries}",
            )
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except rate_limit_exception as exception:
                    last_exception = exception
                    current_backoff = calculate_backoff(attempt)
                    logger.log(
                        log_level,
                        f"Attempt {attempt + 1} failed with exception: {exception}. "
                        f"Retrying in {current_backoff:.2f} seconds.",
                    )
                    time.sleep(current_backoff)
            # If all retries fail, log the final failure and raise the exception without additional message
            logger.error(
                f"All {retries} retries failed for function {func.__name__}.",
                exc_info=(
                    type(last_exception),
                    last_exception,
                    last_exception.__traceback__,
                )
                if last_exception is not None
                else True,
            )
            if last_exception is not None:
                raise last_exception
            raise rate_limit_exception

        return _wrapper

    return _outer_wrapper
