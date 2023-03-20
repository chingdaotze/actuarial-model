from pandas import DataFrame

from src.system.data_sources.data_source.file_json import DataSourceJsonFile


class GmwbBenefit(
    DataSourceJsonFile
):

    """
    GMWB benefit table.
    """

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

        """
        Convenience method to access data from the GMWB charge table. Returns a GMWB withdrawal rate for policies
        that still have a positive account value.

        :param rider_name:
        :param age_first_withdrawal:
        :return:
        """

        withdrawal_rate_table = self.cache[rider_name]['av_active']

    def av_exhaust_withdrawal_rate(
        self,
        rider_name: str,
        age_first_withdrawal: int
    ) -> float:

        """
        Convenience method to access data from the GMWB charge table. Returns a GMWB withdrawal rate for policies
        that no longer have an account value.

        :param rider_name:
        :param age_first_withdrawal:
        :return:
        """

        withdrawal_rate_table = self.cache[rider_name]['av_exhaust']
