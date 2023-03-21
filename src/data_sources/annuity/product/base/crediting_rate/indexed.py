from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class IndexedCreditingRate(
    DataSourceCsvFile
):

    """
    Indexed crediting table.
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

    def term(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate term.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['term']

    def cap(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate cap.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['cap']

    def spread(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate spread.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['spread']

    def participation_rate(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a participation rate.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['participation_rate']

    def floor(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate floor.

        :param account_name:
        :return:
        """

        return self.cache[account_name]['floor']
