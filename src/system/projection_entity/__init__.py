from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Union,
    Callable,
    Any
)
from datetime import date
from os.path import (
    join,
    dirname
)

from dateutil.relativedelta import relativedelta

from src.system.projection.parameters import ProjectionParameters
from src.system.data_sources.data_source.base import DataSourceBase
from src.system.data_sources.namespace import DataSourceNamespace
from src.system.data_sources.collection import DataSourceCollection
from src.system.projection_entity.projection_values import ProjectionValues


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
        projection_parameters: ProjectionParameters,
        data_source: Union[DataSourceBase, DataSourceNamespace, DataSourceCollection],
        values: ProjectionValues
    ):

        self.projection_parameters: ProjectionParameters = projection_parameters
        self.data_source: Union[DataSourceBase, DataSourceNamespace, DataSourceCollection] = data_source
        self.values: ProjectionValues = values

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

        for attribute_name, attribute in self.__dict__.items():

            if issubclass(type(attribute), ProjectionEntity):

                attribute_output_file_path = join(
                    dirname(output_file_path),
                    f'{attribute_name}.csv'
                )

                attribute.write_snapshots(
                    output_file_path=attribute_output_file_path
                )


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
        Wrapper function that wraps the decorated function. Contains the core logic for this decorator. Note that
        instance must be a subclass of a projection entity.

        :param instance:
        :param args:
        :param kwargs:
        :return:
        """

        t = kwargs['t']
        duration: relativedelta = kwargs['duration']

        return_value = function(
            instance,
            *args,
            **kwargs
        )

        instance.values.take_snapshot(
            t=t + duration
        )

        return return_value

    return wrapper
