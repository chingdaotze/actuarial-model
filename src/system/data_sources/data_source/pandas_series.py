from pandas import Series

from src.system.constants import DEFAULT_COL
from src.system.data_sources.data_source.base import DataSourceBase


class DataSourcePandasSeries(
    DataSourceBase
):

    """
    Abstract data source for a Pandas Series. Inherit this class to implement a custom Pandas Series.
    """

    def __init__(
        self,
        data: Series
    ):

        DataSourceBase.__init__(
          self=self
        )

        self.cache = data.to_frame(
            name=DEFAULT_COL
        )
