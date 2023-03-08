from abc import ABC
from datetime import date

from pandas import DataFrame


class ProjectionValues(
    ABC
):

    """
    Abstract object that contains all current and historic values for a particular entity.
    """

    def __init__(
        self
    ):

        self.__snapshots: DataFrame = DataFrame()

    @property
    def snapshots(
        self
    ) -> DataFrame:

        """
        Read-only property to return internal _snapshots container.

        :return:
        """

        return self.__snapshots

    def take_snapshot(
        self,
        t: date
    ) -> None:

        """

        :param t:
        :return:
        """

        # TODO: Implement snapshot storage

    def save_snapshots(
        self,
        path: str
    ) -> None:

        """

        :param path:
        :return:
        """

        self.snapshots.to_csv(
            path_or_buf=path,
            index=True
        )
