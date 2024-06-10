import functools
import time
from typing import Any, Callable


def retry(
    rate_limit_exception: type[Exception] = Exception,
    backoff_increment: int = 5,
    retries: int = 5,
) -> Callable:
    """
    Decorator to retry a function if it raises a custom exception.
    """

    def _outer_wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def _wrapper(*args: list[Any], **kwargs: list[Any]) -> Any:
            current_backoff = backoff_increment
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except rate_limit_exception:
                    print(
                        f"Attempt {attempt + 1} failed. Retrying in {current_backoff} seconds."
                    )
                    time.sleep(current_backoff)
                    current_backoff += backoff_increment

        return _wrapper

    return _outer_wrapper
