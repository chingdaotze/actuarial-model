"""
:mod:`Data source <src.system.data_sources.data_source>` for a Guaranteed Minimum Death Benefit (GMDB) rider.
"""

from typing import Dict

from src.data_sources.annuity.model_points.model_point.riders.base import BaseRider


class Gmdb(
    BaseRider
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a Guaranteed Minimum Death Benefit (GMDB) rider.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes a GMDB rider based on data within an annuity model point file.

        :param data: Data for a GMDB rider.
        """

        BaseRider.__init__(
            self=self,
            data=data
        )
