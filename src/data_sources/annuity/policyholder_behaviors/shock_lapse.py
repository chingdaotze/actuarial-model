from src.system.data_sources.data_source.file_csv import DataSourceCsvFile


class ShockLapse(
    DataSourceCsvFile
):

    """
    Shock lapse table.
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
            keys='years_after_surrender_charge',
            inplace=True
        )

    def shock_lapse_multiplier(
        self,
        years_after_surrender_charge: int
    ) -> float:

        """
        Convenience method to access data from the shock lapse table. Returns a shock lapse multiplier.

        :param years_after_surrender_charge:
        :return:
        """

        return self.cache['multiplier'][years_after_surrender_charge]
