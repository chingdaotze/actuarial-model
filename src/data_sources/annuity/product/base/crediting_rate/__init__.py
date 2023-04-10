from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.crediting_rate.fixed import FixedCreditingRate
from src.data_sources.annuity.product.base.crediting_rate.indexed import IndexedCreditingRate


class CreditingRate(
    DataSourceNamespace
):

    """
    Namespace that contains all crediting-related data sources and namespaces.
    """

    fixed: FixedCreditingRate
    indexed: IndexedCreditingRate

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
