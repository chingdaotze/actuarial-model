"""
:mod:`Data source <src.system.data_sources.data_source>` for the shock lapse table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.projection_entity.projection_value import use_latest_value


class ShockLapse(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the shock lapse table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the shock lapse table into cache.

        Relative path to the shock lapse table:

        ``resource/annuity/policyholder_behaviors/shock_lapse_multiplier.csv``

        :param path: Path to the shock lapse table.
        """

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
        Returns a shock lapse multiplier as a percentage of base lapse.

        :param years_after_cdsc_period: Years elapsed after the CDSC period.
        :return: Shock lapse multiplier.
        """

        lookup_value = min(
            years_after_cdsc_period,
            self.cache.index.max()
        )

        return self.cache['multiplier'][lookup_value]
