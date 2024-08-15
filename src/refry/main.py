import functools
import math
import random
import time
from typing import Any
from typing import Callable
from typing import Type


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
            # Default is the sequential backoff strategy
            backoff_type, backoff_strategies['sequential']
        )
        return backoff + random.uniform(0, backoff_increment) if jitter else backoff

    def _outer_wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def _wrapper(*args: list[Any], **kwargs: list[Any]) -> Any:
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except rate_limit_exception:
                    current_backoff = calculate_backoff(attempt)
                    print(
                        f"Attempt {attempt + 1} failed. Retrying in {current_backoff} seconds."
                    )
                    time.sleep(current_backoff)

        return _wrapper

    return _outer_wrapper
