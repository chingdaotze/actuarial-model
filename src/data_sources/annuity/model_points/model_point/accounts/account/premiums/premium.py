"""
:mod:`Data source <src.system.data_sources.data_source>` for a single premium.
"""

from typing import Dict
from datetime import date

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.date import str_to_date
from src.system.constants import DEFAULT_COL


class Premium(
    DataSourcePythonDict
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a single premium.
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
    def premium_date(
        self
    ) -> date:

        """
        Date that this premium was / will be paid.

        :return: Premium date.
        """

        return str_to_date(
            target_str=self.cache[DEFAULT_COL]['date']
        )

    @property
    def premium_amount(
        self
    ) -> float:

        """
        Premium payment dollar amount.

        :return: Premium payment amount.
        """

        return self.cache[DEFAULT_COL]['amount']
