"""
:mod:`Data source <src.system.data_sources.data_source>` for the GMDB charge rate.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.constants import DEFAULT_COL
from src.system.projection_entity.projection_value import use_latest_value


class GmdbCharge(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the GMDB charge rate.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the GMDB charge table into cache.

        Relative path to the GMDB charge table:

        ``resource/annuity/product/gmdb/charge.csv``

        :param path: Path to the GMDB charge table.
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
        rider_name: str
    ) -> float:

        """
        Returns a GMDB charge rate.

        :param rider_name: Rider name.
        :return: GMDB charge rate.
        """

        return self.cache[rider_name]['charge_rate']
