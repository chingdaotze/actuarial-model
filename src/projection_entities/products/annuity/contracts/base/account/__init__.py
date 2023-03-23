from abc import ABC, abstractmethod
from typing import List
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    projection_entity_init,
    take_snapshot
)

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource
from src.projection_entities.products.annuity.contracts.base.account.premium import Premium


class AccountValues(
    ProjectionValues
):

    def __init__(
        self
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.account_value: float = 0.0
        self.interest_credited: float = 0.0
        self.surrender_charge_quote: float = 0.0


class Account(
    ProjectionEntity,
    ABC
):

    data_sources: AnnuityDataSources
    values: AccountValues

    @projection_entity_init
    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        account_data_source: AccountDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources,
            values=AccountValues()
        )

        self.account_data_source: AccountDataSource = account_data_source

        self.premiums: List[Premium] = []

    def __str__(
        self
    ) -> str:

        return f'account_{self.account_data_source.id}'

    @property
    def surrender_charge_quote(
        self
    ) -> float:

        surrender_charge_quote = 0.0

        for subpay in self.premiums:

            surrender_charge_quote += subpay.surrender_charge_quote

        surrender_charge_quote = min(
            surrender_charge_quote,
            self.values.account_value
        )

        return surrender_charge_quote

    @abstractmethod
    def credit_interest(
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

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        next_t = t + duration

        # Add new premiums
        if next_t in self.account_data_source.premiums.keys:

            subpay = Premium(
                init_t=next_t,
                data_sources=self.data_sources,
                account_data_source=self.account_data_source
            )

            self.premiums.append(
                subpay
            )

            self.values.account_value += subpay.values.premium_amount

        # Credit interest to account
        self.values.interest_credited = self.credit_interest(
            t=t,
            duration=duration
        )

        self.values.account_value += self.values.interest_credited

        # Calculate surrender charge quote
        self.values.surrender_charge_quote = self.surrender_charge_quote
