"""
:mod:`Data source <src.system.data_sources.data_source>` for the annuity annuitization table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class Annuitization(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the annuity annuitization table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the annuitization table into cache.

        Relative path to the annuitization table:

        ``resource/annuity/policyholder_behaviors/annuitization_rate.csv``

        :param path: Path to the annuitization table.
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys='attained_age',
            inplace=True
        )

    @use_latest_value
    def annuitization_rate(
        self,
        attained_age: int
    ) -> float:

        """
        Returns an annuitization rate.

        :param attained_age: Attained age.
        :return: Annuitization rate.
        """

        return self.cache['annuitization_rate'][attained_age]
