from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class SurrenderCharge(
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
            keys='policy_year',
            inplace=True
        )

    def surrender_charge_rate(
        self,
        policy_year: int,
        product_name: str
    ) -> float:

        return self.cache[product_name][policy_year]
