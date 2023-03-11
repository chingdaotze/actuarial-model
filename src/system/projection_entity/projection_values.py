from abc import ABC
from datetime import date

from pandas import DataFrame

from src.system.data_sources import DataSources


class ProjectionValues(
    ABC
):

    """
    Abstract container class that holds:

    1. The current state (as class attributes).
    2. Historic snapshots of class attributes (within a DataFrame). Snapshots are indexed by date and
       an integer index.
    3. A reference to external data sources used to set the initial state.

    Inherit this class to implement a custom set of projection values by adding additional attributes.
    For example, a policy entity might store its account value as an attribute within this container.
    """

    def __init__(
        self,
        data_sources: DataSources
    ):

        """
        Constructor method. Initial values can be set by reading from external data sources.

        :param data_sources:
        """

        self.data_sources: DataSources = data_sources
        self.__snapshots: DataFrame = DataFrame(
            index=['t', 'shutter_count']
        )

    @property
    def snapshots(
        self
    ) -> DataFrame:

        """
        Read-only property to access snapshots.

        :return:
        """

        return self.__snapshots

    def take_snapshot(
        self,
        t: date
    ) -> None:

        """
        Stores a copy of all attributes (excluding data_sources) and records values within an internal
        DataFrame.

        :param t:
        :return:
        """

        # TODO: Implement snapshot storage

    def write_snapshots(
        self,
        path: str
    ) -> None:

        """
        Writes snapshots to disk as a CSV file.

        :param path:
        :return:
        """

        self.snapshots.to_csv(
            path_or_buf=path,
            index=True
        )
