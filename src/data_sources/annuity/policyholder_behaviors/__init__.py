from os.path import (
    isdir,
    join
)

from src.system.logger import logger
from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.policyholder_behaviors.base_lapse import BaseLapse
from src.data_sources.annuity.policyholder_behaviors.shock_lapse import ShockLapse
from src.data_sources.annuity.policyholder_behaviors.annuitization import Annuitization


class PolicyholderBehaviors(
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

        self.base_lapse: BaseLapse = BaseLapse(
            path=join(
                self.path,
                'base_lapse_rate.csv'
            )
        )

        self.shock_lapse: ShockLapse = ShockLapse(
            path=join(
                self.path,
                'shock_lapse_multiplier.csv'
            )
        )

        self.annuitization: Annuitization = Annuitization(
            path=join(
                self.path,
                'annuitization_rate.csv'
            )
        )
