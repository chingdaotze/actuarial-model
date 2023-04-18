"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity interest crediting.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.crediting_rate.fixed import FixedCreditingRate
from src.data_sources.annuity.product.base.crediting_rate.indexed import IndexedCreditingRate


class CreditingRate(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity interest crediting.
    """

    fixed: FixedCreditingRate       #: Fixed account crediting assumptions.
    indexed: IndexedCreditingRate   #: Fixed indexed account crediting assumptions.

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

        self.fixed = FixedCreditingRate(
            path=join(
                self.path,
                'crediting_rate_fixed.csv'
            )
        )

        self.indexed = IndexedCreditingRate(
            path=join(
                self.path,
                'crediting_rate_indexed.csv'
            )
        )
