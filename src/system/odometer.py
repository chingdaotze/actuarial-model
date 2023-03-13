from typing import Callable
from datetime import datetime
from uuid import uuid4

from src.system.logger import logger


def odometer(
    function: Callable
) -> Callable:

    """
    Decorator that logs the runtime of the decorated function. Each time a function is called, it is
    given a unique function ID as a GUID.

    :param function:
    :return:
    """

    def wrapper(
        *args,
        **kwargs
    ):

        start_time = datetime.now()
        function_id = str(uuid4())

        logger.print(
            message=f'{function.__qualname__}: {function_id} starting ...'
        )

        function(
            *args,
            **kwargs
        )

        run_time = datetime.now() - start_time

        logger.print(
            message=f'{function.__qualname__}: {function_id} complete! '
                    f'Runtime was {round(run_time.seconds, 2)} seconds.'
        )

    return wrapper
