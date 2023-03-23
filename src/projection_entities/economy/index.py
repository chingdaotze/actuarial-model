from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    take_init_snapshot,
    take_snapshot
)

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.economic_scenarios.economic_scenario import EconomicScenario


class IndexValues(
    ProjectionValues
):

    def __init__(
        self,
        index_value: float
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.index_value: float = index_value
        self.pct_change: float = 0.0


class Index(
    ProjectionEntity
):

    """
    Projection entity that represents an economic index, like S&P 500, Big Mac, or Inverse Cramer.
    """

    data_sources: AnnuityDataSources
    values: IndexValues

    @take_init_snapshot
    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        index_name: str
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources,
            values=IndexValues(
                index_value=data_sources.economic_scenario.get_rate(
                    name=index_name,
                    t=init_t
                )
            )
        )

        self.economic_scenario: EconomicScenario = data_sources.economic_scenario
        self.index_name: str = index_name

    def __str__(
        self
    ) -> str:

        return f'index_{self.index_name}'

    def calc_pct_change(
        self,
        t: date,
        duration: relativedelta
    ) -> float:

        """
        Calculates the percentage growth in the index between two points in time.

        :param t:
        :param duration:
        :return:
        """

        curr_rate = self.economic_scenario.get_rate(
            name=self.index_name,
            t=t
        )

        next_rate = self.economic_scenario.get_rate(
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

        self.values.index_value = self.economic_scenario.get_rate(
            name=self.index_name,
            t=t + duration
        )
