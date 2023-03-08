from abc import ABC

from pandas import DataFrame


class DataSourceBase(
    ABC
):

    """
    Abstract class that represents a data source. A data source caches data from an external source,
    then provides convenience methods to access the cache.
    """

    def __init__(
        self
    ):

        self.cache: DataFrame = DataFrame()
