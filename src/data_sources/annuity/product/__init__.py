"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity product assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.base import BaseProduct
from src.data_sources.annuity.product.gmdb import GmdbRider
from src.data_sources.annuity.product.gmwb import GmwbRider


class Product(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity product assumptions.
    """

    base_product: BaseProduct   #: Base product assumptions.
    gmdb_rider: GmdbRider       #: Guaranteed Minimum Death Benefit rider assumptions.
    gmwb_rider: GmwbRider       #: Guaranteed Minimum Withdrawal Benefit rider assumptions.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the product
        assumption folder.

        Relative path to the product assumption folder:

        ``resource/annuity/product``

        :param path: Path to the product assumption folder.
        """

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.base_product = BaseProduct(
            path=join(
                self.path,
                'base'
            )
        )

        self.gmdb_rider = GmdbRider(
            path=join(
                self.path,
                'gmdb'
            )
        )

        self.gmwb_rider = GmwbRider(
            path=join(
                self.path,
                'gmwb'
            )
        )
