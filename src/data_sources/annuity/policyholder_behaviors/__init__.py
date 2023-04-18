"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity policyholder behavior
assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.policyholder_behaviors.base_lapse import BaseLapse
from src.data_sources.annuity.policyholder_behaviors.shock_lapse import ShockLapse
from src.data_sources.annuity.policyholder_behaviors.annuitization import Annuitization


class PolicyholderBehaviors(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity policyholder behavior
    assumptions.
    """

    base_lapse: BaseLapse           #: Base lapse assumptions.
    shock_lapse: ShockLapse         #: Shock lapse assumptions.
    annuitization: Annuitization    #: Annuitization assumptions.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the policyholder behavior
        assumption folder.

        Relative path to the policyholder behavior assumption folder:

        ``resource/annuity/policyholder_behaviors``

        :param path: Path to the policyholder behavior assumption folder.
        """

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.base_lapse = BaseLapse(
            path=join(
                self.path,
                'base_lapse_rate.csv'
            )
        )

        self.shock_lapse = ShockLapse(
            path=join(
                self.path,
                'shock_lapse_multiplier.csv'
            )
        )

        self.annuitization = Annuitization(
            path=join(
                self.path,
                'annuitization_rate.csv'
            )
        )
