from abc import (
    ABC,
    abstractmethod
)
from typing import Type

from dateutil.relativedelta import relativedelta

from src.system.data_sources import DataSources
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

    3. A projection entity implements a special roll-forward event, which moves the projection entity
       forward through time.

    Inherit this class to implement a custom projection entity.
    """

    def __init__(
        self,
        data_sources: DataSources,
        values_type: Type[ProjectionValues]
    ):

        self.values: values_type = values_type(
            data_sources=data_sources
        )

    @abstractmethod
    def roll_forward(
        self,
        duration: relativedelta
    ) -> None:

        """
        Abstract method that pushes the projection entity forward in time. This method should
        trigger all events that are time-dependent. For example, updating policy counts for any
        decrements that occur within the interval, or updating account values using the latest
        market values.

        :param duration:
        :return:
        """

        ...
