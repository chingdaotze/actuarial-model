from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class SurrenderCharge(
    DataSourceCsvFile
):

    """
    Surrender charge table.
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
            keys='policy_year',
            inplace=True
        )

    def surrender_charge_rate(
        self,
        policy_year: int,
        product_name: str
    ) -> float:

        """
        Convenience method to access data from the surrender charge table. Returns a surrender charge rate.

        :param policy_year:
        :param product_name:
        :return:
        """

        return self.cache[product_name][policy_year]
