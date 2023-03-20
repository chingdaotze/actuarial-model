from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base import BaseProduct
from src.data_sources.annuity.product.gmdb import GmdbRider
from src.data_sources.annuity.product.gmwb import GmwbRider


class Product(
    DataSourceNamespace
):

    """
    Namespace that contains all product-related data sources and namespaces.
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

        self.base_product: BaseProduct = BaseProduct(
            path=join(
                self.path,
                'base'
            )
        )

        self.gmdb_rider: GmdbRider = GmdbRider(
            path=join(
                self.path,
                'gmdb'
            )
        )

        self.gmwb_rider: GmwbRider = GmwbRider(
            path=join(
                self.path,
                'gmwb'
            )
        )
