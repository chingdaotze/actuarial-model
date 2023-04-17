"""
Pandas `DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_-based data source.
"""

from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase


class DataSourcePandasDataFrame(
    DataSourceBase
):

    """
    Abstract data source for a Pandas `DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_.
    Inherit this class to implement a custom Pandas DataFrame data source.
    """

    def __init__(
        self,
        data: DataFrame
    ):

        """
        Constructor method. Copies data (via assignment) from input
        `DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ into the cache.

        :param data: Input DataFrame.
        """

        DataSourceBase.__init__(
          self=self
        )

        self.cache = data
