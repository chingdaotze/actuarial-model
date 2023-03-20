from os.path import join

from src.system.data_sources.namespace import DataSourceNamespace

from src.data_sources.annuity.product.gmwb.benefit import GmwbBenefit
from src.data_sources.annuity.product.gmwb.charge import GmwbCharge


class GmwbRider(
    DataSourceNamespace
):

    """
    Namespace that contains all GMWB-related data sources and namespaces.
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

        self.gmwb_benefit: GmwbBenefit = GmwbBenefit(
            path=join(
                self.path,
                'benefit.json'
            )
        )

        self.gmwb_charge: GmwbCharge = GmwbCharge(
            path=join(
                self.path,
                'charge.csv'
            )
        )
