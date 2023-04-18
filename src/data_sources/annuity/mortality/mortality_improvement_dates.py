"""
:mod:`Data source <src.system.data_sources.data_source>` for mortality improvement date model assumptions.
"""

from datetime import date

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.date import str_to_date


class MortalityImprovementDates(
    DataSourceCsvFile
):

    """
    Scale G2 mortality improvement assumptions. Scale G2 is based on time elapsed since the table was created.
    These assumptions are required to calculate the final mortality improvement rate.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the assumption table into cache.

        Relative path to the assumption table:

        ``resource/annuity/mortality/mortality_improvement_projection_scale_g2_dates.csv``

        :param path: Path to assumption table.
        """

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

        :return: Mortality improvement start date.
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

        :return: Mortality improvement end date.
        """

        return str_to_date(
            target_str=self.cache['value']['mortality_improvement_end_date']
        )
