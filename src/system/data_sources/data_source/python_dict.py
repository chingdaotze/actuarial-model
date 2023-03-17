from typing import Dict

from pandas import DataFrame

from src.system.data_sources.data_source.base import DataSourceBase
from src.system.constants import DEFAULT_COL


class DataSourcePythonDict(
    DataSourceBase
):

    """
    Abstract data source for a Python dictionary. Inherit this class to implement a custom Python dictionary.
    """

    def __init__(
        self,
        data: Dict
    ):

        DataSourceBase.__init__(
            self=self
        )

        self.cache = DataFrame.from_dict(
            data=data,
            orient='index',
            columns=[DEFAULT_COL]
        )
