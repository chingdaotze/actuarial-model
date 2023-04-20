"""
:mod:`Abstract data source <src.system.data_sources.data_source>` for a rider.
"""

from typing import Dict

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL


class BaseRider(
    DataSourcePythonDict
):

    """
    :mod:`Abstract data source <src.system.data_sources.data_source>` for a rider.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes an abstract rider based on data within an annuity model point file.

        :param data: Data for any single rider.
        """

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

    @property
    def rider_type(
        self
    ) -> str:

        """
        Rider type, used to indicate what kind of rider this is.

        :return: Rider type.
        """

        return self.cache[DEFAULT_COL]['rider_type']

    @property
    def rider_name(
        self
    ) -> str:

        """
        Human-readable rider name.

        :return: Rider name.
        """

        return self.cache[DEFAULT_COL]['rider_name']
