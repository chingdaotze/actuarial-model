from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    projection_entity_init,
    take_snapshot
)
from src.system.date import date_to_str
from src.system.logger import logger

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource
from src.data_sources.annuity.model_points.model_point import ModelPoint as ModelPointDataSource


class PremiumValues(
    ProjectionValues
):

    def __init__(
        self,
        premium_amount: float
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.premium_amount: float = premium_amount
        self.premium_age = relativedelta()

        self.surrender_charge_rate: float = 0.0
        self.surrender_charge_quote: float = 0.0
        self.surrender_charge_assessed: float = 0.0


class Premium(
    ProjectionEntity
):

    data_sources: AnnuityDataSources
    values: PremiumValues

    @projection_entity_init
    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        account_data_source: AccountDataSource
    ):

        premium_data_source = None

        if init_t in account_data_source.premiums:

            premium_data_source = account_data_source.premiums[
                init_t
            ]

        else:

            logger.raise_expr(
                expr=KeyError(
                    f'Could not find a premium on: {date_to_str(target_date=init_t)} '
                    f'for account: {account_data_source.id} !'
                )
            )

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources,
            values=PremiumValues(
                premium_amount=premium_data_source.premium_amount
            )
        )

        self.account_id: str = account_data_source.id

        self.model_point: ModelPointDataSource = self.data_sources.model_point

    def __str__(
        self
    ) -> str:

        return f'account_{self.account_id}_premium_{date_to_str(target_date=self.init_t)}'

    @property
    def surrender_charge_rate(
        self
    ) -> float:

        surrender_charge_rate = self.data_sources.product.base_product.surrender_charge.surrender_charge_rate(
            policy_year=self.values.premium_age.years,
            product_name=self.model_point.product_name
        )

        return surrender_charge_rate

    @property
    def surrender_charge_quote(
        self,
    ) -> float:

        surrender_charge_quote = self.values.premium_amount * self.surrender_charge_rate

        return surrender_charge_quote

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        next_t = t + duration

        self.values.premium_age = relativedelta(
            dt1=self.init_t,
            dt2=next_t
        )

        self.values.surrender_charge_rate = self.surrender_charge_rate
        self.values.surrender_charge_quote = self.surrender_charge_quote
