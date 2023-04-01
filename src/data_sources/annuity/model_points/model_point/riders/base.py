from typing import Dict

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL


class BaseRider(
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
    def rider_type(
        self
    ) -> float:
        """
        GMWB Benefit Base, typically used as a basis for GMWB withdrawals.

        :return:
        """

        return self.cache[DEFAULT_COL]['rider_type']

    @property
    def rider_name(
        self
    ) -> str:

        """
        Human-readable rider name.

        :return:
        """

        return self.cache[DEFAULT_COL]['rider_name']
