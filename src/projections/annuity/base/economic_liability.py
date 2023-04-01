from src.system.projection import Projection
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.annuity import AnnuityDataSources

from src.projection_entities.economy import Economy
from src.projection_entities.products.annuity.contracts.base import Contract


class EconomicLiabilityProjection(
    Projection
):

    """
    Sample economic liability projection.
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

        self.economy: Economy = Economy(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

        self.contract: Contract = Contract(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

    def project_time_step(
        self
    ) -> None:

        self.economy.age_economy()

        self.contract.age_contract()

        self.contract.process_premiums()

        self.contract.credit_interest()

        self.contract.assess_charges()

        self.contract.update_cash_surrender_value()
