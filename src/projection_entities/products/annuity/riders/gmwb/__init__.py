"""
Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
"""

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

    """
    Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
    """

    data_sources: AnnuityDataSources
    _gmwb_data_source: GmwbDataSource

    benefit_base: ProjectionValue                   #: Benefit base, used as a basis for withdrawals.
    charge_rate: ProjectionValue                    #: Charge rate, used to calculate the charge amount.
    charge_amount: ProjectionValue                  #: Charge amount, assessed against the account value.
    withdrawal_program_active: ProjectionValue      #: Indicator to determine if the rider's withdrawal program has started.
    av_active_withdrawal_rate: ProjectionValue      #: Withdrawal rate when account value is positive.
    av_exhaust_withdrawal_rate: ProjectionValue     #: Withdrawal rate when account value is zero.
    withdrawal: ProjectionValue                     #: Withdrawal amount.
    claim: ProjectionValue                          #: Claim amount (withdrawals once account value is zero).

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        gmwb_data_source: GmwbDataSource
    ):

        """
        Constructor method.

        :param time_steps: Projection-wide timekeeping object.
        :param data_sources: Annuity data sources.
        :param gmwb_data_source: GMWB rider data source.
        """

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

        """
        Adds premiums paid from the base contract into the :attr:`benefit base <benefit_base>`.

        :param base_contract: Base contract.
        :return: Nothing.
        """

        self.benefit_base[self.time_steps.t] = \
            self.benefit_base + base_contract.premium_new

    def process_charge(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        r"""
        Every quarter, charges the base contract for the GMWB charge.

        .. math::
            GMWB \, charge = benefit \, base \times \frac{GMDB \, charge \, rate}{4}

        :math:`GMWB \, charge \, rate` is read from
        :meth:`~src.data_sources.annuity.product.gmwb.charge.GmwbCharge.charge_rate`.

        Applies charge to the base contract using
        :meth:`~src.projection_entities.products.annuity.base_contract.BaseContract.assess_charge`.

        :param base_contract: Base contract.
        :return: Nothing.
        """

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

        r"""
        Calculates withdrawal amount:

        .. math::
            withdrawal\, amount = withdrawal \, rate \times benefit \, base

        :math:`withdrawal \, rate` is read from
        :class:`~src.data_sources.annuity.product.gmwb.benefit.GmwbBenefit`.

        Applies withdrawal to the base contract using
        :meth:`~src.projection_entities.products.annuity.base_contract.BaseContract.process_withdrawal`.

        :param base_contract:
        :return:
        """

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
