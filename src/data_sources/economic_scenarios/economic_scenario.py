from datetime import date

from pandas import DataFrame

from src.system.data_sources.data_source.pandas_data_frame import DataSourcePandasDataFrame


class EconomicScenario(
    DataSourcePandasDataFrame
):

    """
    Data source that represents a single economic scenario.
    """

    def __init__(
        self,
        data: DataFrame
    ):

        DataSourcePandasDataFrame.__init__(
            self=self,
            data=data
        )

        self.cache.reset_index(
            drop=True,
            inplace=True
        )

        self.cache.set_index(
            keys='t',
            inplace=True
        )

    def get_rate(
        self,
        name: str,
        t: date
    ) -> float:

        """
        Convenience method to access data from the scenario file. Returns a rate from the scenario file.

        :param name:
        :param t:
        :return:
        """

        return self.cache[name][t]