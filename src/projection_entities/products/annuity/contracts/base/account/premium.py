from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    take_init_snapshot,
    take_snapshot
)
from src.system.date import date_to_str

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account.premiums.premium import Premium as \
    PremiumDataSource
from src.data_sources.annuity.model_points.model_point import ModelPoint as ModelPointDataSource


class PremiumValues(
    ProjectionValues
):

    def __init__(
        self,
        premium_date: date,
        premium_amount: float
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.premium_date: date = premium_date
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

    @take_init_snapshot
    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        premium_data_source: PremiumDataSource,
        account_id: str
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources,
            values=PremiumValues(
                premium_date=premium_data_source.premium_date,
                premium_amount=premium_data_source.premium_amount
            )
        )

        self.model_point: ModelPointDataSource = self.data_sources.model_point
        self.account_id: str = account_id

        self.calc_surrender_charge_quote()

    def __str__(
        self
    ) -> str:

        return f'account_{self.account_id}_premium_{date_to_str(target_date=self.init_t)}'

    def calc_surrender_charge_quote(
        self,
    ) -> None:

        self.values.surrender_charge_rate = self.data_sources.product.base_product.surrender_charge.\
            surrender_charge_rate(
                policy_year=self.values.premium_age.years,
                product_name=self.model_point.product_name
            )

        self.values.surrender_charge_quote = self.values.premium_amount * self.values.surrender_charge_rate

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        self.values.premium_age += duration
