from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class FixedCreditingRate(
    DataSourceCsvFile
):

    """
    Fixed crediting table.
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
            keys='account_name',
            inplace=True
        )

    def crediting_rate(
        self,
        account_name: str
    ) -> float:

        """
        Convenience method to access data from the crediting table. Returns a fixed crediting rate.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['crediting_rate']
