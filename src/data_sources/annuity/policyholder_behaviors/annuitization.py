from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class Annuitization(
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
            keys='attained_age',
            inplace=True
        )

    def annuitization_rate(
        self,
        attained_age: int
    ) -> float:

        return self.cache['annuitization_rate'][attained_age]
