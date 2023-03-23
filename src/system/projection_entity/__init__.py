from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Callable,
    Any
)
from datetime import date
from os.path import (
    join,
    dirname
)

from dateutil.relativedelta import relativedelta

from src.system.data_sources import DataSourcesRoot
from src.system.projection_entity.projection_values import ProjectionValues
from src.system.logger import logger


class ProjectionEntity(
    ABC
):

    """
    Abstract class that represents an entity within a projection (like a person or a policy). A projection
    entity is the primary building block for projections, and has several defined properties:

    1. A projection entity contains a values attribute, which stores the current and historic states
       of a projection entity.

    2. A projection entity declares events as class methods. For example, a person could have a death
       event. Events typically change and update the values attribute.

    3. A projection entity implements a special project event, which moves the projection entity
       forward through time.

    Inherit this class to implement a custom projection entity.
    """

    def __init__(
        self,
        init_t: date,
        data_sources: DataSourcesRoot,
        values: ProjectionValues
    ):

        self.init_t: date = init_t
        self.data_sources: DataSourcesRoot = data_sources
        self.values: ProjectionValues = values

    @abstractmethod
    def __str__(
        self
    ) -> str:

        """
        Abstract method that provides a string representation of the projection entity. Also used as a
        file name when printing output.

        :return:
        """

        ...

    @abstractmethod
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        """
        Abstract method that pushes the projection entity forward in time. This method should
        trigger all events that are time-dependent. For example, updating policy counts for any
        decrements that occur within the interval, or updating account values using the latest
        market values.

        :param t:
        :param duration:
        :return:
        """

        ...

    def write_snapshots(
        self,
        output_file_path: str
    ) -> None:

        """
        Convenience method that writes output for itself, as well as any projection entity members.
        Note that this function behaves recursively.

        :param output_file_path:
        :return:
        """

        self.values.write_snapshots(
            path=output_file_path
        )

        for attribute in self.__dict__.values():

            if issubclass(type(attribute), ProjectionEntity):

                attribute_output_file_path = join(
                    dirname(output_file_path),
                    f'{attribute}.csv'
                )

                attribute.write_snapshots(
                    output_file_path=attribute_output_file_path
                )


def projection_entity_init(
    function: Callable[[ProjectionEntity, ...], None]
) -> Callable:

    """
    Decorator that takes a snapshot at object initialization, and calls the projects initial values.
    Note that this decorator only works on the __init__ function.

    :param function:
    :return:
    """

    def wrapper(
        instance: ProjectionEntity,
        *args,
        **kwargs
    ) -> Any:

        """
        Wrapper function that wraps the decorated function. Contains the core logic for this decorator. Note that
        instance must be a subclass of a projection entity.

        :param instance:
        :param args:
        :param kwargs:
        :return:
        """

        if issubclass(type(instance), ProjectionEntity):

            if function.__name__ == '__init__':

                # Execute function
                function(
                    instance,
                    *args,
                    **kwargs
                )

                # Execute projection
                init_t = kwargs['init_t']

                instance.project(
                    t=init_t,
                    duration=relativedelta()
                )  # Snapshot automatically taken here if method is decorated

            else:

                logger.raise_expr(
                    expr=AssertionError(
                        'Must use the @projection_entity_init decorator on the __init__ function!'
                    )
                )

        else:

            logger.raise_expr(
                expr=AssertionError(
                    'Must use the @projection_entity_init decorator on a projection entity!'
                )
            )

    return wrapper


def take_snapshot(
    function: Callable[[ProjectionEntity, date, relativedelta], Any]
) -> Callable:

    """
    Decorator that takes a snapshot whenever it is used. Note that this only works on functions within a projection
    entity.

    :param function:
    :return:
    """

    def wrapper(
        instance: ProjectionEntity,
        *args,
        **kwargs
    ) -> Any:

        """
        Wrapper function that wraps the decorated function. Contains the core logic for this decorator. Note that:

        1. Instance must be a subclass of a projection entity.
        2. There must be keyword arguments of t and duration.

        :param instance:
        :param args:
        :param kwargs:
        :return:
        """

        if issubclass(type(instance), ProjectionEntity):

            if 't' in kwargs and 'duration' in kwargs:

                # Execute function
                return_value = function(
                    instance,
                    *args,
                    **kwargs
                )

                # Take snapshot
                t = kwargs['t']
                duration: relativedelta = kwargs['duration']

                instance.values.take_snapshot(
                    t=t + duration
                )

                return return_value

            else:

                logger.raise_expr(
                    expr=AssertionError(
                        '@take_snapshot decorator missing required arguments t and duration!'
                    )
                )

        else:

            logger.raise_expr(
                expr=AssertionError(
                    'Must use the @take_snapshot decorator on a projection entity!'
                )
            )

    return wrapper
