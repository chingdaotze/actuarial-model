"""
:mod:`Data source <src.system.data_sources.data_source>` for a single annuity model point.
"""

from pandas import Series

from src.system.constants import DEFAULT_COL

from src.data_sources.model_points.model_point import ModelPointBase
from src.data_sources.annuity.model_points.model_point.annuitants import Annuitants
from src.data_sources.annuity.model_points.model_point.riders import Riders
from src.data_sources.annuity.model_points.model_point.accounts import Accounts


class ModelPoint(
    ModelPointBase
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a single annuity model point. Contains
    nested data sources for dynamic parts of a model point.
    """

    annuitants: Annuitants      #: Annuitants associated with this model point.
    riders: Riders              #: Riders associated with this model point.
    accounts: Accounts          #: Accounts associated with this model point.

    def __init__(
        self,
        data: Series
    ):

        """
        Constructor method. Initializes a model point based on data within an annuity model point file.

        :param data: Model point data.
        """

        ModelPointBase.__init__(
            self=self,
            data=data
        )

        self.annuitants = Annuitants(
            data=self.cache[DEFAULT_COL]['annuitants']
        )

        self.riders = Riders(
            data=self.cache[DEFAULT_COL]['riders']
        )

        self.accounts = Accounts(
            data=self.cache[DEFAULT_COL]['accounts']
        )
