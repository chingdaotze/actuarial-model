from abc import ABC
from os.path import exists
from typing import Callable

from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase
from src.system.logger import logger


class DataSourceFile(
    DataSourceBase,
    ABC
):

    """
    Abstract data source object for a file on disk. Loads file from disk into cache.
    """

    def __init__(
        self,
        path: str,
        dataframe_load_function: Callable[[str], DataFrame]
    ):

        DataSourceBase.__init__(
            self=self
        )

        self.path: str = path

        if exists(path=self.path):

            self.cache = dataframe_load_function(
                self.path
            )

        else:

            logger.raise_expr(
                expr=FileNotFoundError(
                    f'Could not locate data source file for {self.__qualname__} at: {self.path} !'
                )
            )
