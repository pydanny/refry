import functools
import logging
import time
from typing import Any, Callable


def retry(
    rate_limit_exception: type[Exception]= Exception, backoff_increment: int = 5, retries: int = 5, logger: logging.Logger = None
) -> Callable:
    """
    Decorator to retry a function if it raises a `rate_limit_exception`.
    """

    def _outer_wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def _wrapper(*args: list[Any], **kwargs: list[Any]) -> Any:
            current_backoff = backoff_increment
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except rate_limit_exception:
                    logger.debug("Rate limited, backing off on attempt", attempt + 1)
                    time.sleep(current_backoff)
                    current_backoff += backoff_increment

        return _wrapper
    return _outer_wrapper