from abc import (
    ABC,
    abstractmethod
)
from datetime import date
from os.path import (
    join,
    dirname
)

from pandas import DataFrame

from src.system.projection.time_steps import TimeSteps
from src.system.data_sources import DataSourcesRoot
from src.system.projection_entity.projection_value import ProjectionValue


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
        time_steps: TimeSteps,
        data_sources: DataSourcesRoot,
        init_t: date = None
    ):

        self.time_steps: TimeSteps = time_steps
        self.data_sources: DataSourcesRoot = data_sources

        self.init_t: date

        if init_t is None:

            self.init_t = time_steps.t

        else:

            self.init_t = init_t

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

    def write_projection_values(
        self,
        output_file_path: str
    ) -> None:

        # Combine all values into single DataFrame
        output_dataframe = DataFrame()

        for attribute_name, attribute in self.__dict__.items():

            if issubclass(type(attribute), ProjectionValue):

                if attribute.print_values:

                    output_dataframe = output_dataframe.join(
                        other=attribute.history.rename(
                            columns={
                                attribute.VALUE_COL: attribute_name
                            }
                        ),
                        how='outer'
                    )

        # Write DataFrame to disk
        if not output_dataframe.empty:

            output_dataframe.insert(
                loc=0,
                column='index',
                value=range(output_dataframe.shape[0])
            )

            output_dataframe.set_index(
                keys=['index'],
                append=True
            )

            output_dataframe.to_csv(
                path_or_buf=output_file_path,
                index=True
            )

        else:

            output_dataframe.to_csv(
                path_or_buf=output_file_path,
                index=False
            )

    def write_projection_values_recursively(
        self,
        output_file_path: str
    ) -> None:

        """
        Convenience method that writes output for itself, as well as any projection entity members.
        Note that this function behaves recursively.

        :param output_file_path:
        :return:
        """

        def _call_write_projection_values_recursively(
            projection_entity: ProjectionEntity
        ):

            projection_entity_output_file_path = join(
                dirname(output_file_path),
                f'{projection_entity}.csv'
            )

            projection_entity.write_projection_values_recursively(
                output_file_path=projection_entity_output_file_path
            )

        # Write values for this object
        self.write_projection_values(
            output_file_path=output_file_path
        )

        # Write values for all child objects
        for attribute in self.__dict__.values():

            if issubclass(type(attribute), ProjectionEntity):

                _call_write_projection_values_recursively(
                    projection_entity=attribute
                )

            elif isinstance(attribute, list):

                for element in attribute:

                    if issubclass(type(element), ProjectionEntity):

                        _call_write_projection_values_recursively(
                            projection_entity=element
                        )

            elif isinstance(attribute, dict):

                for element in attribute.values():

                    if issubclass(type(element), ProjectionEntity):

                        _call_write_projection_values_recursively(
                            projection_entity=element
                        )
