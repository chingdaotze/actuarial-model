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
    Data source collection that contains premiums.
    """

    def __init__(
        self,
        data: List[Dict]
    ):
        """
        Constructor method. Generates premium data sources from a list of dictionaries.

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
