from typing import TYPE_CHECKING

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.date import calc_whole_years

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmwb import Gmwb as GmwbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.base_contract import BaseContract


class Gmwb(
    ProjectionEntity
):

    data_sources: AnnuityDataSources
    _gmwb_data_source: GmwbDataSource

    benefit_base: ProjectionValue
    charge_rate: ProjectionValue
    charge_amount: ProjectionValue
    withdrawal_program_active: ProjectionValue
    av_active_withdrawal_rate: ProjectionValue
    av_exhaust_withdrawal_rate: ProjectionValue
    withdrawal: ProjectionValue
    claim: ProjectionValue

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

        self._gmwb_data_source: GmwbDataSource = gmwb_data_source

        self.benefit_base = ProjectionValue(
            init_t=self.init_t,
            init_value=self._gmwb_data_source.benefit_base
        )

        self.charge_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.charge_amount = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.withdrawal_program_active = ProjectionValue(
            init_t=self.init_t,
            init_value=False
        )

        self.av_active_withdrawal_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.av_exhaust_withdrawal_rate = ProjectionValue(
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
            self.benefit_base + base_contract.premium_new

    def process_charge(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        self.charge_rate[self.time_steps.t] = 0.0
        self.charge_amount[self.time_steps.t] = 0.0

        account_value = base_contract.account_value.latest_value

        for _ in base_contract.quarterversaries:

            self.charge_rate[self.time_steps.t] = self.data_sources.product.gmwb_rider.gmwb_charge.charge_rate(
                product_name=self._gmwb_data_source.rider_name
            )

            self.charge_amount[self.time_steps.t] = (
                self.charge_amount +
                min(
                    self.benefit_base * (self.charge_rate / 4.0),
                    account_value
                )
            )

            account_value -= self.charge_amount

        base_contract.assess_charge(
            charge_amount=self.charge_amount,
            charge_account_name='gmwb_charge'
        )

    def _set_withdrawal_program(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        if not self.withdrawal_program_active:

            # Determine whether withdrawal program starts
            if (
                    self._gmwb_data_source.first_withdrawal_date is not None and
                    self.time_steps.t >= self._gmwb_data_source.first_withdrawal_date
            ):

                self.withdrawal_program_active[self.time_steps.t] = True

            if not base_contract.account_value:

                self.withdrawal_program_active[self.time_steps.t] = True

            # Set withdrawal rates
            if self.withdrawal_program_active:

                primary_annuitant = base_contract.primary_annuitant

                age_first_withdrawal = calc_whole_years(
                    dt1=self._gmwb_data_source.first_withdrawal_date,
                    dt2=primary_annuitant.date_of_birth
                )

                self.av_active_withdrawal_rate[self.time_steps.t] = \
                    self.data_sources.product.gmwb_rider.gmwb_benefit.av_active_withdrawal_rate(
                        rider_name=self._gmwb_data_source.rider_name,
                        age_first_withdrawal=age_first_withdrawal
                    )

                self.av_exhaust_withdrawal_rate[self.time_steps.t] = \
                    self.data_sources.product.gmwb_rider.gmwb_benefit.av_exhaust_withdrawal_rate(
                        rider_name=self._gmwb_data_source.rider_name,
                        age_first_withdrawal=age_first_withdrawal
                    )

        # Roll previous values forward
        self.withdrawal_program_active[self.time_steps.t] = self.withdrawal_program_active
        self.av_active_withdrawal_rate[self.time_steps.t] = self.av_active_withdrawal_rate
        self.av_exhaust_withdrawal_rate[self.time_steps.t] = self.av_exhaust_withdrawal_rate

    def process_withdrawal(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        self._set_withdrawal_program(
            base_contract=base_contract
        )

        self.withdrawal[self.time_steps.t] = 0.0
        self.claim[self.time_steps.t] = 0.0

        if self.withdrawal_program_active:

            account_value = base_contract.account_value.latest_value

            for _ in base_contract.monthiversaries:

                if account_value:

                    # Take withdrawal at AV active rate
                    withdrawal_requested = self.av_active_withdrawal_rate * self.benefit_base

                    self.withdrawal += min(
                        withdrawal_requested,
                        account_value
                    )

                    account_value -= self.withdrawal

                    # Take remainder as claim
                    self.claim[self.time_steps.t] = withdrawal_requested - self.withdrawal

                else:

                    # Take claim at AV exhaust rate
                    self.claim[self.time_steps.t] = self.av_exhaust_withdrawal_rate * self.benefit_base

        base_contract.process_withdrawal(
            withdrawal_amount=self.withdrawal
        )
