"""
:class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
that holds all annuity model points.
"""

from src.data_sources.model_points import ModelPointsBase
from src.data_sources.annuity.model_points.model_point import ModelPoint


class ModelPoints(
    ModelPointsBase
):

    """
    :class:`Data source collection <src.system.data_sources.collection.DataSourceCollection>`
    that holds all annuity model points.
    """

    def __init__(
        self,
        path: str
    ):

        """
        Constructor method. Reads data from a JSON file and instantiates annuity model points, organized by
        :attr:`model point ID <src.data_sources.model_points.model_point.ModelPointBase.id>`.

        Relative path to the model point file:

        ``resource/annuity/model_points.json``

        :param path: Path to an annuity model point file.
        """

        ModelPointsBase.__init__(
            self=self,
            path=path,
            model_point_type=ModelPoint
        )
