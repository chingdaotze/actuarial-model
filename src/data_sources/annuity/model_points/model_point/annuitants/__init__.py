from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection

from src.data_sources.annuity.model_points.model_point.annuitants.annuitant import Annuitant


class Annuitants(
    DataSourceCollection
):

    """
    Data source collection that represents one or more annuitants.
    """

    def __init__(
        self,
        data: List[Dict]
    ):

        """
        Constructor method. Generates annuitant data sources from a list of dictionaries.

        :param data:
        """

        DataSourceCollection.__init__(
            self=self
        )

        for row in data:

            self[row['id']] = Annuitant(
                data=row
            )
