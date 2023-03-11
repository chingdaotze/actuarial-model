from abc import (
    ABC,
    abstractmethod
)
from datetime import date

from src.system.projection.parameters import ProjectionParameters
from src.system.data_sources import DataSources


class Projection(
    ABC
):

    """
    Abstract class that represents a projection moving forward through time. Inherit this class to
    implement a projection.
    """

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        """
        Constructor method. Sets the starting time step and declares projection entities. Override this
        method to declare additional projection entities.

        :param projection_parameters:
        """

        self.projection_parameters: ProjectionParameters = projection_parameters

        self.data_sources: DataSources = DataSources(
            projection_parameters=projection_parameters
        )

        self.t: date = self.projection_parameters.start_t

    @abstractmethod
    def project_time_step(
        self
    ) -> None:

        """
        Abstract method that calls events from various projection entities. Override this method to define
        events that occur within a single time step.

        :return:
        """

        ...

    # noinspection PyMethodMayBeStatic
    def halt_projection(
        self
    ) -> bool:

        """
        By default, evaluating this method may trigger a halt in the main projection loop.
        Override this method to define custom halt logic. For example, halting when the policy count
        reaches zero. The default behavior is to never halt the projection.

        :return:
        """

        return False

    def run_projection(
        self
    ) -> None:

        """
        Runs the main projection loop, projecting forward one time step at a time. Override this method to
        create a custom projection loop.

        :return:
        """

        while self.t <= self.projection_parameters.end_t:

            self.project_time_step()

            self.t += self.projection_parameters.time_step

            if self.halt_projection():

                break
