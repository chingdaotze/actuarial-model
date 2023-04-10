from datetime import date

from pandas import DataFrame

from src.system.data_sources.data_source.pandas_data_frame import DataSourcePandasDataFrame
from src.system.projection_entity.projection_value import use_latest_value


class EconomicScenario(
    DataSourcePandasDataFrame
):

    """
    Data source that represents a single economic scenario.
    """

    scenario_index: int

    def __init__(
        self,
        data: DataFrame,
        scenario_index: int
    ):

        DataSourcePandasDataFrame.__init__(
            self=self,
            data=data
        )

        self.scenario_index = scenario_index

    @use_latest_value
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
