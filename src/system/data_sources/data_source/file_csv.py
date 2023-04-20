"""
`CSV file <https://en.wikipedia.org/wiki/Comma-separated_values>`_-based data source.
"""

from abc import ABC

from pandas import read_csv

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceCsvFile(
    DataSourceFile,
    ABC
):

    """
    Abstract data source for a `CSV file <https://en.wikipedia.org/wiki/Comma-separated_values>`_.
    Inherit this class to implement a custom CSV file data source.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Loads data from a `CSV file <https://en.wikipedia.org/wiki/Comma-separated_values>`_
        into the cache.

        :param path: Path to CSV file.
        """

        DataSourceFile.__init__(
            self=self,
            path=path,
            dataframe_load_function=read_csv
        )
