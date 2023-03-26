from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.date import date_to_str

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account.premiums.premium import Premium as \
    PremiumDataSource


class Premium(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        account_id: str,
        premium_data_source: PremiumDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources
        )

        self._product_name: str = self.data_sources.model_point.product_name
        self._account_id: str = account_id

        self.premium_amount: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=premium_data_source.premium_amount
        )

        self.premium_age: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=relativedelta()
        )

        self.surrender_charge_rate: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_surrender_charge_rate()
        )

        self.surrender_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self.calc_surrender_charge()
        )

    def __str__(
        self
    ) -> str:

        return f'account_{self._account_id}_premium_{date_to_str(target_date=self.init_t)}'

    def calc_surrender_charge_rate(
        self
    ) -> float:

        return self.data_sources.product.base_product.surrender_charge.surrender_charge_rate(
            policy_year=self.premium_age.latest_value.years + 1,
            product_name=self._product_name
        )

    def calc_surrender_charge(
        self
    ) -> float:

        return self.premium_amount.latest_value * self.surrender_charge_rate.latest_value

    def update_premium(
        self,
        next_t: date
    ) -> None:

        self.premium_age[next_t] = relativedelta(
            dt1=self.init_t,
            dt2=next_t
        )

        self.surrender_charge_rate[next_t] = self.calc_surrender_charge_rate()
        self.surrender_charge[next_t] = self.calc_surrender_charge()
