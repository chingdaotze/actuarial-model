"""
:mod:`Data source <src.system.data_sources.data_source>` for the surrender charge table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class SurrenderCharge(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the surrender charge table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the surrender charge (CDSC) table into cache.

        Relative path to the annuitization table:

        ``resource/annuity/product/base/surrender_charge.csv``

        :param path: Path to the surrender charge table.
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
    def surrender_charge_rate(
        self,
        policy_year: int,
        product_name: str
    ) -> float:

        """
        Returns a surrender charge rate.

        :param policy_year: Policy year.
        :param product_name: Product name.
        :return: Surrender charge rate.
        """

        lookup_value = min(
            policy_year,
            self.cache.index.max()
        )

        return self.cache[product_name][lookup_value]

    @use_latest_value
    def cdsc_period(
        self,
        product_name: str
    ) -> int:

        """
        Returns a maximum surrender charge period for a given product.

        :param product_name: Product name.
        :return: Maximum surrender charge period.
        """

        surrender_charge_table = self.cache[product_name]

        return max(
            surrender_charge_table[surrender_charge_table != 0.0].index
        )
