from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.policyholder_behaviors.base_lapse import BaseLapse
from src.data_sources.annuity.policyholder_behaviors.shock_lapse import ShockLapse
from src.data_sources.annuity.policyholder_behaviors.annuitization import Annuitization


class PolicyholderBehaviors(
    DataSourceNamespace
):

    """
    Namespace that contains all policyholder behavior-related data sources.
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
