"""
:mod:`Data source <src.system.data_sources.data_source>` for the GMDB type translation.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.constants import DEFAULT_COL
from src.system.projection_entity.projection_value import use_latest_value


class GmdbTypes(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the GMDB type translation.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the GMDB types table into cache.

        Relative path to the GMDB types table:

        ``resource/annuity/product/gmdb/types.csv``

        :param path: Path to the GMDB types table.
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
    def gmdb_type(
        self,
        rider_name: str
    ) -> float:

        """
        Returns a GMDB types translation. Given a GMDB name, returns the type of GMDB rider.

        :param rider_name: Rider name.
        :return: GMDB type.
        """

        return self.cache[rider_name]['type']
