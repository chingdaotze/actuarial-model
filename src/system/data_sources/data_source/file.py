"""
Abstract `file <https://en.wikipedia.org/wiki/Computer_file>`_-based data source.
"""

from abc import ABC
from os.path import exists
from typing import Callable

from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase
from src.system.logger import Logger


class DataSourceFile(
    DataSourceBase,
    ABC
):

    """
    Abstract data source object for a `file <https://en.wikipedia.org/wiki/Computer_file>`_ on disk.
    Loads file from disk into cache. Inherit this class to specify a particular file format.
    """

    def __init__(
        self,
        path: str,
        dataframe_load_function: Callable[[str], DataFrame]
    ):

        """
        Constructor method. Checks if the file exists.

        :param path: Path to a file that contains data source data.
        :param dataframe_load_function: Function used to load data into the cache
        """

        DataSourceBase.__init__(
            self=self
        )

        self.path: str = path

        if exists(path=self.path):

            self.cache = dataframe_load_function(
                self.path
            )

        else:

            Logger().raise_expr(
                expr=FileNotFoundError(
                    f'Could not locate data source file for {self.__qualname__} at: {self.path} !'
                )
            )
