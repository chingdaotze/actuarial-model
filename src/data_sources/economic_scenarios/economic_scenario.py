from datetime import date

from pandas import DataFrame

from src.system.data_sources.data_source.pandas_data_frame import DataSourcePandasDataFrame


class EconomicScenario(
    DataSourcePandasDataFrame
):

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
            keys='DATE',
            inplace=True
        )

    def get_rate(
        self,
        name: str,
        as_of: date
    ) -> float:

        return self.cache[name][as_of]
