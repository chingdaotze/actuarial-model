from abc import ABC
from typing import TYPE_CHECKING

from src.system.data_sources.namespace import DataSourceNamespace
if TYPE_CHECKING:
    from src.system.projection.parameters import ProjectionParameters


class DataSourcesRoot(
    DataSourceNamespace,
    ABC
):

    """
    Abstract container class that acts as a top-level namespace for data sources.
    """

    def __init__(
        self,
        projection_parameters: 'ProjectionParameters'
    ):

        """
        Constructor method. Data sources can be added by overriding and adding additional class
        attributes.

        :param projection_parameters:
        """

        DataSourceNamespace.__init__(
            self=self,
            path=projection_parameters.resource_dir_path
        )

        self.projection_parameters: ProjectionParameters = projection_parameters
