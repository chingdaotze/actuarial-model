from typing import (
    Dict,
    Union
)
from datetime import date

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL
from src.system.date import str_to_date


class Gmwb(
    DataSourcePythonDict
):

    """
    Data source that represents a Guaranteed Minimum Withdrawal Benefit (GMWB) rider.
    """

    def __init__(
        self,
        data: Dict
    ):

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

    @property
    def rider_name(
        self
    ) -> str:

        """
        Human-readable rider name.

        :return:
        """

        return self.cache[DEFAULT_COL]['rider_name']

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
    ) -> Union[date, None]:

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
