"""
`JSON file <https://en.wikipedia.org/wiki/JSON>`_-based data source.
"""

from abc import ABC

from pandas import read_json

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceJsonFile(
    DataSourceFile,
    ABC
):

    """
    Abstract data source for a `JSON file <https://en.wikipedia.org/wiki/JSON>`_. Inherit this class to implement a custom JSON file data source.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from `JSON file <https://en.wikipedia.org/wiki/JSON>`_ into the cache.

        :param path: Path to JSON file.
        """

        DataSourceFile.__init__(
            self=self,
            path=path,
            dataframe_load_function=read_json
        )
