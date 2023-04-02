from typing import Any
from datetime import date

from pandas import DataFrame


class ProjectionValue:

    VALUE_COL: str = 'value'
    _history: DataFrame
    _print_values: bool

    def __init__(
        self,
        init_t: date,
        init_value: Any,
        print_values: bool = True
    ):

        self._history = DataFrame(
            columns=['t', self.VALUE_COL]
        )

        self._history.set_index(
            keys='t',
            inplace=True
        )

        self._print_values = print_values

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

    @property
    def print_values(
        self
    ) -> bool:

        return self._print_values

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
