"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that holds all economic stochastic scenarios.
"""

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
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
    that holds all economic stochastic scenarios.
    """

    rates: List[str]    #: List of rates in the economic scenario file.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Reads data from a CSV file and instantiates economic scenarios, organized by
        :attr:`scenario index <src.data_sources.economic_scenarios.economic_scenario.EconomicScenario.scenario_index>`.

        Relative path to the economic scenario file:

        ``resource/annuity/economic_scenarios.csv``

        :param path: Path to an economic scenario file.
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

        self.rates = list(self.cache.columns)

        for scenario_index in self.cache.index.levels[0].unique():

            instance = EconomicScenario(
                data=self.cache.loc[scenario_index],
                scenario_index=scenario_index
            )

            self[instance.scenario_index] = instance
