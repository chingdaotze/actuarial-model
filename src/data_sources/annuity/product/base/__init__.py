from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.surrender_charge import SurrenderCharge
from src.data_sources.annuity.product.base.crediting_rate import CreditingRate


class BaseProduct(
    DataSourceNamespace
):

    """
    Namespace that contains all base product-related data sources and namespaces.
    """

    surrender_charge: SurrenderCharge
    crediting_rate: CreditingRate

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

        self.surrender_charge = SurrenderCharge(
            path=join(
                self.path,
                'surrender_charge.csv'
            )
        )

        self.crediting_rate = CreditingRate(
            path=self.path
        )
