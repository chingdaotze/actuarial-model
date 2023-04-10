from datetime import date

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.date import str_to_date


class MortalityImprovementDates(
    DataSourceCsvFile
):

    """
    Adjustments to the mortality improvement table.
    """

    def __init__(
        self,
        path: str
    ):

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys='name',
            inplace=True
        )

    @property
    def mortality_improvement_start_date(
        self
    ) -> date:

        """
        Returns the mortality improvement start date, which is used to adjust the Scale G2 mortality table.

        :return:
        """

        return str_to_date(
            target_str=self.cache['value']['mortality_improvement_start_date']
        )

    @property
    def mortality_improvement_end_date(
        self
    ) -> date:

        """
        Returns the mortality improvement end date, which is used to adjust the Scale G2 mortality table.

        :return:
        """

        return str_to_date(
            target_str=self.cache['value']['mortality_improvement_end_date']
        )
