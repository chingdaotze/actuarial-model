from datetime import date
from dateutil.relativedelta import relativedelta
from typing import (
    List,
    Self
)


class TimeSteps:

    def __init__(
        self,
        start_t: date,
        end_t: date,
        time_step: relativedelta
    ):
        self._index: int = 0
        self._time_step: relativedelta = time_step
        self._time_steps: List[date] = []

        time_step = start_t

        while time_step <= end_t:

            self._time_steps.append(
                time_step
            )

            time_step += self._time_step

    def __iter__(
        self
    ) -> Self:

        self._index = -1
        return self

    def __next__(
        self
    ) -> date:

        if self._index < len(self._time_steps) - 1:

            self._index += 1
            t = self.t

            return t

        else:

            raise StopIteration

    @property
    def min_t(
        self
    ) -> date:

        return min(
            self._time_steps
        )

    @property
    def max_t(
        self
    ) -> date:

        return max(
            self._time_steps
        )

    @property
    def prev_t(
        self
    ) -> date:

        return self._time_steps[
            max(
                self._index - 1,
                0
            )
        ]

    @property
    def t(
        self
    ) -> date:

        return self._time_steps[
            self._index
        ]

    @property
    def next_t(
        self
    ) -> date:

        return self._time_steps[
            min(
                self._index,
                len(self._time_steps) - 1
            )
        ]
