from abc import ABC, abstractmethod
from typing import List
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
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
        init_t: date,
        data_sources: AnnuityDataSources,
        account_data_source: AccountDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources
        )

        self.account_data_source: AccountDataSource = account_data_source

        self.premiums: List[Premium] = self.get_new_premiums(
            t=self.init_t,
            duration=relativedelta()
        )

        self.account_value: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_total_premium()
        )

        self.interest_credited: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.surrender_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_surrender_charge()
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

        return f'account_{self.account_data_source.id}'

    def get_new_premiums(
        self,
        t: date,
        duration: relativedelta
    ) -> List[Premium]:

        next_t = t + duration

        premiums = [
            Premium(
                init_t=premium_date,
                data_sources=self.data_sources,
                account_id=self.account_data_source.id,
                premium_data_source=premium_data_source
            ) for premium_date, premium_data_source in self.account_data_source.premiums.items
            if t < premium_date <= next_t
        ]

        return premiums

    def calc_total_premium(
        self
    ) -> float:

        return sum(
            [subpay.premium_amount.latest_value for subpay in self.premiums]
        )

    def calc_surrender_charge(
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

    @abstractmethod
    def calc_interest_credited(
        self,
        t: date,
        duration: relativedelta
    ) -> float:

        """
        Abstract method that represents an interest crediting mechanism. Inherit and override to implement
        a custom crediting algorithm (e.g. RILA, separate account crediting, or indexed crediting).

        :param t:
        :param duration:
        :return:
        """

        ...
