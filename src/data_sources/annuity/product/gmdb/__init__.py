from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmdb.charge import GmdbCharge


class GmdbRider(
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

        self.charge: GmdbCharge = GmdbCharge(
            path=join(
                self.path,
                'charge.csv'
            )
        )
