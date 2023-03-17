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
from src.system.enums import Gender


class Person(
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
    def id(
        self
    ) -> str:

        return self.cache[DEFAULT_COL]['id']

    @property
    def gender(
        self
    ) -> Gender:

        return Gender(
            self.cache[DEFAULT_COL]['gender']
        )

    @property
    def date_of_birth(
        self
    ) -> date:

        return datetime.strptime(
            self.cache[DEFAULT_COL]['dob'],
            DATE_FORMAT
        ).date()
