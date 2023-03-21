from typing import Dict
from datetime import (
    date,
    datetime
)

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import (
    DEFAULT_COL,
    DATE_FORMAT
)


class Premium(
    DataSourcePythonDict
):

    def __init__(
        self,
        data: Dict
    ):

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

    @property
    def premium_date(
        self
    ) -> date:

        return datetime.strptime(
            self.cache[DEFAULT_COL]['date'],
            DATE_FORMAT
        ).date()

    @property
    def premium_amount(
        self
    ) -> float:

        return self.cache[DEFAULT_COL]['amount']
