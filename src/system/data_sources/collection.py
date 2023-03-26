from abc import ABC
from typing import (
    TypeVar,
    Dict,
    List
)


K = TypeVar(
    name='K'
)

V = TypeVar(
    name='V'
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

        """
        Constructor method. Initializes internal data structure.
        """

        self.__collection: Dict[K, V] = {}

    def __setitem__(
        self,
        key: K,
        value: V
    ) -> None:

        self.__collection[key] = value

    def __getitem__(
        self,
        item: K
    ) -> V:

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

    @property
    def keys(
        self
    ) -> List[K]:

        return list(
            self.__collection.keys()
        )

    @property
    def items(
        self
    ) -> List[K]:

        return list(
            self.__collection.items()
        )
