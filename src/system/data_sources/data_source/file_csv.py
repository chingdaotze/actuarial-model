from abc import ABC

from pandas import read_csv

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceCsvFile(
    DataSourceFile,
    ABC
):

    """
    Abstract data source for a CSV file. Inherit this class to implement a custom CSV file.
    """

    def __init__(
        self,
        path: str
    ):

        DataSourceFile.__init__(
            self=self,
            path=path,
            dataframe_load_function=read_csv
        )
