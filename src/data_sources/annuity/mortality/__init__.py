"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity mortality assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.mortality.base_mortality import BaseMortality
from src.data_sources.annuity.mortality.mortality_improvement import MortalityImprovement
from src.data_sources.annuity.mortality.mortality_improvement_dates import MortalityImprovementDates


class Mortality(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity mortality assumptions.
    """

    base_mortality: BaseMortality                               #: Base mortality assumptions.
    mortality_improvement: MortalityImprovement                 #: Mortality improvement assumptions.
    mortality_improvement_dates: MortalityImprovementDates      #: Mortality improvement date assumptions.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the mortality assumption folder.

        Relative path to the mortality assumption folder:

        ``resource/annuity/mortality``

        :param path: Path to the mortality assumption folder.
        """

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.base_mortality = BaseMortality(
            path=join(
                self.path,
                '2012_individual_annuity_mortality_basic_table.csv'
            )
        )

        self.mortality_improvement = MortalityImprovement(
            path=join(
                self.path,
                'mortality_improvement_projection_scale_g2.csv'
            )
        )

        self.mortality_improvement_dates = MortalityImprovementDates(
            path=join(
                self.path,
                'mortality_improvement_projection_scale_g2_dates.csv'
            )
        )
