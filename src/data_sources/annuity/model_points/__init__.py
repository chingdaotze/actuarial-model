from src.data_sources.model_points import ModelPointsBase
from src.data_sources.annuity.model_points.model_point import ModelPoint


class ModelPoints(
    ModelPointsBase
):

    def __init__(
        self,
        path: str
    ):

        ModelPointsBase.__init__(
            self=self,
            path=path,
            model_point_type=ModelPoint
        )
