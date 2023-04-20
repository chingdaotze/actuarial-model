"""
Python `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_-based data source.
"""

from typing import Dict

from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase
from src.system.constants import DEFAULT_COL


class DataSourcePythonDict(
    DataSourceBase
):

    """
    Abstract data source for a Python `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_.
    Inherit this class to implement a custom Python dictionary data source.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Copies data from input
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_ into the cache.

        :param data: Input dictionary.
        """

        DataSourceBase.__init__(
            self=self
        )

        self.cache = DataFrame.from_dict(
            data=data,
            orient='index',
            columns=[DEFAULT_COL]
        )
