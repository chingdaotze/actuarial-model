from typing import Union

from pandas import Series

from src.system.constants import DEFAULT_COL

from src.data_sources.model_points.model_point import ModelPointBase
from src.data_sources.annuity.model_points.model_point.annuitants import Annuitants
from src.data_sources.annuity.model_points.model_point.gmwb import Gmwb
from src.data_sources.annuity.model_points.model_point.accounts import Accounts


class ModelPoint(
    ModelPointBase
):

    """
    Data source that represents an annuity model point.
    """

    def __init__(
        self,
        data: Series
    ):

        ModelPointBase.__init__(
            self=self,
            data=data
        )

        self.annuitants: Annuitants = Annuitants(
            data=self.cache[DEFAULT_COL]['annuitants']
        )

        self.gmwb: Union[Gmwb, None]

        if self.cache[DEFAULT_COL]['gmwb'] is not None:

            self.gmwb = Gmwb(
                data=self.cache[DEFAULT_COL]['gmwb']
            )

        else:

            self.gmwb = None

        self.accounts: Accounts = Accounts(
            data=self.cache[DEFAULT_COL]['accounts']
        )

    @property
    def gmdb(
        self
    ) -> Union[str, None]:

        """
        Guaranteed Minimum Death Benefit (GMDB) human-readable rider name. Returns None if the model point does not
        have a GMDB rider.

        :return:
        """

        return self.cache[DEFAULT_COL]['gmdb']
