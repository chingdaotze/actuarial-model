from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmdb.charge import GmdbCharge


class GmdbRider(
    DataSourceNamespace
):

    """
    Namespace that contains all base GMDB-related data sources and namespaces.
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

        self.charge: GmdbCharge = GmdbCharge(
            path=join(
                self.path,
                'charge.csv'
            )
        )
