from abc import (
    ABC,
    abstractmethod
)
from os.path import join

from src.system.projection.parameters import ProjectionParameters
from src.system.projection.time_steps import TimeSteps
from src.system.data_sources import DataSourcesRoot
from src.system.projection_entity import ProjectionEntity


class Projection(
    ABC
):

    """
    Abstract class that represents a projection moving forward through time. Inherit this class to
    implement a projection.
    """

    projection_parameters: ProjectionParameters
    time_steps: TimeSteps
    data_sources: DataSourcesRoot
    output_dir_path: str

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_sources: DataSourcesRoot
    ):

        """
        Constructor method. Sets the starting time step and declares projection entities. Override this
        method to declare additional projection entities.

        :param projection_parameters:
        """

        self.projection_parameters = projection_parameters

        self.time_steps = TimeSteps(
            start_t=projection_parameters.start_t,
            end_t=projection_parameters.end_t,
            time_step=projection_parameters.time_step
        )

        self.data_sources = data_sources

    @abstractmethod
    def __str__(
        self
    ) -> str:

        ...

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

        for _ in self.time_steps:

            self.project_time_step()

            if self.halt_projection():

                break

    def write_output(
        self
    ) -> None:

        """
        Convenience method that writes output for projection entity members. Note that this function behaves
        recursively, and will write output for nested projection entity members as well.

        :param:
        :return:
        """

        for attribute in self.__dict__.values():

            if issubclass(type(attribute), ProjectionEntity):

                attribute_output_file_path = join(
                    self.output_dir_path,
                    f'{attribute}.csv'
                )

                attribute.write_projection_values_recursively(
                    output_file_path=attribute_output_file_path
                )

    @abstractmethod
    def setup_output(
        self
    ) -> None:

        """
        Abstract method that sets up the projection's output directory. Method is called serially for each projection
        before the projection starts running.

        :return:
        """

        ...
