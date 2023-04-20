"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity GMDB rider assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmdb.charge import GmdbCharge
from src.data_sources.annuity.product.gmdb.types import GmdbTypes


class GmdbRider(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity GMDB rider assumptions.
    """

    gmdb_charge: GmdbCharge     #: GMDB charge assumptions.
    gmdb_types: GmdbTypes       #: GMDB type translation.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the GMDB rider
        assumption folder.

        Relative path to the GMDB rider assumption folder:

        ``resource/annuity/product/gmdb``

        :param path: Path to the GMDB rider assumption folder.
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
