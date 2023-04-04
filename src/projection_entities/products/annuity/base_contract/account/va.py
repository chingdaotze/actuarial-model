from dateutil.relativedelta import relativedelta

from src.projection_entities.products.annuity.base_contract.account import Account

from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource


class SeparateAccount(
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

        crediting_rate = 0

        elapsed_days = relativedelta(
            dt1=self.time_steps.t,
            dt2=self.time_steps.prev_t
        ).days

        self.interest_credited[self.time_steps.t] = self.account_value.latest_value * crediting_rate

        self.account_value[self.time_steps.t] = self.account_value.latest_value + self.interest_credited.latest_value
