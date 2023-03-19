from abc import ABC


class DataSourceNamespace(
    ABC
):

    """
    Abstract container class that holds a pre-defined collection of data sources. Data sources can be added by
    inheriting and declaring additional class attributes.

    Inherit this class to implement a custom data source collection.
    """

    def __str__(
        self
    ) -> str:

        return str(
            self.__qualname__
        )
