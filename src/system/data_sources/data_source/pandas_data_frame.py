from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase


class DataSourcePandasDataFrame(
    DataSourceBase
):

    """
    Abstract data source for a Pandas DataFrame. Inherit this class to implement a custom Pandas DataFrame.
    """

    def __init__(
        self,
        data: DataFrame
    ):

        DataSourceBase.__init__(
          self=self
        )

        self.cache = data
