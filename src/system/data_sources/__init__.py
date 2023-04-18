"""
Modeling framework :ref:`object model <object_model>` :ref:`Data Sources <data_sources>`.
"""

from abc import (
    ABC,
    abstractmethod
)
from typing import (
    TYPE_CHECKING,
    Generator,
    Self,
    Any
)

from src.system.data_sources.namespace import DataSourceNamespace
if TYPE_CHECKING:
    from src.system.projection.parameters import ProjectionParameters


class DataSourcesRoot(
    DataSourceNamespace,
    ABC
):

    """
    Abstract container class that acts as a top-level :mod:`namespace <src.system.data_sources.namespace>` for
    data sources.
    """

    projection_parameters: 'ProjectionParameters'     #: Projection parameters.

    def __init__(
        self,
        projection_parameters: 'ProjectionParameters'
    ):

        """
        Constructor method. Data sources can be added by overriding and adding additional class
        attributes.

        :param projection_parameters: Set of projection parameters that contains a resource directory.
        """

        DataSourceNamespace.__init__(
            self=self,
            path=projection_parameters.resource_dir_path
        )

        self.projection_parameters = projection_parameters

    @abstractmethod
    def configured_data_sources(
        self
    ) -> Generator[Self, Any, None]:

        """
        Abstract generator that is used to iterate through various run configurations. For example,
        this can be used to create a generator that iterates through each model point & scenario combination.

        :return: Generator that iterates through data sources.
        """

        ...
