from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.constants import DEFAULT_COL


class GmwbCharge(
    DataSourceCsvFile
):

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
        product_name: str
    ) -> float:

        return self.cache[product_name]['charge_rate']
