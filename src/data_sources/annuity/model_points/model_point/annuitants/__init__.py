"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that contains annuitants for a particular
:class:`model point <src.data_sources.annuity.model_points.model_point.ModelPoint>`.
"""

from typing import (
    List,
    Dict
)

from src.system.data_sources.collection import DataSourceCollection

from src.data_sources.annuity.model_points.model_point.annuitants.annuitant import Annuitant


class Annuitants(
    DataSourceCollection
):

    """
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
    that contains one or more annuitants for a particular
    :class:`model point <src.data_sources.annuity.model_points.model_point.ModelPoint>`.
    """

    def __init__(
        self,
        data: List[Dict]
    ):

        """
        Constructor method. Initializes a collection of annuitants based on data within an annuity model point file,
        organized by
        :attr:`annuitant ID <src.data_sources.annuity.model_points.model_point.annuitants.annuitant.Annuitant.id>`.

        :param data: Data for multiple annuitants.
        """

        DataSourceCollection.__init__(
            self=self
        )

        for row in data:

            instance = Annuitant(
                data=row
            )

            self[instance.id] = instance
