from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection.parameters import ProjectionParameters
from src.system.projection_entity import (
    ProjectionEntity,
    take_snapshot
)
from src.data_sources.economic_scenarios.economic_scenario import EconomicScenario


class IndexValues(
    ProjectionValues
):

    def __init__(
        self
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.index_value: float = 0.0
        self.pct_change: float = 0.0


class Index(
    ProjectionEntity
):

    """
    Projection entity that represents an economic index, like S&P 500, Big Mac, or Inverse Cramer.
    """

    data_source: EconomicScenario
    values: IndexValues

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_source: EconomicScenario,
        index_name: str
    ):

        ProjectionEntity.__init__(
            self=self,
            projection_parameters=projection_parameters,
            data_source=data_source,
            values=IndexValues()
        )

        self.index_name: str = index_name

        self.project(
            t=self.projection_parameters.start_t,
            duration=relativedelta()
        )

    def calc_pct_change(
        self,
        t: date,
        duration: relativedelta
    ) -> float:

        """
        Calculates the percentage growth in the index over time.

        :param t:
        :param duration:
        :return:
        """

        curr_rate = self.data_source.get_rate(
            name=self.index_name,
            t=t
        )

        next_rate = self.data_source.get_rate(
            name=self.index_name,
            t=t + duration
        )

        pct_change = (next_rate / curr_rate) - 1.0

        return pct_change

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        """
        Calculates:

        1. The percent change in the index from one period to the next.
        2. The index value itself.

        :param t:
        :param duration:
        :return:
        """

        self.values.pct_change = self.calc_pct_change(
            t=t,
            duration=duration
        )

        self.values.index_value = self.data_source.get_rate(
            name=self.index_name,
            t=t + duration
        )
