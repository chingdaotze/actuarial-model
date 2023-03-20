from abc import ABC
from os.path import isdir

from src.system.logger import logger


class DataSourceNamespace(
    ABC
):

    """
    Abstract container class that holds a pre-defined collection of data sources. Data sources can be added by
    inheriting and declaring additional class attributes.

    Inherit this class to implement a custom data source collection.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Checks whether the namespace exists.

        :param path:
        """

        self.path: str = path

        if not isdir(self.path):

            logger.raise_expr(
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
