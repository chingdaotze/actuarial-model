from abc import ABC
from typing import Type

from src.system.data_sources.collection import DataSourceCollection
from src.system.data_sources.data_source.file_json import DataSourceJsonFile

from src.data_sources.annuity.model_points.model_point import ModelPoint


class ModelPointsBase(
    DataSourceJsonFile,
    DataSourceCollection,
    ABC
):

    """
    Data source collection that holds model points.
    """

    def __init__(
        self,
        path: str,
        model_point_type: Type[ModelPoint]
    ):

        """
        Constructor that reads data from a JSON file, and generates model points of an arbitrary type.

        :param path:
        :param model_point_type:
        """

        DataSourceJsonFile.__init__(
            self=self,
            path=path
        )

        DataSourceCollection.__init__(
            self=self
        )

        for data in [row[1] for row in self.cache.iterrows()]:

            self[data['id']] = model_point_type(
                data=data
            )
