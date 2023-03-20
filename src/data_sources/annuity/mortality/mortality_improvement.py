from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.enums import Gender


class MortalityImprovement(
    DataSourceCsvFile
):

    """
    Mortality improvement table.
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
            keys='age_nearest_birthday',
            inplace=True
        )

    def mortality_improvement_rate(
        self,
        gender: Gender,
        attained_age: int
    ) -> float:

        """
        Convenience method to access data from the mortality improvement table. Returns a mortality improvement rate.

        :param gender:
        :param attained_age:
        :return:
        """

        return self.cache[gender][attained_age]
