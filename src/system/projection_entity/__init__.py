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
        init_t: date,
        data_sources: DataSourcesRoot
    ):

        self.init_t: date = init_t
        self.data_sources: DataSourcesRoot = data_sources

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

                output_dataframe = output_dataframe.join(
                    other=attribute.history.rename(
                        columns={
                            attribute.VALUE_COL: attribute_name
                        }
                    ),
                    how='outer'
                )

        # Create index
        output_dataframe.insert(
            loc=0,
            column='index',
            value=range(output_dataframe.shape[0])
        )

        output_dataframe.set_index(
            keys=['index'],
            append=True
        )

        # Write DataFrame to disk
        output_dataframe.to_csv(
            path_or_buf=output_file_path,
            index=True
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

        # Write values for this object
        self.write_projection_values(
            output_file_path=output_file_path
        )

        # Write values for all child objects
        for attribute in self.__dict__.values():

            if issubclass(type(attribute), ProjectionEntity):

                attribute_output_file_path = join(
                    dirname(output_file_path),
                    f'{attribute}.csv'
                )

                attribute.write_projection_values_recursively(
                    output_file_path=attribute_output_file_path
                )
