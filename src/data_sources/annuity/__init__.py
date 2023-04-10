from os.path import join
from typing import (
    Generator,
    Self,
    Any
)

from src.system.data_sources import DataSourcesRoot
from src.system.projection.parameters import ProjectionParameters
from src.system.data_sources.namespace import DataSourceNamespace


from src.data_sources.economic_scenarios import EconomicScenarios
from src.data_sources.economic_scenarios.economic_scenario import EconomicScenario
from src.data_sources.annuity.model_points import ModelPoints
from src.data_sources.annuity.model_points.model_point import ModelPoint
from src.data_sources.annuity.mortality import Mortality
from src.data_sources.annuity.policyholder_behaviors import PolicyholderBehaviors
from src.data_sources.annuity.product import Product


class AnnuityDataSources(
    DataSourcesRoot
):

    economic_scenarios: EconomicScenarios
    model_points: ModelPoints
    mortality: Mortality
    policyholder_behaviors: PolicyholderBehaviors
    product: Product

    economic_scenario: EconomicScenario
    model_point: ModelPoint

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

        # Economic scenarios
        self.economic_scenarios = EconomicScenarios(
            path=join(
                self.path,
                'economic_scenarios.csv'
            )
        )

        # Model points
        self.model_points = ModelPoints(
            path=join(
                self.path,
                'model_points.json'
            )
        )

        # Mortality
        self.mortality = Mortality(
            path=join(
                self.path,
                'mortality'
            )
        )

        # Policyholder behaviors
        self.policyholder_behaviors = PolicyholderBehaviors(
            path=join(
                self.path,
                'policyholder_behaviors'
            )
        )

        # Product
        self.product = Product(
            path=join(
                self.path,
                'product'
            )
        )

    def configured_data_sources(
        self
    ) -> Generator[Self, Any, None]:

        for model_point in self.model_points:

            self.model_point = model_point

            for economic_scenario in self.economic_scenarios:

                self.economic_scenario = economic_scenario

                yield self
