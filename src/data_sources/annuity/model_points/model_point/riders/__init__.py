from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection
from src.system.logger import logger

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

            if base_rider.rider_type == 'gmwb':

                instance = Gmwb(
                    data=row
                )

            elif base_rider.rider_type == 'gmdb':

                instance = Gmdb(
                    data=row
                )

            else:

                logger.raise_expr(
                    expr=NotImplementedError(
                        f'Unhandled rider_type: {base_rider.rider_type} !'
                    )
                )

            self[index] = instance
