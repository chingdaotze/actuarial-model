from typing import (
    Callable,
    Any
)
from datetime import datetime
from uuid import uuid4

from src.system.logger import logger


def odometer(
    function: Callable
) -> Callable:

    """
    Decorator that logs the runtime of a decorated function. Each time a function is called, it is
    given a unique function ID as a GUID.

    :param function:
    :return:
    """

    def wrapper(
        *args,
        **kwargs
    ) -> Any:

        """
        Wrapper function that wraps the decorated function. Contains the core logic for this decorator.

        :param args:
        :param kwargs:
        :return:
        """

        start_time = datetime.now()
        function_id = str(uuid4())

        logger.print(
            message=f'Function: {function.__qualname__}, ID: {function_id} starting ...'
        )

        return_value = function(
            *args,
            **kwargs
        )

        run_time = datetime.now() - start_time

        logger.print(
            message=f'Function: {function.__qualname__}, ID: {function_id} complete! '
                    f'Runtime was {round(run_time.seconds, 2)} seconds.'
        )

        return return_value

    return wrapper
