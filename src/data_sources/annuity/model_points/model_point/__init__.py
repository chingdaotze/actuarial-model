from typing import Union

from pandas import Series

from src.system.constants import DEFAULT_COL

from src.data_sources.model_points.model_point import ModelPointBase
from src.data_sources.annuity.model_points.model_point.annuitants import Annuitants


class ModelPoint(
    ModelPointBase
):

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

    @property
    def gmdb(
        self
    ) -> Union[str, None]:
        return self.cache[DEFAULT_COL]['gmdb']

    @property
    def gmwb(
        self
    ) -> Union[str, None]:

        return self.cache[DEFAULT_COL]['gmwb']
