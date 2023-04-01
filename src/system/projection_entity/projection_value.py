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

        self._history: DataFrame = DataFrame(
            columns=['t', self.VALUE_COL]
        )

        self._history.set_index(
            keys='t',
            inplace=True
        )

        self[init_t] = init_value

    @property
    def latest_value(
        self
    ) -> Any:

        return self._history[self.VALUE_COL][self._history.index.max()]

    @property
    def history(
        self
    ) -> DataFrame:

        return self._history

    def __setitem__(
        self,
        key: date,
        value: Any
    ) -> None:

        self._history.loc[key] = value

    def __getitem__(
        self,
        item: date
    ) -> Any:

        return self._history[self.VALUE_COL][item]
