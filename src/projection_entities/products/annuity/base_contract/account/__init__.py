from abc import (
    ABC,
    abstractmethod
)
from typing import List
from datetime import date
from calendar import isleap

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import (
    ProjectionValue,
    compare_latest_value
)

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource
from src.projection_entities.products.annuity.base_contract.account.premium import Premium


class Account(
    ProjectionEntity,
    ABC
):

    data_sources: AnnuityDataSources
    account_data_source: AccountDataSource
    premiums: List[Premium]

    premium_new: ProjectionValue
    premium_cumulative: ProjectionValue
    account_value: ProjectionValue
    interest_credited: ProjectionValue
    gmdb_charge: ProjectionValue
    gmwb_charge: ProjectionValue
    withdrawal: ProjectionValue
    surrender_charge: ProjectionValue

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

        self.account_data_source = account_data_source

        self.premiums = self._get_new_premiums(
            t1=self.init_t
        )

        self.premium_new = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.premium_cumulative = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.interest_credited = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmdb_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmwb_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.withdrawal = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.account_value = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.surrender_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

    def __str__(
        self
    ) -> str:

        return f'contract.account.{self.account_data_source.id}'

    def _calc_days_in_year(
        self
    ) -> int:

        if not isleap(year=self.time_steps.t.year):

            days_in_year = 365

        else:

            days_in_year = 366  # Leap year

        return days_in_year

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
            [subpay.premium_amount for subpay in self.premiums]
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        surrender_charge = sum(
            [subpay.surrender_charge for subpay in self.premiums]
        )

        surrender_charge = min(
            surrender_charge,
            self.account_value,
            key=compare_latest_value
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
                [subpay.premium_amount for subpay in new_premiums]
            )

            # Update values
            self.premium_cumulative[self.time_steps.t] = self.premium_cumulative + self.premium_new

            self.account_value[self.time_steps.t] = self.account_value + self.premium_new

    @abstractmethod
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
        charge_amount: float,
        charge_account_name: str
    ) -> None:

        charge_account = self.__dict__[charge_account_name]
        charge_account[self.time_steps.t] = charge_amount

        self.account_value[self.time_steps.t] = self.account_value - charge_amount

    def process_withdrawal(
        self,
        withdrawal_amount: float
    ) -> None:

        self.withdrawal[self.time_steps.t] = withdrawal_amount
        self.account_value[self.time_steps.t] = self.account_value - self.withdrawal

    def update_surrender_charge(
        self
    ) -> None:

        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()