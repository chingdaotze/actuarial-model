from typing import List
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.products.annuity.contracts.base.account import Account


class Contract(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources
        )

        self.accounts: List[Account] = self._get_new_accounts(
            t=self.init_t,
            duration=relativedelta()
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

        self.cash_surrender_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

        self.gmdb_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmwb_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return 'contract'

    def _get_new_accounts(
        self,
        t: date,
        duration: relativedelta
    ) -> List[Account]:

        next_t = t + duration

        accounts = [
            Account(
                init_t=account_data_source.account_date,
                data_sources=self.data_sources,
                account_data_source=account_data_source
            ) for account_data_source in self.data_sources.model_point.accounts
            if t < account_data_source.account_date <= next_t
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

    def process_premiums(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        next_t = t + duration

        # Process premiums for existing accounts
        for sub_account in self.accounts:

            sub_account.process_premiums(
                t=t,
                duration=duration
            )

        # Get new accounts
        new_accounts = self._get_new_accounts(
            t=t,
            duration=duration
        )

        self.accounts += new_accounts

        # Calculate new premium total
        self.premium_new[next_t] = self._calc_new_premium()

        # Update values
        self.premium_cumulative[next_t] = self.premium_new.latest_value + self.premium_new.latest_value
        self.account_value[next_t] = self.account_value.latest_value + self.premium_new.latest_value
