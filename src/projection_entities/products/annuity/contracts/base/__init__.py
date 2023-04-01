from typing import List
from datetime import date
from math import floor

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.logger import logger

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.people.annuitant import Annuitant
from src.projection_entities.products.annuity.contracts.base.account import Account
from src.projection_entities.products.annuity.riders.gmwb import Gmwb
from src.projection_entities.products.annuity.riders.gmdb.rop import GmdbRop
from src.projection_entities.products.annuity.riders.gmdb.rav import GmdbRav
from src.projection_entities.products.annuity.riders.gmdb.mav import GmdbMav


class Contract(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    annuitants: List[Annuitant]
    accounts: List[Account]
    riders: List[Gmwb | GmdbRop | GmdbRav | GmdbMav]

    quarterversaries: ProjectionValue
    monthiversaries: ProjectionValue
    anniversaries: ProjectionValue
    premium_new: ProjectionValue
    premium_cumulative: ProjectionValue
    account_value: ProjectionValue
    interest_credited: ProjectionValue
    gmdb_charge: ProjectionValue
    gmwb_charge: ProjectionValue
    withdrawal: ProjectionValue
    surrender_charge: ProjectionValue
    cash_surrender_value: ProjectionValue

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.annuitants = [
            Annuitant(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                annuitant_data_source=annuitant_data_source
            ) for annuitant_data_source in self.data_sources.model_point.annuitants
        ]

        self.accounts = self._get_new_accounts(
            t1=self.init_t
        )

        self.riders = []

        for rider_data_source in self.data_sources.model_point.riders:

            if rider_data_source.rider_type == 'gmwb':

                self.riders.append(
                    Gmwb(
                        time_steps=self.time_steps,
                        data_sources=self.data_sources,
                        gmwb_data_source=rider_data_source
                    )
                )

            elif rider_data_source.rider_type == 'gmdb':

                rider_type = self.data_sources.product.gmdb_rider.types.gmdb_type(
                    rider_name=rider_data_source.rider_name
                )

                if rider_type == 'rop':

                    self.riders.append(
                        GmdbRop(
                            time_steps=self.time_steps,
                            data_sources=self.data_sources,
                            gmdb_data_source=rider_data_source
                        )
                    )

                elif rider_type == 'mav':

                    self.riders.append(
                        GmdbRop(
                            time_steps=self.time_steps,
                            data_sources=self.data_sources,
                            gmdb_data_source=rider_data_source
                        )
                    )

                elif rider_type == 'rav':

                    self.riders.append(
                        GmdbRav(
                            time_steps=self.time_steps,
                            data_sources=self.data_sources,
                            gmdb_data_source=rider_data_source
                        )
                    )

                else:

                    logger.raise_expr(
                        expr=NotImplementedError(
                            f'Unhandled GMDB rider type: {rider_type} !'
                        )
                    )

        self.quarterversaries = ProjectionValue(
            init_t=self.init_t,
            init_value=[[]]
        )

        self.monthiversaries = ProjectionValue(
            init_t=self.init_t,
            init_value=[[]]
        )

        self.anniversaries = ProjectionValue(
            init_t=self.init_t,
            init_value=[[]]
        )

        self.premium_new = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
        )

        self.premium_cumulative = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
        )

        self.account_value = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_account_value()
        )

        self.interest_credited = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmdb_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.gmwb_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.withdrawal = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.surrender_charge = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_surrender_charge()
        )

        self.cash_surrender_value = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_cash_surrender_value()
        )

    def __str__(
        self
    ) -> str:

        return 'contract'

    def _get_new_accounts(
        self,
        t1: date,
        t2: date = None
    ) -> List[Account]:

        if t2 is None:

            accounts = [
                Account(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_data_source=account_data_source
                ) for account_data_source in self.data_sources.model_point.accounts
                if t1 == account_data_source.account_date
            ]

        else:

            accounts = [
                Account(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    account_data_source=account_data_source
                ) for account_data_source in self.data_sources.model_point.accounts
                if t1 < account_data_source.account_date <= t2
            ]

        return accounts

    def _calc_new_premium(
        self
    ) -> float:

        return sum(
            [sub_account.premium_new.latest_value for sub_account in self.accounts]
        )

    def _calc_account_value(
        self
    ) -> float:

        return sum(
            [sub_account.account_value.latest_value for sub_account in self.accounts]
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        return sum(
            [sub_account.surrender_charge.latest_value for sub_account in self.accounts]
        )

    def _calc_cash_surrender_value(
        self
    ) -> float:

        return max(
            self.account_value.latest_value - self.surrender_charge.latest_value,
            0.0
        )

    def _update_xversaries(
        self,
        xversaries: ProjectionValue,
        frequency: int
    ) -> None:

        issue_date = self.data_sources.model_point.issue_date

        start_date_range = relativedelta(
            dt1=self.time_steps.prev_t,
            dt2=issue_date
        )

        start_xversary_months = floor((start_date_range.years * 12 + start_date_range.months) / frequency) * frequency

        end_date_rate = relativedelta(
            dt1=self.time_steps.t,
            dt2=issue_date
        )

        end_xversary_months = floor((end_date_rate.years * 12 + end_date_rate.months) / frequency) * frequency

        max_xversary_date = issue_date + relativedelta(
            months=end_xversary_months
        )

        xversary_date = issue_date + relativedelta(
            months=start_xversary_months
        )

        xversary_dates = []

        while xversary_date < max_xversary_date:

            xversary_date += relativedelta(
                months=frequency
            )

            xversary_dates.append(
                xversary_date
            )

        xversaries[self.time_steps.t] = [xversary_dates]

    def age_contract(
        self
    ) -> None:

        # Update annuitants
        for annuitant in self.annuitants:

            annuitant.update_attained_age()

        # Update upcoming anniversaries
        self._update_xversaries(
            xversaries=self.monthiversaries,
            frequency=1
        )

        self._update_xversaries(
            xversaries=self.quarterversaries,
            frequency=3
        )

        self._update_xversaries(
            xversaries=self.anniversaries,
            frequency=12
        )

    def process_premiums(
        self
    ) -> None:

        if self.time_steps.t != self.init_t:

            # Process premiums for existing accounts
            for sub_account in self.accounts:

                sub_account.process_premiums()

            # Get new accounts
            if self.time_steps.t != self.init_t:

                new_accounts = self._get_new_accounts(
                    t1=self.time_steps.prev_t,
                    t2=self.time_steps.t
                )

                self.accounts += new_accounts

            # Calculate new premium total
            self.premium_new[self.time_steps.t] = self._calc_new_premium()

            # Update values
            self.premium_cumulative[self.time_steps.t] = \
                self.premium_cumulative.latest_value + self.premium_new.latest_value

            self.account_value[self.time_steps.t] = self._calc_account_value()
            self.update_cash_surrender_value()

    def credit_interest(
        self
    ) -> None:

        # Credit interest for each account
        for sub_account in self.accounts:

            sub_account.credit_interest()

        # Update values
        self.account_value[self.time_steps.t] = self._calc_account_value()
        self.update_cash_surrender_value()

    def assess_charge(
        self,
        charge_amount: float
    ) -> None:

        # Apply charge pro rata across accounts
        for sub_account in self.accounts:

            pro_rata_factor = sub_account.account_value.latest_value / self.account_value.latest_value
            pro_rata_charge = charge_amount * pro_rata_factor

            sub_account.process_charge(
                charge_amount=pro_rata_charge
            )

        # Update values
        self.account_value[self.time_steps.t] = self._calc_account_value()
        self.update_cash_surrender_value()

    def assess_charges(
        self
    ) -> None:

        pass

    def process_withdrawal(
        self
    ):

        pass

    def update_cash_surrender_value(
        self
    ) -> None:

        for sub_account in self.accounts:

            sub_account.update_surrender_charge()

        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()
        self.cash_surrender_value[self.time_steps.t] = self._calc_cash_surrender_value()
