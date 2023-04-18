"""
:mod:`Data source <src.system.data_sources.data_source>` for the fixed account crediting table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class FixedCreditingRate(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the fixed account crediting table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the fixed account crediting table into cache.

        Relative path to the fixed account crediting table:

        ``resource/annuity/product/base/crediting_rate_fixed.csv``

        :param path: Path to the fixed account crediting table.
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys='account_name',
            inplace=True
        )

    @use_latest_value
    def crediting_rate(
        self,
        account_name: str
    ) -> float:

        """
        Returns the fixed account crediting rate.

        :param account_name: Account name.
        :return: Fixed account crediting rate.
        """

        return self.cache['crediting_rate'][account_name]
