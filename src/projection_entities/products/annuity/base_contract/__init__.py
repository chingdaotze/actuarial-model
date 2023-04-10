from typing import List
from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.enums import (
    AccountType,
    Rider,
    DeathBenefitOptions
)
from src.system.logger import logger
from src.system.projection.scripts.get_xversaries import get_xversaries

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.accounts.account import Account as AccountDataSource
from src.projection_entities.people.annuitants import Annuitants
from src.projection_entities.people.annuitants.annuitant import Annuitant
from src.projection_entities.products.annuity.base_contract.account import Account
from src.projection_entities.products.annuity.base_contract.account.fa import FixedAccount
from src.projection_entities.products.annuity.base_contract.account.ia import IndexedAccount
from src.projection_entities.products.annuity.base_contract.account.va import SeparateAccount
from src.projection_entities.products.annuity.riders.gmwb import Gmwb
from src.projection_entities.products.annuity.riders.gmdb.base import GmdbBase
from src.projection_entities.products.annuity.riders.gmdb.rop import GmdbRop
from src.projection_entities.products.annuity.riders.gmdb.rav import GmdbRav
from src.projection_entities.products.annuity.riders.gmdb.mav import GmdbMav


class BaseContract(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    annuitants: Annuitants
    accounts: List[Account]
    riders: List[Gmwb | GmdbRop | GmdbRav | GmdbMav]

    quarterversaries: ProjectionValue
    monthiversaries: ProjectionValue
    anniversaries: ProjectionValue
    premium_new: ProjectionValue
    premium_cumulative: ProjectionValue
    interest_credited: ProjectionValue
    gmdb_charge: ProjectionValue
    gmwb_charge: ProjectionValue
    withdrawal: ProjectionValue
    account_value: ProjectionValue
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

        self.annuitants = Annuitants(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

        self.accounts = self._get_new_accounts(
            t1=self.init_t
        )

        self.riders = []

        for rider_data_source in self.data_sources.model_point.riders:

            if rider_data_source.rider_type == Rider.GUARANTEED_MINIMUM_WITHDRAWAL_BENEFIT:

                self.riders.append(
                    Gmwb(
                        time_steps=self.time_steps,
                        data_sources=self.data_sources,
                        gmwb_data_source=rider_data_source
                    )
                )

            elif rider_data_source.rider_type == Rider.GUARANTEED_MINIMUM_DEATH_BENEFIT:

                rider_type = self.data_sources.product.gmdb_rider.types.gmdb_type(
                    rider_name=rider_data_source.rider_name
                )

                if rider_type == DeathBenefitOptions.RETURN_OF_PREMIUM:

                    self.riders.append(
                        GmdbRop(
                            time_steps=self.time_steps,
                            data_sources=self.data_sources,
                            gmdb_data_source=rider_data_source
                        )
                    )

                elif rider_type == DeathBenefitOptions.ACCOUNT_VALUE_RATCHET:

                    self.riders.append(
                        GmdbMav(
                            time_steps=self.time_steps,
                            data_sources=self.data_sources,
                            gmdb_data_source=rider_data_source
                        )
                    )

                elif rider_type == DeathBenefitOptions.RETURN_OF_ACCOUNT_VALUE:

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
            init_value=[[]],
            print_values=False
        )

        self.monthiversaries = ProjectionValue(
            init_t=self.init_t,
            init_value=[[]],
            print_values=False
        )

        self.anniversaries = ProjectionValue(
            init_t=self.init_t,
            init_value=[[]],
            print_values=False
        )

        self.premium_new = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
        )

        self.premium_cumulative = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_new_premium()
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

        self.account_value = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_account_value()
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

    def _get_new_account(
        self,
        account_data_source: AccountDataSource
    ) -> Account:

        if account_data_source.account_type == AccountType.FIXED:

            return FixedAccount(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                account_data_source=account_data_source
            )

        elif account_data_source.account_type == AccountType.INDEXED:

            return IndexedAccount(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                account_data_source=account_data_source
            )

        elif account_data_source.account_type == AccountType.SEPARATE:

            return SeparateAccount(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                account_data_source=account_data_source
            )

        else:

            logger.raise_expr(
                expr=NotImplementedError(
                    f'Unhandled account type: {account_data_source.account_type} !'
                )
            )

    def _get_new_accounts(
        self,
        t1: date,
        t2: date = None
    ) -> List[Account]:

        if t2 is None:

            accounts = [
                self._get_new_account(account_data_source=account_data_source) for account_data_source
                in self.data_sources.model_point.accounts if t1 == account_data_source.account_date
            ]

        else:

            accounts = [
                self._get_new_account(account_data_source=account_data_source) for account_data_source
                in self.data_sources.model_point.accounts if t1 < account_data_source.account_date <= t2
            ]

        return accounts

    def _calc_new_premium(
        self
    ) -> float:

        return sum(
            [sub_account.premium_new for sub_account in self.accounts]
        )

    def _calc_account_value(
        self
    ) -> float:

        return sum(
            [sub_account.account_value for sub_account in self.accounts]
        )

    def _calc_surrender_charge(
        self
    ) -> float:

        return sum(
            [sub_account.surrender_charge for sub_account in self.accounts]
        )

    def _calc_cash_surrender_value(
        self
    ) -> float:

        return max(
            self.account_value - self.surrender_charge,
            0.0
        )

    @property
    def primary_annuitant(
        self
    ) -> Annuitant:

        return self.annuitants.primary_annuitant

    def age_contract(
        self
    ) -> None:

        # Update upcoming anniversaries
        self.monthiversaries[self.time_steps.t] = [get_xversaries(
            issue_date=self.data_sources.model_point.issue_date,
            start_date=self.time_steps.prev_t,
            end_date=self.time_steps.t,
            frequency=1
        )]

        self.quarterversaries[self.time_steps.t] = [get_xversaries(
            issue_date=self.data_sources.model_point.issue_date,
            start_date=self.time_steps.prev_t,
            end_date=self.time_steps.t,
            frequency=3
        )]

        self.anniversaries[self.time_steps.t] = [get_xversaries(
            issue_date=self.data_sources.model_point.issue_date,
            start_date=self.time_steps.prev_t,
            end_date=self.time_steps.t,
            frequency=12
        )]

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
            self.premium_cumulative[self.time_steps.t] = self.premium_cumulative + self.premium_new

            self.account_value[self.time_steps.t] = self._calc_account_value()

            self.update_cash_surrender_value()

        # Process premiums for riders
        for rider in self.riders:

            rider.process_premiums(
                base_contract=self
            )

    def credit_interest(
        self
    ) -> None:

        # Credit interest for each account
        interest_credited = 0.0

        for sub_account in self.accounts:

            sub_account.credit_interest()

            interest_credited += sub_account.interest_credited

        # Update values
        self.account_value[self.time_steps.t] = self._calc_account_value()
        self.interest_credited[self.time_steps.t] = interest_credited

        self.update_cash_surrender_value()

    def assess_charge(
        self,
        charge_amount: ProjectionValue,
        charge_account_name: str
    ) -> None:

        # Apply charge pro rata across accounts
        for sub_account in self.accounts:

            if self.account_value:

                pro_rata_factor = sub_account.account_value / self.account_value

            else:

                pro_rata_factor = 0.0

            pro_rata_charge = charge_amount * pro_rata_factor

            sub_account.process_charge(
                charge_amount=pro_rata_charge,
                charge_account_name=charge_account_name
            )

        # Update values
        charge_account = self.__dict__[charge_account_name]
        charge_account[self.time_steps.t] = charge_amount

        self.account_value[self.time_steps.t] = self._calc_account_value()
        self.update_cash_surrender_value()

    def assess_charges(
        self
    ) -> None:

        # Assess rider charges
        for rider in self.riders:

            rider.process_charge(
                base_contract=self
            )

    def process_withdrawal(
        self,
        withdrawal_amount: ProjectionValue
    ) -> None:

        # Apply withdrawal pro rata across accounts
        for sub_account in self.accounts:

            if self.account_value:

                pro_rata_factor = sub_account.account_value / self.account_value

            else:

                pro_rata_factor = 0.0

            pro_rata_withdrawal = withdrawal_amount * pro_rata_factor

            sub_account.process_withdrawal(
                withdrawal_amount=pro_rata_withdrawal
            )

        # Update values
        self.withdrawal[self.time_steps.t] = withdrawal_amount
        self.account_value[self.time_steps.t] = self._calc_account_value()
        self.update_cash_surrender_value()

    def process_withdrawals(
        self
    ) -> None:

        for rider in self.riders:

            if isinstance(rider, Gmwb):

                rider.process_withdrawal(
                    base_contract=self
                )

    def update_gmdb_naar(
        self
    ) -> None:

        for rider in self.riders:

            if issubclass(type(rider), GmdbBase):

                rider.update_net_amount_at_risk(
                    base_contract=self
                )

    def update_cash_surrender_value(
        self
    ) -> None:

        for sub_account in self.accounts:

            sub_account.update_surrender_charge()

        self.surrender_charge[self.time_steps.t] = self._calc_surrender_charge()
        self.cash_surrender_value[self.time_steps.t] = self._calc_cash_surrender_value()
