"""
:class:`Root data source <src.system.data_sources.DataSourcesRoot>` for the annuity model.
"""

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

    """
    :class:`Root data source <src.system.data_sources.DataSourcesRoot>` input package for the annuity model.
    This class contains all data sources (model inputs) for the annuity model.
    """

    economic_scenarios: EconomicScenarios                   #: Economic environment.
    model_points: ModelPoints                               #: Annuity model points.
    mortality: Mortality                                    #: Annuity mortality assumptions.
    policyholder_behaviors: PolicyholderBehaviors           #: Annuity policyholder behavior assumptions.
    product: Product                                        #: Annuity product assumptions.

    economic_scenario: EconomicScenario                     #: Current stochastic economic scenario.
    model_point: ModelPoint                                 #: Current model point.

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        """
        Constructor method. Initializes annuity inputs package.

        :param projection_parameters: Set of projection parameters that contains a resource directory.
        """

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

        """
        Generator that cycles through each model point and economic scenario combination, setting the
        :attr:`model_point` and :attr:`economic_scenario` attributes as it goes.

        :return: Data source, with cycling ``model_point`` and ``economic_scenario`` attributes.
        """

        for model_point in self.model_points:

            self.model_point = model_point

            for economic_scenario in self.economic_scenarios:

                self.economic_scenario = economic_scenario

                yield self
