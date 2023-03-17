from src.system.data_sources.collection import DataSourceCollection
from src.system.data_sources.data_source.file_csv import DataSourceCsvFile

from data_sources.economic_scenarios.economic_scenario import EconomicScenario


class EconomicScenarios(
    DataSourceCsvFile,
    DataSourceCollection
):

    def __init__(
        self,
        path: str
    ):

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        DataSourceCollection.__init__(
            self=self
        )

        # Construct scenarios
        self.cache.set_index(
            keys='PATH',
            inplace=True
        )

        for scenario_index in self.cache.index.unique():

            self[scenario_index] = EconomicScenario(
                data=self.cache.loc[scenario_index]
            )
