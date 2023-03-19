from os.path import (
    isdir,
    join
)

from src.system.logger import logger
from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.mortality.base_mortality import BaseMortality
from src.data_sources.annuity.mortality.mortality_improvement import MortalityImprovement


class Mortality(
    DataSourceNamespace
):

    def __init__(
        self,
        path: str
    ):
        self.path: str = path

        if not isdir(self.path):

            logger.raise_expr(
                expr=NotADirectoryError(
                    f'Could not locate a valid directory at this location: {self.path} to compile annuity data sources!'
                )
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
