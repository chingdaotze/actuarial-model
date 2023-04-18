"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that holds model points.
"""

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
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
    that holds model points.
    """

    def __init__(
        self,
        path: str,
        model_point_type: Type[ModelPoint]
    ):

        """
        Constructor method. Reads data from a JSON file and instantiates model points of a specified type, organized
        by :attr:`model point ID <src.data_sources.model_points.model_point.ModelPointBase.id>`.

        :param path: Path to a model point file.
        :param model_point_type: Class definition of model point data source to instantiate.
        """

        DataSourceJsonFile.__init__(
            self=self,
            path=path
        )

        DataSourceCollection.__init__(
            self=self
        )

        for data in [row[1] for row in self.cache.iterrows()]:

            instance = model_point_type(
                data=data
            )

            self[instance.id] = instance
