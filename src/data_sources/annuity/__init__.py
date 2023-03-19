from os.path import join

from src.system.data_sources import DataSourcesRoot
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import logger
from src.system.data_sources.namespace import DataSourceNamespace


from src.data_sources.economic_scenarios import EconomicScenarios
from src.data_sources.annuity.model_points import ModelPoints
from src.data_sources.annuity.mortality import Mortality
from src.data_sources.annuity.policyholder_behaviors import PolicyholderBehaviors
from src.data_sources.annuity.product import Product


class AnnuityDataSources(
    DataSourcesRoot
):

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        DataSourcesRoot.__init__(
            self=self,
            projection_parameters=projection_parameters
        )

        DataSourceNamespace.__init__(
            self=self,
            path=join(
                self.projection_parameters.resource_dir_path,
                'annuity'
            )
        )

        logger.print(
            message=f'Compiling annuity data sources from: {self.path} ...'
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

        # Mortality
        self.mortality: Mortality = Mortality(
            path=join(
                self.path,
                'mortality'
            )
        )

        # Policyholder behaviors
        self.policyholder_behaviors: PolicyholderBehaviors = PolicyholderBehaviors(
            path=join(
                self.path,
                'policyholder_behaviors'
            )
        )

        # Product
        self.product: Product = Product(
            path=join(
                self.path,
                'product'
            )
        )
