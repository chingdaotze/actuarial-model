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

    def __init__(
        self
    ):

        """
        Constructor method. Declares an empty cache.
        """

        self.cache: DataFrame = DataFrame()
