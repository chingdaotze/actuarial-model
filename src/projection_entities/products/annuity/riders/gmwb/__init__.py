from typing import TYPE_CHECKING
from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmwb import Gmwb as GmwbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.contracts.base import Contract


class Gmwb(
    ProjectionEntity
):

    data_sources: AnnuityDataSources
    rider_name: str
    first_withdrawal_date: date
    benefit_base: ProjectionValue

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        gmwb_data_source: GmwbDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.rider_name = gmwb_data_source.rider_name
        self.first_withdrawal_date = gmwb_data_source.first_withdrawal_date

        self.benefit_base = ProjectionValue(
            init_t=self.init_t,
            init_value=gmwb_data_source.benefit_base
        )

    def __str__(
        self
    ) -> str:

        return 'contract.riders.gmwb'

    def process_premiums(
        self,
        base_contract: 'Contract'
    ) -> None:

        self.benefit_base[self.time_steps.t] = \
            self.benefit_base.latest_value + base_contract.premium_new[self.time_steps.t]

    def process_charge(
        self,
        base_contract: 'Contract'
    ) -> None:

        for _ in base_contract.quarterversaries.latest_value:

            gmwb_charge_rate = self.data_sources.product.gmwb_rider.gmwb_charge.charge_rate(
                product_name=self.rider_name
            )

            gmwb_charge = min(
                self.benefit_base.latest_value * (gmwb_charge_rate / 4.0),
                base_contract.account_value.latest_value
            )

            base_contract.assess_charge(
                charge_amount=gmwb_charge
            )

    def process_withdrawal(
        self,
        base_contract: 'Contract'
    ) -> None:

        if self.time_steps.t >= self.first_withdrawal_date:

            for _ in base_contract.monthiversaries.latest_value:

                # TODO: Start taking withdrawals

                pass
