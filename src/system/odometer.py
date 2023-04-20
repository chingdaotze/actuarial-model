"""
Performance-profiling decorator function.
"""

from typing import (
    Callable,
    Any
)
from functools import wraps
from datetime import datetime
from uuid import uuid4

from src.system.logger import Logger


def odometer(
    function: Callable
) -> Callable:

    """
    Decorator that logs the runtime of a decorated function. Each time a function is called, it is
    given a unique function ID as a GUID.

    :param function: Function to wrap.
    :return: A wrapped function.
    """

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ) -> Any:

        start_time = datetime.now()
        function_id = str(uuid4())

        Logger().print(
            message=f'Function: {function.__qualname__}, ID: {function_id} starting ...'
        )

        return_value = function(
            *args,
            **kwargs
        )

        run_time = datetime.now() - start_time

        Logger().print(
            message=f'Function: {function.__qualname__}, ID: {function_id} complete! '
                    f'Runtime was {round(run_time.seconds, 2)} seconds.'
        )

        return return_value

    return wrapper
