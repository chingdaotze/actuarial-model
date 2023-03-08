from abc import (
    ABC,
    abstractmethod
)
from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.data_sources import DataSources
from src.system.projection_entity.projection_values import ProjectionValues


class ProjectionEntity(
    ABC
):

    """
    Abstract class that represents an entity within a projection. This abstract class must have:

    1. A values attribute, which contains all the current and historical values for the entity,
    2. An inputs attribute, which contains external data sources,
    3. A roll-forward method, which is a special method called whenever the projection moves forward in time.
    """

    def __init__(
        self
    ):

        self.data_sources: DataSources
        self.values: ProjectionValues

    @abstractmethod
    def roll_forward(
        self,
        duration: relativedelta
    ) -> None:

        ...
