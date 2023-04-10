from dateutil.relativedelta import relativedelta

from src.projection_entities.products.annuity.base_contract.account import Account

from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource


class FixedAccount(
    Account
):

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        account_data_source: AccountDataSource
    ):

        Account.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources,
            account_data_source=account_data_source
        )

    def credit_interest(
        self
    ) -> None:

        crediting_rate = self.data_sources.product.base_product.crediting_rate.fixed.crediting_rate(
            account_name=self.account_data_source.account_name
        )

        elapsed_days = (self.time_steps.t - self.time_steps.prev_t).days

        days_in_year = self._calc_days_in_year()

        crediting_rate *= (elapsed_days / days_in_year)

        self.interest_credited[self.time_steps.t] = self.account_value * crediting_rate

        self.account_value[self.time_steps.t] = self.account_value + self.interest_credited
