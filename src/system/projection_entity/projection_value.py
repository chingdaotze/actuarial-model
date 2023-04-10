from typing import (
    Any,
    Self,
    Callable
)
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

    @staticmethod
    def _parse_other(
        other: Any
    ) -> Any:

        if issubclass(type(other), ProjectionValue):

            return other.latest_value

        else:

            return other

    # https://docs.python.org/3/reference/datamodel.html#basic-customization
    def __repr__(
        self
    ) -> str:

        return str(
            self.latest_value
        )

    def __str__(
        self
    ) -> str:

        return str(
            self.latest_value
        )

    def __lt__(
        self,
        other
    ) -> bool:

        return self.latest_value < self._parse_other(
            other=other
        )

    def __le__(
        self,
        other
    ) -> bool:

        return self.latest_value <= self._parse_other(
            other=other
        )

    def __eq__(
        self,
        other
    ) -> bool:

        return self.latest_value == self._parse_other(
            other=other
        )

    def __ne__(
        self,
        other
    ) -> bool:

        return self.latest_value != self._parse_other(
            other=other
        )

    def __gt__(
        self,
        other
    ) -> bool:

        return self.latest_value > self._parse_other(
            other=other
        )

    def __ge__(
        self,
        other
    ) -> bool:

        return self.latest_value >= self._parse_other(
            other=other
        )

    def __bool__(
        self
    ) -> bool:

        return bool(
            self.latest_value
        )

    # https://docs.python.org/3/reference/datamodel.html#emulating-container-types
    def __len__(
        self
    ) -> int:

        return len(self.latest_value)

    def __setitem__(
        self,
        key: date,
        value: Any
    ) -> None:

        value = self._parse_other(
            other=value
        )

        self._history.loc[key] = value

    def __getitem__(
        self,
        item: date
    ) -> Any:

        return self._history[self.VALUE_COL][item]

    def __delitem__(
        self,
        key: date
    ) -> None:

        self._history.drop(
            key,
            inplace=True
        )

    def __iter__(
        self
    ) -> iter:

        return iter(
            self.latest_value
        )

    def __reversed__(
        self
    ) -> reversed:

        return reversed(
            self.latest_value
        )

    def __contains__(
        self,
        item: Any
    ) -> bool:

        return item in self.latest_value

    # https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
    def __add__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value + self._parse_other(
            other=other
        )

    def __sub__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value - self._parse_other(
            other=other
        )

    def __mul__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value * self._parse_other(
            other=other
        )

    def __matmul__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value.__matmul__(
            self._parse_other(
                other=other
            )
        )

    def __truediv__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value / self._parse_other(
            other=other
        )

    def __floordiv__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value // self._parse_other(
            other=other
        )

    def __mod__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value % self._parse_other(
            other=other
        )

    def __divmod__(
        self,
        other: Any
    ) -> Any:

        return divmod(
            self.latest_value,
            self._parse_other(
                other=other
            )
        )

    def __pow__(
        self,
        power: Any,
        modulo: Any = None
    ) -> Any:

        return pow(
            self.latest_value,
            self._parse_other(
                other=power
            ),
            modulo
        )

    def __lshift__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value << self._parse_other(
            other=other
        )

    def __rshift__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value >> self._parse_other(
            other=other
        )

    def __and__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value & self._parse_other(
            other=other
        )

    def __xor__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value ^ self._parse_other(
            other=other
        )

    def __or__(
        self,
        other: Any
    ) -> Any:

        return self.latest_value | self._parse_other(
            other=other
        )

    def __radd__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) + self.latest_value

    def __rsub__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) - self.latest_value

    def __rmul__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) * self.latest_value

    def __rmatmul__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ).__matmul__(
            self.latest_value
        )

    def __rtruediv__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) / self.latest_value

    def __rfloordiv__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) // self.latest_value

    def __rmod__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) % self.latest_value

    def __rdivmod__(
        self,
        other: Any
    ) -> Any:

        return divmod(
            self._parse_other(
                other=other
            ),
            self.latest_value
        )

    def __rpow__(
        self,
        power: Any,
        modulo: Any = None
    ) -> Any:

        return pow(
            self._parse_other(
                other=power
            ),
            self.latest_value,
            modulo
        )

    def __rlshift__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) << self.latest_value

    def __rrshift__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) >> self.latest_value

    def __rand__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) & self.latest_value

    def __rxor__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) ^ self.latest_value

    def __ror__(
        self,
        other: Any
    ) -> Any:

        return self._parse_other(
            other=other
        ) | self.latest_value

    def __iadd__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value + self._parse_other(
            other=other
        )

        return self

    def __isub__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value - self._parse_other(
            other=other
        )

        return self

    def __imul__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value - self._parse_other(
            other=other
        )

        return self

    def __imatmul__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value.__matmul__(
            self._parse_other(
                other=other
            )
        )

        return self

    def __itruediv__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value / self._parse_other(
            other=other
        )

        return self

    def __ifloordiv__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value // self._parse_other(
            other=other
        )

        return self

    def __imod__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value % self._parse_other(
            other=other
        )

        return self

    def __ipow__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value ** self._parse_other(
            other=other
        )

        return self

    def __ilshift__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value << self._parse_other(
            other=other
        )

        return self

    def __irshift__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value >> self._parse_other(
            other=other
        )

        return self

    def __iand__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value & self._parse_other(
            other=other
        )

        return self

    def __ixor__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value ^ self._parse_other(
            other=other
        )

        return self

    def __ior__(
        self,
        other: Any
    ) -> Self:

        self.latest_value = self.latest_value | self._parse_other(
            other=other
        )

        return self

    @property
    def latest_value(
        self
    ) -> Any:

        return self._history[self.VALUE_COL][self._history.index.max()]

    @latest_value.setter
    def latest_value(
        self,
        value: Any
    ) -> None:

        self._history[self.VALUE_COL][self._history.index.max()] = value

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


def compare_latest_value(
    element: Any
) -> Any:

    if issubclass(type(element), ProjectionValue):

        return element.latest_value

    else:

        return element


def use_latest_value(
    function: Callable
) -> Callable:

    """
    Decorator that scans function arguments for Projection value types, then replaces them with the latest_value
    attribute.

    :param function:
    :return:
    """

    def wrapper(
        *args,
        **kwargs
    ) -> Any:

        """
        Wrapper function that wraps the decorated function. Contains the core logic for this decorator.

        :param args:
        :param kwargs:
        :return:
        """

        args = [arg.latest_value if issubclass(type(arg), ProjectionValue) else arg for arg in args]

        kwargs = {
            key: item.latest_value if issubclass(type(item), ProjectionValue) else item for key, item in kwargs.items()
        }

        return_value = function(
            *args,
            **kwargs
        )

        return return_value

    return wrapper
