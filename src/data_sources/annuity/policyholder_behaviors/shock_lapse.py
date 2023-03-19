from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class ShockLapse(
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
            keys='years_after_surrender_charge',
            inplace=True
        )

    def shock_lapse_multiplier(
        self,
        years_after_surrender_charge: int
    ) -> float:

        return self.cache['multiplier'][years_after_surrender_charge]
