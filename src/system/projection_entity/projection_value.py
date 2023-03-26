from typing import Any
from datetime import date

from pandas import DataFrame


class ProjectionValue:

    VALUE_COL = 'value'

    def __init__(
        self,
        init_t: date,
        init_value: Any
    ):

        self.__history: DataFrame = DataFrame(
            columns=['t', self.VALUE_COL]
        )

        self.__history.set_index(
            keys='t',
            inplace=True
        )

        self[init_t] = init_value

    @property
    def latest_value(
        self
    ) -> Any:

        return self.__history[self.__history.index.max]

    @property
    def history(
        self
    ) -> DataFrame:

        return self.__history

    def __setitem__(
        self,
        key: date,
        value: Any
    ) -> None:

        self.__history.loc[key] = value

    def __getitem__(
        self,
        item: date
    ) -> Any:

        return self.__history[[item]]
