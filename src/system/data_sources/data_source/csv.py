from pandas import read_csv

from src.system.data_sources.data_source.file import DataSourceFile


class DataSourceCsv(
    DataSourceFile
):

    """
    Data source object for a CSV file.
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
