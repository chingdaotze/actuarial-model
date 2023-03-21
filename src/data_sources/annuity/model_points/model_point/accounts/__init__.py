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
    Data source collection that contains accounts.
    """

    def __init__(
        self,
        data: List[Dict]
    ):

        """
        Constructor method. Generates account data sources from a list of dictionaries.

        :param data:
        """

        DataSourceCollection.__init__(
            self=self
        )

        for row in data:

            instance = Account(
                data=row
            )

            self[instance.id] = instance
