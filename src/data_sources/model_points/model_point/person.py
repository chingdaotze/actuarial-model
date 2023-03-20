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

    """
    Data source that represents a person.
    """

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

        """
        Unique identifier for a particular individual. This could be a Social Security Number or DNA sequence.
        For security purposes, this value should probably be salted and hashed.

        :return:
        """

        return self.cache[DEFAULT_COL]['id']

    @property
    def gender(
        self
    ) -> Gender:

        """
        Gender for this particular individual.

        :return:
        """

        return Gender(
            self.cache[DEFAULT_COL]['gender']
        )

    @property
    def date_of_birth(
        self
    ) -> date:

        """
        Date of birth for this particular individual.

        :return:
        """

        return datetime.strptime(
            self.cache[DEFAULT_COL]['dob'],
            DATE_FORMAT
        ).date()
