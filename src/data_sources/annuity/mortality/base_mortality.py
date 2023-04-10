from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.enums import Gender
from src.system.projection_entity.projection_value import use_latest_value


class BaseMortality(
    DataSourceCsvFile
):

    """
    Base mortality table.
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

    @use_latest_value
    def base_mortality_rate(
        self,
        gender: Gender,
        attained_age: int
    ) -> float:

        """
        Convenience method to access data from the base mortality table. Returns a base mortality rate.

        :param gender:
        :param attained_age:
        :return:
        """

        return self.cache[gender][attained_age]
