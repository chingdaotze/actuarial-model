from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class Annuitization(
    DataSourceCsvFile
):

    """
    Annuitization rate table.
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
            keys='attained_age',
            inplace=True
        )

    @use_latest_value
    def annuitization_rate(
        self,
        attained_age: int
    ) -> float:

        """
        Convenience method to access data from the annuitization table. Returns an annuitization rate.

        :param attained_age:
        :return:
        """

        return self.cache['annuitization_rate'][attained_age]
