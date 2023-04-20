"""
Fixed interest account.
"""

from src.projection_entities.products.annuity.base_contract.account import Account

from src.system.projection.time_steps import TimeSteps
from src.system.date import calc_partial_years

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource


class FixedAccount(
    Account
):

    """
    Fixed interest account.
    """

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

        r"""
        Credits interest to the sub\-account, where the fixed crediting rate is from
        :meth:`~src.data_sources.annuity.product.base.crediting_rate.fixed.FixedCreditingRate.crediting_rate`.

        .. math::
            interest \, credited = account \, value \times crediting \, rate \times years \, elapsed

        :math:`years \, elapsed` is calculated using :func:`~src.system.date.calc_partial_years`.

        :return: Nothing
        """

        crediting_rate = self.data_sources.product.base_product.crediting_rate.fixed.crediting_rate(
            account_name=self.account_data_source.account_name
        )

        partial_years = calc_partial_years(
            dt1=self.time_steps.t,
            dt2=self.time_steps.prev_t
        )

        crediting_rate *= partial_years

        self.interest_credited[self.time_steps.t] = self.account_value * crediting_rate

        self.account_value[self.time_steps.t] = self.account_value + self.interest_credited
