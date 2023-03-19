from pandas import DataFrame

from src.system.data_sources.data_source.file_json import DataSourceJsonFile


class GmwbBenefit(
    DataSourceJsonFile
):

    def __init__(
        self,
        path: str
    ):

        DataSourceJsonFile.__init__(
            self=self,
            path=path
        )

        # Transform tables
        self.cache = self.cache.applymap(
            func=lambda cell_data: DataFrame.from_dict(
                data=cell_data,
                orient='index'
            )
        )

    def av_active_withdrawal_rate(
        self,
        rider_name: str,
        age_first_withdrawal: int
    ) -> float:

        withdrawal_rate_table = self.cache[rider_name]['av_active']

    def av_exhaust_withdrawal_rate(
        self,
        rider_name: str,
        age_first_withdrawal: int
    ) -> float:

        withdrawal_rate_table = self.cache[rider_name]['av_exhaust']
