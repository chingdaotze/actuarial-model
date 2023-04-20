"""
:mod:`Data source <src.system.data_sources.data_source>` for a generic person.
"""

from typing import Dict
from datetime import date

from src.system.data_sources.data_source.python_dict import DataSourcePythonDict
from src.system.constants import DEFAULT_COL
from src.system.enums import Gender
from src.system.date import str_to_date


class Person(
    DataSourcePythonDict
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a generic person.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes a person based on data within a model point file.

        :param data: Model point data.
        """

        DataSourcePythonDict.__init__(
            self=self,
            data=data
        )

    @property
    def id(
        self
    ) -> str:

        """
        Unique identifier for this particular individual. This could be a Social Security Number or DNA sequence.
        For security purposes, this value should probably be salted and hashed.

        :return: Person ID.
        """

        return self.cache[DEFAULT_COL]['id']

    @property
    def gender(
        self
    ) -> Gender:

        """
        Gender for this particular individual.

        :return: Gender.
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

        :return: Date of birth.
        """

        return str_to_date(
            target_str=self.cache[DEFAULT_COL]['dob']
        )
