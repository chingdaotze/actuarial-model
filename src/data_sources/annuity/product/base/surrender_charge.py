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

        lookup_value = min(
            policy_year,
            self.cache.index.max()
        )

        return self.cache[product_name][lookup_value]

    def cdsc_period(
        self,
        product_name: str
    ) -> int:

        """
        Convenience method to access data from the surrender charge table. Returns the maximum surrender charge period.

        :param product_name:
        :return:
        """

        surrender_charge_table = self.cache[product_name]

        return max(
            surrender_charge_table[surrender_charge_table != 0.0].index
        )
