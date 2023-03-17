from os.path import (
    join,
    isdir
)

from src.system.logger import logger
from src.system.data_sources import DataSources
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.economic_scenarios import EconomicScenarios
from src.data_sources.annuity.model_points import ModelPoints


class AnnuityDataSources(
    DataSources
):

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        DataSources.__init__(
            self=self,
            projection_parameters=projection_parameters
        )

        # Create path to annuity resource package
        self.path: str = join(
            self.projection_parameters.resource_dir_path,
            'annuity'
        )

        if not isdir(self.path):

            logger.raise_expr(
                expr=NotADirectoryError(
                    f'Could not locate a valid directory at this location: {self.path} to compile annuity data sources!'
                )
            )

        # Economic scenarios
        self.economic_scenarios: EconomicScenarios = EconomicScenarios(
            path=join(
                self.path,
                'economic_scenarios.csv'
            )
        )

        # Model points
        self.model_points: ModelPoints = ModelPoints(
            path=join(
                self.path,
                'model_points.json'
            )
        )

        pass
