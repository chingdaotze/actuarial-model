"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity base product assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.surrender_charge import SurrenderCharge
from src.data_sources.annuity.product.base.crediting_rate import CreditingRate


class BaseProduct(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity base product assumptions.
    """

    surrender_charge: SurrenderCharge   #: Surrender charge assumptions.
    crediting_rate: CreditingRate       #: Crediting rate assumptions.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the base product
        assumption folder.

        Relative path to the base product assumption folder:

        ``resource/annuity/product/base``

        :param path: Path to the base product assumption folder.
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
