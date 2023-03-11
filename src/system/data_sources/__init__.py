from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.system.projection.parameters import ProjectionParameters


class DataSources(
    ABC
):

    """
    Abstract container class that holds a collection of data sources. Inherit this class to implement
    a custom data source collection. Data sources can be added by declaring additional class attributes.
    """

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        """
        Constructor method. Data sources can be added by overriding and adding additional class
        attributes.

        :param projection_parameters:
        """

        self.projection_parameters: ProjectionParameters = projection_parameters
