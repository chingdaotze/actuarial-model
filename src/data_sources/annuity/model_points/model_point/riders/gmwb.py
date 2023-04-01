from typing import Dict
from datetime import date

from src.data_sources.annuity.model_points.model_point.riders.base import BaseRider
from src.system.constants import DEFAULT_COL
from src.system.date import str_to_date


class Gmwb(
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

    @property
    def benefit_base(
        self
    ) -> float:

        """
        GMWB Benefit Base, typically used as a basis for GMWB withdrawals.

        :return:
        """

        return self.cache[DEFAULT_COL]['benefit_base']

    @property
    def first_withdrawal_date(
        self
    ) -> date | None:

        """
        GMWB Benefit Base, typically used as a basis for GMWB withdrawals.

        :return:
        """

        return_value = self.cache[DEFAULT_COL]['first_withdrawal_date']

        if return_value is not None:

            return_value = str_to_date(
                target_str=return_value
            )

        return return_value
