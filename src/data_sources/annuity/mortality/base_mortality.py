"""
:mod:`Data source <src.system.data_sources.data_source>` for the annuity base mortality table.
"""

from src.system.data_sources.data_source.file_csv import DataSourceCsvFile
from src.system.enums import Gender
from src.system.projection_entity.projection_value import use_latest_value


class BaseMortality(
    DataSourceCsvFile
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for the annuity base mortality table.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from the base mortality table into cache.

        Source(s):

        - `<https://mort.soa.org/ViewTable.aspx?&TableIdentity=2581>`_
        - `<https://mort.soa.org/ViewTable.aspx?&TableIdentity=2582>`_

        Relative path to the base mortality table:

        ``resource/annuity/mortality/2012_individual_annuity_mortality_basic_table.csv``

        :param path: Path to the base mortality table.
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
    def base_mortality_rate(
        self,
        gender: Gender,
        attained_age: int
    ) -> float:

        """
        Returns a base mortality rate.

        :param gender: Lookup gender.
        :param attained_age: Lookup attained age. Age should be Age Nearest Birthday (ANB).
        :return: Base mortality rate.
        """

        return self.cache[gender][attained_age]
