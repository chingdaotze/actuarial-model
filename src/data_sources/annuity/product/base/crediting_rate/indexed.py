from pandas import isna

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


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

    @use_latest_value
    def index(
        self,
        account_name: str
    ) -> str:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate index.

        :param account_name:
        :return:
        """

        return self.cache['index'][account_name]

    @use_latest_value
    def term(
        self,
        account_name: str
    ) -> int:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate term.

        :param account_name:
        :return:
        """

        return self.cache['term'][account_name]

    @use_latest_value
    def cap(
        self,
        account_name: str
    ) -> float | None:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate cap.

        :param account_name:
        :return:
        """

        value = self.cache['cap'][account_name]

        if isna(value):

            return None

        else:

            return value

    @use_latest_value
    def spread(
        self,
        account_name: str
    ) -> float | None:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate spread.

        :param account_name:
        :return:
        """

        value = self.cache['spread'][account_name]

        if isna(value):

            return None

        else:

            return value

    @use_latest_value
    def participation_rate(
        self,
        account_name: str
    ) -> float | None:

        """
        Convenience method to access data from the crediting table. Returns a participation rate.

        :param account_name:
        :return:
        """

        value = self.cache['participation_rate'][account_name]

        if isna(value):

            return None

        else:

            return value

    @use_latest_value
    def floor(
        self,
        account_name: str
    ) -> float | None:

        """
        Convenience method to access data from the crediting table. Returns a crediting rate floor.

        :param account_name:
        :return:
        """

        value = self.cache['floor'][account_name]

        if isna(value):

            return None

        else:

            return value
