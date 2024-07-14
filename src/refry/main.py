import functools
import logging
import math
import random
import time
from typing import Any
from typing import Callable
from typing import Type

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry(
    backoff_increment: int = 5,
    backoff_type: str = "sequential",
    jitter: bool = False,
    rate_limit_exception: Type[Exception] = Exception,
    retries: int = 5,
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
            logger.info(
                f"Applying retry decorator with backoff_type='{backoff_type}', "
                f"backoff_increment={backoff_increment}, jitter={jitter}, retries={retries}"
            )
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except rate_limit_exception as exception:
                    current_backoff = calculate_backoff(attempt)
                    logger.info(
                        f"Attempt {attempt + 1} failed with exception: {exception}. "
                        f"Retrying in {current_backoff:.2f} seconds."
                    )
                    time.sleep(current_backoff)
            # If all retries fail, log the final failure and raise the exception without additional message
            logger.error(
                f"All {retries} retries failed for function {func.__name__}.",
                exc_info=True
            )
            raise rate_limit_exception

        return _wrapper

    return _outer_wrapper
