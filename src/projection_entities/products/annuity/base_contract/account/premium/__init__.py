r"""
Premium payment within a sub\-account.
"""

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.date import (
    date_to_str,
    calc_whole_years
)

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account.premiums.premium import Premium as \
    PremiumDataSource


class Premium(
    ProjectionEntity
):

    """
    Premium payment.
    """

    data_sources: AnnuityDataSources

    _product_name: str
    _account_id: str

    premium_amount: ProjectionValue             #: Premium amount.
    premium_age: ProjectionValue                #: Time elapsed since premium was paid.
    surrender_charge_rate: ProjectionValue      #: Point-in-time surrender charge rate.
    surrender_charge: ProjectionValue           #: Point-in-time surrender charge amount.

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        account_id: str,
        premium_data_source: PremiumDataSource
    ):

        """
        Constructor method.

        :param time_steps: Projection-wide timekeeping object.
        :param data_sources: Annuity data sources.
        :param account_id: Parent account.
        :param premium_data_source: Premium data source to initialize this premium payment.
        """

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources,
            init_t=premium_data_source.premium_date
        )

        self._product_name = self.data_sources.model_point.product_name
        self._account_id = account_id

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
            init_value=self._calc_surrender_charge_rate()
        )

        self.surrender_charge: ProjectionValue = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

    def __str__(
        self
    ) -> str:

        return f'contract.account.{self._account_id}.premium.{date_to_str(target_date=self.init_t)}'

    @property
    def premium_year(
        self
    ) -> int:

        """
        Calculates the premium age in years, using :func:`~src.system.date.calc_whole_years`.

        :return: Premium age in years.
        """

        return calc_whole_years(
            dt1=self.time_steps.t,
            dt2=self.init_t
        )

    def _calc_surrender_charge_rate(
        self
    ) -> float:

        return self.data_sources.product.base_product.surrender_charge.surrender_charge_rate(
            policy_year=self.premium_year,
            product_name=self._product_name
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        return self.premium_amount * self.surrender_charge_rate

    def update_premium(
        self
    ) -> None:

        """
        Projects the premium forwards by one time step by updating :attr:`premium_age`, :attr:`surrender_charge_rate`,
        and :attr:`surrender_charge`.

        :return:
        """

        self.premium_age[self.time_steps.t] = relativedelta(
            dt1=self.time_steps.t,
            dt2=self.init_t
        )

        self.surrender_charge_rate[self.time_steps.t] = self._calc_surrender_charge_rate()
        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()
