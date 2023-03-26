from typing import List
from pandas import to_datetime

from src.system.data_sources.collection import DataSourceCollection
from src.system.data_sources.data_source.file_csv import DataSourceCsvFile

from src.data_sources.economic_scenarios.economic_scenario import EconomicScenario


class EconomicScenarios(
    DataSourceCsvFile,
    DataSourceCollection
):

    """
    Data source collection that holds multiple stochastic economic scenarios.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor that reads data from a CSV file, and generates economic scenarios.

        :param path:
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        DataSourceCollection.__init__(
            self=self
        )

        # Construct scenarios
        self.cache['t'] = to_datetime(
            self.cache['t']
        ).dt.date

        self.cache.set_index(
            keys=['path', 't'],
            inplace=True
        )

        self.rates: List[str] = list(self.cache.columns)

        for scenario_index in self.cache.index.levels[0].unique():

            instance = EconomicScenario(
                data=self.cache.loc[scenario_index],
                scenario_index=scenario_index
            )

            self[instance.scenario_index] = instance
