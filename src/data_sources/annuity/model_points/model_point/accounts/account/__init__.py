"""
:mod:`Data source <src.system.data_sources.data_source>` for a single account.
"""

from typing import Dict
from datetime import date

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL
from src.system.enums import AccountType

from src.data_sources.annuity.model_points.model_point.accounts.account.premiums import Premiums


class Account(
    DataSourcePythonDict
):

    premiums: Premiums  #: Premiums associated with this account.

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes a collection of premiums based on data within an annuity model point file.

        :param data: Data for a single account.
        """

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

        self.premiums = Premiums(
            data=data['premiums']
        )

    @property
    def id(
        self
    ) -> str:

        """
        Unique identifier for a single account. For example, this could be a
        `CUSIP <https://en.wikipedia.org/wiki/CUSIP>`_ or a
        `GUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_.

        :return: Account ID.
        """

        return self.cache[DEFAULT_COL]['id']

    @property
    def account_type(
        self
    ) -> AccountType:

        """
        Account type. This field is currently used to indicate crediting strategies for a particular account.

        :return: Account type.
        """

        return AccountType(
            self.cache[DEFAULT_COL]['account_type']
        )

    @property
    def account_name(
        self
    ) -> str:

        """
        Human-readable account name.

        :return: Friendly account name.
        """

        return self.cache[DEFAULT_COL]['account_name']

    @property
    def account_value(
        self
    ) -> float:

        """
        Current account value. For new business model points, this should always be 0.0.

        :return: Account value.
        """

        return self.cache[DEFAULT_COL]['account_value']

    @property
    def account_date(
        self
    ) -> date:

        """
        Date the account was, or will be opened.

        :return: Account opening date.
        """

        return min(
            premium.premium_date for premium in self.premiums
        )
