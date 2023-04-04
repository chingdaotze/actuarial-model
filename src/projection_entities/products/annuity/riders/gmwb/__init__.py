from typing import TYPE_CHECKING
from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmwb import Gmwb as GmwbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.base_contract import BaseContract


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

        self.charge_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.charge_amount = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.withdrawal = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.claim = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return 'contract.riders.gmwb'

    def process_premiums(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        self.benefit_base[self.time_steps.t] = \
            self.benefit_base.latest_value + base_contract.premium_new.latest_value

    def process_charge(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        if base_contract.quarterversaries.latest_value:

            for _ in base_contract.quarterversaries.latest_value:

                self.charge_rate[self.time_steps.t] = self.data_sources.product.gmwb_rider.gmwb_charge.charge_rate(
                    product_name=self.rider_name
                )

                self.charge_amount[self.time_steps.t] = min(
                    self.benefit_base.latest_value * (self.charge_rate.latest_value / 4.0),
                    base_contract.account_value.latest_value
                )

                base_contract.assess_charge(
                    charge_amount=self.charge_amount.latest_value,
                    charge_account_name='gmwb_charge'
                )

        else:

            self.charge_amount[self.time_steps.t] = 0.0

            base_contract.assess_charge(
                charge_amount=self.charge_amount.latest_value,
                charge_account_name='gmwb_charge'
            )

    def process_withdrawal(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        if self.time_steps.t >= self.first_withdrawal_date:

            for _ in base_contract.monthiversaries.latest_value:

                # TODO: Start taking withdrawals

                pass
