from typing import List
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    take_init_snapshot,
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
        self.surrender_charge: float = 0.0


class Account(
    ProjectionEntity
):

    data_sources: AnnuityDataSources
    values: AccountValues

    @take_init_snapshot
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

        self.id: str = account_data_source.id

        self.premiums: List[Premium] = []

    def __str__(
        self
    ) -> str:

        return f'account_{self.id}'

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        # TODO: Add new premiums

        # TODO: Credit interest to existing premiums

        ...
