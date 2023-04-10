from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


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

    @use_latest_value
    def shock_lapse_multiplier(
        self,
        years_after_cdsc_period: int
    ) -> float:

        """
        Convenience method to access data from the shock lapse table. Returns a shock lapse multiplier.

        :param years_after_cdsc_period:
        :return:
        """

        lookup_value = min(
            years_after_cdsc_period,
            self.cache.index.max()
        )

        return self.cache['multiplier'][lookup_value]
