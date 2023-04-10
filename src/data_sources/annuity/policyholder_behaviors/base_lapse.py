from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class BaseLapse(
    DataSourceCsvFile
):

    """
    Base lapse table.
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

    @use_latest_value
    def base_lapse_rate(
        self,
        policy_year: int
    ) -> float:

        """
        Convenience method to access data from the base lapse table. Returns a base lapse rate.

        :param policy_year:
        :return:
        """

        return self.cache['lapse_rate'][policy_year]
