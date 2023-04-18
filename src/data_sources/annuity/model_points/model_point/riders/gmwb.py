"""
:mod:`Data source <src.system.data_sources.data_source>` for a Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
"""

from typing import Dict
from datetime import date

from src.data_sources.annuity.model_points.model_point.riders.base import BaseRider
from src.system.constants import DEFAULT_COL
from src.system.date import str_to_date


class Gmwb(
    BaseRider
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes a GMWB rider based on data within an annuity model point file.

        :param data: Data for a GMWB rider.
        """

        BaseRider.__init__(
            self=self,
            data=data
        )

    @property
    def benefit_base(
        self
    ) -> float:

        """
        GMWB Benefit Base, typically used as a basis for GMWB withdrawals.

        :return: GMWB Benefit Base.
        """

        return self.cache[DEFAULT_COL]['benefit_base']

    @property
    def first_withdrawal_date(
        self
    ) -> date | None:

        """
        Withdrawal program start date. If this policy has no planned withdrawal program, return None.

        :return: Withdrawal program start date.
        """

        return_value = self.cache[DEFAULT_COL]['first_withdrawal_date']

        if return_value is not None:

            return_value = str_to_date(
                target_str=return_value
            )

        return return_value
