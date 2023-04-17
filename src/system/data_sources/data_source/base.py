"""
Abstract data source.
"""

from abc import ABC

from pandas import DataFrame


class DataSourceBase(
    ABC
):

    """
    Abstract class that represents a data source. A data source caches data from an external source,
    (like a file or database connection) then provides convenience methods to access the cache.
    Inherit this class to implement a custom data source.
    """

    cache: DataFrame  #: Internal cache, populated at runtime.

    def __init__(
        self
    ):

        """
        Constructor method. Declares an empty
        `DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ to use as a cache.
        """

        self.cache = DataFrame()
