"""
:mod:`Data source <src.system.data_sources.data_source>` for the GMWB charge rate.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.constants import DEFAULT_COL
from src.system.projection_entity.projection_value import use_latest_value


class GmwbCharge(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the GMWB charge rate.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the GMWB charge table into cache.

        Relative path to the GMWB charge table:

        ``resource/annuity/product/gmwb/charge.csv``

        :param path: Path to the GMWB charge table.
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys=DEFAULT_COL,
            inplace=True
        )

    @use_latest_value
    def charge_rate(
        self,
        product_name: str
    ) -> float:

        """
        Returns a GMWB charge rate.

        :param product_name: Product name.
        :return: GMWB charge rate.
        """

        return self.cache[product_name]['charge_rate']
