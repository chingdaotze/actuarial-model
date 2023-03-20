from src.system.projection import Projection
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.economy.index import Index


class EconomicLiabilityProjection(
    Projection
):

    """
    Sample Variable Annuity economic liability projection.
    """

    data_sources: AnnuityDataSources

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_sources: AnnuityDataSources
    ):

        Projection.__init__(
            self=self,
            projection_parameters=projection_parameters,
            data_sources=data_sources
        )

        self.index = Index(
            projection_parameters=self.projection_parameters,
            economic_scenario=self.data_sources.economic_scenarios[0],
            index_name='SPX'
        )

    def project_time_step(
        self
    ) -> None:

        self.index.project(
            t=self.t,
            duration=self.projection_parameters.time_step
        )
