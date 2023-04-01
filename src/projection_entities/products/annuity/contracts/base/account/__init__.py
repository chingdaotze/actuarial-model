from abc import ABC, abstractmethod
from typing import List
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource
from src.projection_entities.products.annuity.contracts.base.account.premium import Premium


class Account(
    ProjectionEntity,
    ABC
):

    data_sources: AnnuityDataSources

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        account_data_source: AccountDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources,
            init_t=account_data_source.account_date
        )

        self.account_data_source: AccountDataSource = account_data_source

        self.premiums: List[Premium] = self._get_new_premiums(
            t1=self.init_t
        )

        self.premium_new: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.premium_cumulative: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.account_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.interest_credited: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmdb_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmwb_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.withdrawal: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.surrender_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

    def __str__(
        self
    ) -> str:

        return f'contract.account.{self.account_data_source.id}'

    def _get_new_premiums(
        self,
        t1: date,
        t2: date = None
    ) -> List[Premium]:

        if t2 is None:

            premiums = [
                Premium(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_id=self.account_data_source.id,
                    premium_data_source=premium_data_source
                ) for premium_date, premium_data_source in self.account_data_source.premiums.items
                if t1 == premium_date
            ]

        else:

            premiums = [
                Premium(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_id=self.account_data_source.id,
                    premium_data_source=premium_data_source
                ) for premium_date, premium_data_source in self.account_data_source.premiums.items
                if t1 < premium_date <= t2
            ]

        return premiums

    def _calc_total_premium(
        self
    ) -> float:

        return sum(
            [subpay.premium_amount.latest_value for subpay in self.premiums]
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        surrender_charge = sum(
            [subpay.surrender_charge.latest_value for subpay in self.premiums]
        )

        surrender_charge = min(
            surrender_charge,
            self.account_value.latest_value
        )

        return surrender_charge

    def process_premiums(
        self
    ) -> None:

        if self.time_steps.t != self.init_t:

            # Age existing premiums
            for subpay in self.premiums:

                subpay.update_premium()

            # Get new premiums
            new_premiums = self._get_new_premiums(
                t1=self.time_steps.prev_t,
                t2=self.time_steps.t
            )

            self.premiums += new_premiums

            # Calculate new premium total
            self.premium_new[self.time_steps.t] = sum(
                [subpay.premium_amount.latest_value for subpay in new_premiums]
            )

            # Update values
            self.premium_cumulative[self.time_steps.t] = \
                self.premium_cumulative.latest_value + self.premium_new.latest_value

            self.account_value[self.time_steps.t] = self.account_value.latest_value + self.premium_new.latest_value

    def credit_interest(
        self
    ) -> None:

        """
        Abstract method that represents an interest crediting mechanism. Inherit and override to implement
        a custom crediting algorithm (e.g. RILA, separate account crediting, or indexed crediting).

        :return:
        """

        ...

    def process_charge(
        self,
        charge_amount: float
    ) -> None:

        self.account_value[self.time_steps.t] = self.account_value.latest_value - charge_amount

    def process_withdrawal(
        self,
        withdrawal_amount: float
    ) -> None:

        self.account_value[self.time_steps.t] = self.account_value.latest_value - withdrawal_amount

    def update_surrender_charge(
        self
    ) -> None:

        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()
