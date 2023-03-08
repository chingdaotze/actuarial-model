from pandas import read_json

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceJson(
    DataSourceFile
):

    """
    Data source object for a JSON file.
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
