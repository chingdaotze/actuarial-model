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

        self.accounts: List[Account] = self.get_new_accounts(
            t=self.init_t,
            duration=relativedelta()
        )

        self.account_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_account_value()
        )

        self.cash_surrender_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_surrender_charge()
        )

    def __str__(
        self
    ) -> str:

        return 'contract'

    def get_new_accounts(
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

    def calc_account_value(
        self
    ) -> float:

        return sum(
            [sub_account.account_value.latest_value for sub_account in self.accounts]
        )

    def calc_surrender_charge(
        self
    ) -> float:

        return sum(
            [sub_account.surrender_charge.latest_value for sub_account in self.accounts]
        )
