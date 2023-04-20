"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that contains premium payments into a particular
:class:`account <src.data_sources.annuity.model_points.model_point.accounts.account.Account>`.
"""

from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection

from src.data_sources.annuity.model_points.model_point.accounts.account.premiums.premium import Premium


class Premiums(
    DataSourceCollection
):
    """
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
    that contains premium payments into a particular
    :class:`account <src.data_sources.annuity.model_points.model_point.accounts.account.Account>`.
    """

    def __init__(
        self,
        data: List[Dict]
    ):
        """
        Constructor method. Initializes a collection of premiums based on data within an annuity model point file,
        organized by
        :attr:`premium date <src.data_sources.annuity.model_points.model_point.accounts.account.premiums.premium.Premium.premium_date>`.

        :param data:
        """

        DataSourceCollection.__init__(
            self=self
        )

        for row in data:

            instance = Premium(
                data=row
            )

            self[instance.premium_date] = instance
