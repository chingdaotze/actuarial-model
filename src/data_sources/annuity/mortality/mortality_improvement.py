"""
:mod:`Data source <src.system.data_sources.data_source>` for the annuity mortality improvement table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.enums import Gender
from src.system.projection_entity.projection_value import use_latest_value


class MortalityImprovement(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the annuity mortality improvement table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the mortality improvement table into cache.

        Source(s):

        - `<https://mort.soa.org/ViewTable.aspx?&TableIdentity=2583>`_
        - `<https://mort.soa.org/ViewTable.aspx?&TableIdentity=2584>`_

        Relative path to the base mortality table:

        ``resource/annuity/mortality/mortality_improvement_projection_scale_g2.csv``

        :param path: Path to the mortality improvement table.
        """

        DataSourceCsvFile.__init__(
            self=self,
            path=path
        )

        self.cache.set_index(
            keys='age_nearest_birthday',
            inplace=True
        )

    @use_latest_value
    def mortality_improvement_rate(
        self,
        gender: Gender,
        attained_age: int
    ) -> float:

        """
        Returns a mortality improvement rate.

        :param gender: Lookup gender.
        :param attained_age: Lookup attained age. Age should be Age Nearest Birthday (ANB).
        :return: Mortality improvement rate.
        """

        return self.cache[gender][attained_age]
