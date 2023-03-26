from typing import Dict
from datetime import date

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL
from src.system.enums import AccountType

from src.data_sources.annuity.model_points.model_point.accounts.account.premiums import Premiums


class Account(
    DataSourcePythonDict
):

    def __init__(
        self,
        data: Dict
    ):

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

        self.premiums: Premiums = Premiums(
            data=data['premiums']
        )

    @property
    def id(
        self
    ) -> str:

        return self.cache[DEFAULT_COL]['id']

    @property
    def account_type(
        self
    ) -> AccountType:

        return AccountType(
            self.cache[DEFAULT_COL]['account_type']
        )

    @property
    def account_name(
        self
    ) -> str:

        return self.cache[DEFAULT_COL]['account_name']

    @property
    def account_value(
        self
    ) -> float:

        return self.cache[DEFAULT_COL]['account_value']

    @property
    def account_date(
        self
    ) -> date:

        return min(
            premium.premium_date for premium in self.premiums
        )
