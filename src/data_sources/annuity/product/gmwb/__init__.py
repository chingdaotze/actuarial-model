"""
:class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity GMWB rider assumptions.
"""

from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmwb.benefit import GmwbBenefit
from src.data_sources.annuity.product.gmwb.charge import GmwbCharge


class GmwbRider(
    DataSourceNamespace
):

    """
    :class:`Namespace <src.system.data_sources.namespace.DataSourceNamespace>` for annuity GMWB rider assumptions.
    """

    gmwb_benefit: GmwbBenefit   # GMWB benefit assumptions.
    gmwb_charge: GmwbCharge     # GMWB charge assumptions.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Constructs additional data sources using files found in the GMWB rider
        assumption folder.

        Relative path to the GMWB rider assumption folder:

        ``resource/annuity/product/gmwb``

        :param path: Path to the GMWB rider assumption folder.
        """

        DataSourceNamespace.__init__(
            self=self,
            path=path
        )

        self.gmwb_benefit = GmwbBenefit(
            path=join(
                self.path,
                'benefit.json'
            )
        )

        self.gmwb_charge = GmwbCharge(
            path=join(
                self.path,
                'charge.csv'
            )
        )
