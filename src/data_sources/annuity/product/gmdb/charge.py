from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.constants import DEFAULT_COL


class GmdbCharge(
    DataSourceCsvFile
):

    """
    GMDB charge table.
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
            keys=DEFAULT_COL,
            inplace=True
        )

    def charge_rate(
        self,
        rider_name: str
    ) -> float:

        """
        Convenience method to access data from the GMDB charge table. Returns a GMDB charge rate.

        :param rider_name:
        :return:
        """

        return self.cache[rider_name]['charge_rate']
