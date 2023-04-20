"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that contains accounts for a particular
:class:`model point <src.data_sources.annuity.model_points.model_point.ModelPoint>`.
"""

from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection

from src.data_sources.annuity.model_points.model_point.accounts.account import Account


class Accounts(
    DataSourceCollection
):

    """
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>` that
    contains all accounts. Accounts are typically associated with a
    :class:`model point <src.data_sources.annuity.model_points.model_point.ModelPoint>` where one model point
    can have multiple accounts. For example, if a policyholder decides to invest in:

    - 20% SPX
    - 30% Bonds
    - 50% Money market

    We might model this as three distinct accounts.
    """

    def __init__(
        self,
        data: List[Dict]
    ):

        """
        Constructor method. Initializes a collection of accounts based on data within an annuity model point file,
        organized by :attr:`account ID <src.data_sources.annuity.model_points.model_point.accounts.account.Account.id>`.

        :param data: Data for multiple accounts.
        """

        DataSourceCollection.__init__(
            self=self
        )

        for row in data:

            instance = Account(
                data=row
            )

            self[instance.id] = instance
