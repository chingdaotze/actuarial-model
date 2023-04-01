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
    Data source that represents an annuity model point.
    """

    annuitants: Annuitants
    riders: Riders
    accounts: Accounts

    def __init__(
        self,
        data: Series
    ):

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
