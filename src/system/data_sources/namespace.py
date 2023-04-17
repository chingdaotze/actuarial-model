"""
Container that holds a pre-defined collection of :mod:`data sources <src.system.data_sources.data_source>`.
"""

from abc import ABC
from os.path import isdir

from src.system.logger import Logger


class DataSourceNamespace(
    ABC
):

    """
    Abstract container class that holds a pre-defined collection of
    :mod:`data sources <src.system.data_sources.data_source>`. Data sources can be added by inheriting and declaring
    additional class attributes.

    Inherit this class to implement a custom data source collection.
    """

    path: str  #: Path to the namespace.

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Checks whether the namespace exists.

        :param path: File path to a namespace.
        """

        self.path = path

        if not isdir(self.path):

            Logger().raise_expr(
                expr=NotADirectoryError(
                    f'Could not locate a valid directory at this location: {self.path} !'
                )
            )

    def __str__(
        self
    ) -> str:

        return str(
            self.__qualname__
        )
