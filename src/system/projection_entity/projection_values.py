from abc import ABC
from datetime import date

from pandas import (
    DataFrame,
    concat
)


class ProjectionValues(
    ABC
):

    """
    Abstract container class that holds:

    1. The current state (as class attributes).
    2. Historic snapshots of class attributes (within a DataFrame). Snapshots are indexed by date and
       an integer index.

    Inherit this class to implement a custom set of projection values by adding additional attributes.
    For example, a policy entity might store its account value as an attribute within this container.
    """

    def __init__(
        self
    ):

        """
        Constructor method. Constructs the internal snapshots data structure.
        """

        self._snapshots: DataFrame = DataFrame(
            columns=['index', 't', 'label']
        )

        self._snapshots.set_index(
            keys='index',
            inplace=True
        )

    @property
    def snapshots(
        self
    ) -> DataFrame:

        """
        Read-only property to access snapshots.

        :return:
        """

        return self._snapshots

    def take_snapshot(
        self,
        t: date,
        label: str = ''
    ) -> None:

        """
        Stores a copy of all public attributes and records values within an internal data structure.

        :return:
        """

        row = {
            'index': [self._snapshots.shape[0]],
            't': [t],
            'label': [label]
        }

        for name, value in self.__dict__.items():

            if not name.startswith('_'):

                row[name] = [value]

        row = DataFrame.from_dict(
            data=row
        )

        row.set_index(
            keys='index',
            inplace=True
        )

        self._snapshots = concat(
            objs=[
                self._snapshots,
                row
            ]
        )

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
