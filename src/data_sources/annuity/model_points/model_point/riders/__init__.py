from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection
from src.system.logger import Logger
from src.system.enums import Rider

from src.data_sources.annuity.model_points.model_point.riders.base import BaseRider
from src.data_sources.annuity.model_points.model_point.riders.gmwb import Gmwb
from src.data_sources.annuity.model_points.model_point.riders.gmdb import Gmdb


class Riders(
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

        for index, row in enumerate(data):

            base_rider = BaseRider(
                data=row
            )

            instance = None

            if base_rider.rider_type == Rider.GUARANTEED_MINIMUM_WITHDRAWAL_BENEFIT:

                instance = Gmwb(
                    data=row
                )

            elif base_rider.rider_type == Rider.GUARANTEED_MINIMUM_DEATH_BENEFIT:

                instance = Gmdb(
                    data=row
                )

            else:

                Logger().raise_expr(
                    expr=NotImplementedError(
                        f'Unhandled rider_type: {base_rider.rider_type} !'
                    )
                )

            self[index] = instance
