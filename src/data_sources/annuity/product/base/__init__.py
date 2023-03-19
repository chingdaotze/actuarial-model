from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base.surrender_charge import SurrenderCharge


class BaseProduct(
    DataSourceNamespace
):

    def __init__(
        self,
        path: str
    ):

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.surrender_charge: SurrenderCharge = SurrenderCharge(
            path=join(
                self.path,
                'surrender_charge.csv'
            )
        )
