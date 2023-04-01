from typing import Dict

from src.data_sources.annuity.model_points.model_point.riders.base import BaseRider


class Gmdb(
    BaseRider
):

    """
    Data source that represents a Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
    """

    def __init__(
        self,
        data: Dict
    ):

        BaseRider.__init__(
            self=self,
            data=data
        )
