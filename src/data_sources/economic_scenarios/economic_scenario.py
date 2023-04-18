"""
:mod:`Data source <src.system.data_sources.data_source>` for a single economic scenario.
"""

from datetime import date

from pandas import DataFrame

from src.system.data_sources.data_source.pandas_data_frame import DataSourcePandasDataFrame
from src.system.projection_entity.projection_value import use_latest_value


class EconomicScenario(
    DataSourcePandasDataFrame
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a single economic scenario.
    """

    scenario_index: int     #: Stochastic scenario number.

    def __init__(
        self,
        data: DataFrame,
        scenario_index: int
    ):

        """
        Constructor method. Initializes an economic scenario based on data within an economic scenario file.

        :param data: Economic scenario data.
        """

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
        Returns a rate from the scenario file.

        :param name: Rate name.
        :param t: Time step.
        :return: Rate.
        """

        return self.cache[name][t]
