from abc import ABC
from typing import (
    Dict,
    Any
)


class DataSourceCollection(
    ABC
):

    """
    Abstract container class that holds a dynamic collection of data sources. This class provides a dictionary-like
    storage interface, as well as an iterator across collection elements. This class may be used to represent
    data sources that contain other data sources, such as a model point file which contains multiple model points.

    Inherit this class to implement a custom data source collection.
    """

    def __init__(
        self
    ):

        self.__collection: Dict = {}

    def __setitem__(
        self,
        key,
        value
    ) -> None:

        self.__collection[key] = value

    def __getitem__(
        self,
        item
    ) -> Any:

        return self.__collection[item]

    def __iter__(
        self
    ):

        return iter(
            list(
                self.__collection.values()
            )
        )

    def __repr__(
        self
    ) -> str:

        return repr(self.__collection)

    def __str__(
        self
    ) -> str:

        return str(self.__collection)
