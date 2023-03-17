from abc import ABC

from pandas import read_json

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceJsonFile(
    DataSourceFile,
    ABC
):

    """
    Abstract data source for a JSON file. Inherit this class to implement a custom JSON file.
    """

    def __init__(
        self,
        path: str
    ):

        DataSourceFile.__init__(
            self=self,
            path=path,
            dataframe_load_function=read_json
        )
