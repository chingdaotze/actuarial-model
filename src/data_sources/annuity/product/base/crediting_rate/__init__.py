from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.crediting_rate.fixed import FixedCreditingRate
from src.data_sources.annuity.product.base.crediting_rate.indexed import IndexedCreditingRate
from src.data_sources.annuity.product.base.crediting_rate.separate_account import SeparateAccountCreditingRate


class CreditingRate(
    DataSourceNamespace
):

    """
    Namespace that contains all crediting-related data sources and namespaces.
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

        self.fixed: FixedCreditingRate = FixedCreditingRate(
            path=join(
                self.path,
                'crediting_rate_fixed.csv'
            )
        )

        self.indexed: IndexedCreditingRate = IndexedCreditingRate(
            path=join(
                self.path,
                'crediting_rate_indexed.csv'
            )
        )

        self.separate_account: SeparateAccountCreditingRate = SeparateAccountCreditingRate(
            path=join(
                self.path,
                'crediting_rate_separate_account.csv'
            )
        )
