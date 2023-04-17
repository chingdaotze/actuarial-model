"""
Pandas `Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_-based data source.
"""

from pandas import Series

from src.system.constants import DEFAULT_COL
from src.system.data_sources.data_source.base import DataSourceBase


class DataSourcePandasSeries(
    DataSourceBase
):

    """
    Abstract data source for a Pandas `Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_.
    Inherit this class to implement a custom Pandas Series data source.
    """

    def __init__(
        self,
        data: Series
    ):

        """
        Constructor method. Copies data from input
        `Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_ into the cache.

        :param data: Input Series.
        """

        DataSourceBase.__init__(
          self=self
        )

        self.cache = data.to_frame(
            name=DEFAULT_COL
        )
