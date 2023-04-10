from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmdb.charge import GmdbCharge
from src.data_sources.annuity.product.gmdb.types import GmdbTypes


class GmdbRider(
    DataSourceNamespace
):

    """
    Namespace that contains all base GMDB-related data sources and namespaces.
    """

    gmdb_charge: GmdbCharge
    gmdb_types: GmdbTypes

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

        self.gmdb_charge = GmdbCharge(
            path=join(
                self.path,
                'charge.csv'
            )
        )

        self.gmdb_types = GmdbTypes(
            path=join(
                self.path,
                'types.csv'
            )
        )
