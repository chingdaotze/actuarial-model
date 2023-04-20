"""
:mod:`Data source <src.system.data_sources.data_source>` for the base lapse table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class BaseLapse(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the base lapse table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the base lapse table into cache.

        Relative path to the base lapse table:

        ``resource/annuity/policyholder_behaviors/base_lapse_rate.csv``

        :param path: Path to the base lapse table.
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys='policy_year',
            inplace=True
        )

    @use_latest_value
    def base_lapse_rate(
        self,
        policy_year: int
    ) -> float:

        """
        Returns a base lapse rate.

        :param policy_year: Policy year.
        :return: Base lapse rate.
        """

        return self.cache['lapse_rate'][policy_year]
