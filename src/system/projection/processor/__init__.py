from abc import (
    ABC,
    abstractmethod
)
from typing import (
    List,
    Type
)
from copy import deepcopy
from os.path import splitext
from importlib import import_module

from src.system.projection import Projection
from src.system.projection.parameters import ProjectionParameters
from src.system.data_sources import DataSourcesRoot
from src.system.logger import logger


class ProjectionProcessor(
    ABC
):

    projection_parameters: ProjectionParameters
    projections: List[Projection]
    data_sources: DataSourcesRoot
    projection: Type

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        self.projection_parameters = projection_parameters

        # Create data sources
        logger.print(
            message=f'Compiling data sources from: {self.projection_parameters.data_source} ...'
        )

        self.data_sources = self._get_type(
            qualified_path=self.projection_parameters.data_source
        )(
            projection_parameters=self.projection_parameters
        )

        # Create projection objects
        logger.print(
            message=f'Compiling projections from: {self.projection_parameters.projection} ...'
        )

        self.projection = self._get_type(
            qualified_path=self.projection_parameters.projection
        )

        self.projections = []

        for configured_data_sources in self.data_sources.configured_data_sources():

            self.projections.append(
                self.projection(
                    projection_parameters=self.projection_parameters,
                    data_sources=deepcopy(
                        configured_data_sources
                    )
                )
            )

    @staticmethod
    def _get_type(
        qualified_path: str
    ) -> Type:

        """
        WARNING: Allows arbitrary code execution.

        Parses a string and returns a class definition that represents a projection object.

        :return:
        """

        module_path, class_name = splitext(
            qualified_path
        )

        module = import_module(
            name=module_path
        )

        class_def = module.__dict__[class_name[1:]]

        return class_def

    @staticmethod
    def run_projection(
        projection: Projection
    ) -> None:

        # Run projection
        projection.run_projection()

        # Write output
        projection.write_output()

    def setup_output(
        self
    ) -> None:

        logger.print(
            message=f'Setting up projection output ...'
        )

        for projection in self.projections:

            projection.setup_output()

    @abstractmethod
    def run_projections(
        self
    ) -> None:

        ...
