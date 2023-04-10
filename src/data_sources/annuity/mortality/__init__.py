from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.mortality.base_mortality import BaseMortality
from src.data_sources.annuity.mortality.mortality_improvement import MortalityImprovement
from src.data_sources.annuity.mortality.mortality_improvement_dates import MortalityImprovementDates


class Mortality(
    DataSourceNamespace
):

    """
    Namespace that contains all mortality-related data sources.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files from disk.

        :param path:
        """

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.base_mortality: BaseMortality = BaseMortality(
            path=join(
                self.path,
                '2012_individual_annuity_mortality_basic_table.csv'
            )
        )

        self.mortality_improvement: MortalityImprovement = MortalityImprovement(
            path=join(
                self.path,
                'mortality_improvement_projection_scale_g2.csv'
            )
        )

        self.mortality_improvement_dates: MortalityImprovementDates = MortalityImprovementDates(
            path=join(
                self.path,
                'mortality_improvement_projection_scale_g2_dates.csv'
            )
        )
