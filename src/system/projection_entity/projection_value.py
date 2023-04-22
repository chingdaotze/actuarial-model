"""
Modeling framework :ref:`object model <object_model>` :ref:`Projection Value <projection_values>`.
"""

from typing import (
    Any,
    Self,
    Callable
)
from datetime import date
from functools import wraps

from pandas import DataFrame

from src.system.constants import DEFAULT_COL


class ProjectionValue:

    """
    Stores values for a :class:`~src.system.projection_entity.ProjectionEntity`.

    It can best be understood as a standard Python `data type <https://docs.python.org/3/library/stdtypes.html>`_
    combined with a *value history*.

    For example, imagine an `integer <https://docs.python.org/3/library/functions.html#int>`_ that keeps track
    of its past values:

    - Like an integer, projection values support all standard
      `numeric operators <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>`_
      (e.g., +, -, /, \\*, etc...).

      The value used in these operations is the
      :attr:`latest value <src.system.projection_entity.projection_value.ProjectionValue.latest_value>`
      from the value history.

    - However, unlike an integer, a value history can be read or written via the
      `[] operator <https://docs.python.org/3/reference/datamodel.html#object.__getitem__>`_ (like a
      `dictionary <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_).

    Here is a code example:

    .. code-block:: python

        my_projection_value = ProjectionValue(
            init_t=date(
                year=2023,
                month=3,
                day=16
            ),
            init_value=50.0
        )  # Create a new ProjectionValue with a starting history of 50.0 on 3/16/2023.

        new_value = my_projection_value + 25.0  # ProjectionValue's support math operands. The value of
                                                # new_value is 75.0, since my_project_value's latest value is 50.0.

        my_projection_value[
            date(
                year=2023,
                month=4,
                day=16
            )
        ] = new_value           # ProjectionValue's logs a new entry in its history (75.0 on 4/16/2023). Since
                                # 4/16/2023 is the latest date in the history, 75.0 also becomes the latest value.
    """

    _history: DataFrame
    _print_values: bool

    def __init__(
        self,
        init_t: date,
        init_value: Any,
        print_values: bool = True
    ):

        """
        Constructor method.

        :param init_t: Initial time step to index ``init_value`` in the value history.
        :param init_value: Initial value to record in the value history.
        :param print_values: Boolean flag to determine whether this projection value is printed.
        """

        self._history = DataFrame(
            columns=['t', DEFAULT_COL]
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

        return self._history[DEFAULT_COL][item]

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

        """
        Latest value from the value history. For example, if the value history contains:

        +-------------+--------------+
        | t           | value        |
        +-------------+--------------+
        | 3/16/2023   | 0.04         |
        +-------------+--------------+
        | 4/16/2023   | 0.06         |
        +-------------+--------------+
        | 5/16/2023   | 0.08         |
        +-------------+--------------+

        This property will return 0.08, as 5/16/2023 is the "latest" date.

        :return: Latest value from history.
        """

        return self._history[DEFAULT_COL][self._history.index.max()]

    @latest_value.setter
    def latest_value(
        self,
        value: Any
    ) -> None:

        self._history[DEFAULT_COL][self._history.index.max()] = value

    @property
    def history(
        self
    ) -> DataFrame:

        """
        Complete value history for this projection value.

        :return: Value history of this projection value.
        """

        return self._history

    @property
    def print_values(
        self
    ) -> bool:

        """
        Boolean flag used to indicate whether this object should be printed.

        :return: Printing flag.
        """

        return self._print_values


def compare_latest_value(
    element: Any
) -> Any:

    """
    Used as the ``key`` argument for built-in comparison functions like
    `max() <https://docs.python.org/3/library/functions.html#max>`_ or
    `min() <https://docs.python.org/3/library/functions.html#min>`_, comparing the
    :attr:`~src.system.projection_entity.projection_value.ProjectionValue.latest_value` attribute between
    :class:`~src.system.projection_entity.projection_value.ProjectionValue` objects.

    :param element: Element to parse.
    :return: Value to compare.
    """

    if issubclass(type(element), ProjectionValue):

        return element.latest_value

    else:

        return element


def use_latest_value(
    function: Callable
) -> Callable:

    """
    Decorator that scans function arguments for
    :class:`~src.system.projection_entity.projection_value.ProjectionValue`'s, then replaces them with the
    :class:`~src.system.projection_entity.projection_value.ProjectionValue`'s
    :attr:`~src.system.projection_entity.projection_value.ProjectionValue.latest_value` property.

    :param function: Function to wrap.
    :return: A wrapped function.
    """

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ) -> Any:

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
