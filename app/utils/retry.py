import time
from functools import wraps

from app.core.logger import logger


def retry(
    exceptions,
    retries=3,
    delay=2,
    backoff=2
):
    """
    Retry decorator with exponential backoff.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            current_delay = delay

            for attempt in range(1, retries + 1):

                try:
                    return func(*args, **kwargs)

                except exceptions as error:

                    logger.warning(
                        f"Retry attempt {attempt} failed "
                        f"for function {func.__name__}: {error}"
                    )

                    if attempt == retries:
                        raise

                    time.sleep(current_delay)

                    current_delay *= backoff

        return wrapper

    return decorator