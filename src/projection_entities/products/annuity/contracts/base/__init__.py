from typing import List
from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.people.annuitant import Annuitant
from src.projection_entities.products.annuity.contracts.base.account import Account


class Contract(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.annuitants: List[Annuitant] = [
            Annuitant(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                annuitant_data_source=annuitant_data_source
            ) for annuitant_data_source in self.data_sources.model_point.annuitants
        ]

        self.accounts: List[Account] = self._get_new_accounts(
            t1=self.init_t
        )

        self.premium_new: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
        )

        self.premium_cumulative: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
        )

        self.account_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_account_value()
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

        self.surrender_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

        self.cash_surrender_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_cash_surrender_value()
        )

    def __str__(
        self
    ) -> str:

        return 'contract'

    def _get_new_accounts(
        self,
        t1: date,
        t2: date = None
    ) -> List[Account]:

        if t2 is None:

            accounts = [
                Account(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_data_source=account_data_source
                ) for account_data_source in self.data_sources.model_point.accounts
                if t1 == account_data_source.account_date
            ]

        else:

            accounts = [
                Account(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_data_source=account_data_source
                ) for account_data_source in self.data_sources.model_point.accounts
                if t1 < account_data_source.account_date <= t2
            ]

        return accounts

    def _calc_new_premium(
        self
    ) -> float:

        return sum(
            [sub_account.premium_new.latest_value for sub_account in self.accounts]
        )

    def _calc_account_value(
        self
    ) -> float:

        return sum(
            [sub_account.account_value.latest_value for sub_account in self.accounts]
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        return sum(
            [sub_account.surrender_charge.latest_value for sub_account in self.accounts]
        )

    def _calc_cash_surrender_value(
        self
    ) -> float:

        return max(
            self.account_value.latest_value - self.surrender_charge.latest_value,
            0.0
        )

    def update_annuitants(
        self
    ) -> None:

        for annuitant in self.annuitants:

            annuitant.update_attained_age()

    def process_premiums(
        self
    ) -> None:

        if self.time_steps.t != self.init_t:

            # Process premiums for existing accounts
            for sub_account in self.accounts:

                sub_account.process_premiums()

            # Get new accounts
            if self.time_steps.t != self.init_t:

                new_accounts = self._get_new_accounts(
                    t1=self.time_steps.prev_t,
                    t2=self.time_steps.t
                )

                self.accounts += new_accounts

            # Calculate new premium total
            self.premium_new[self.time_steps.t] = self._calc_new_premium()

            # Update values
            self.premium_cumulative[self.time_steps.t] = \
                self.premium_cumulative.latest_value + self.premium_new.latest_value

            self.account_value[self.time_steps.t] = self.account_value.latest_value + self.premium_new.latest_value

    def update_cash_surrender_value(
        self
    ) -> None:

        for sub_account in self.accounts:

            sub_account.update_surrender_charge()

        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()
        self.cash_surrender_value[self.time_steps.t] = self._calc_cash_surrender_value()
