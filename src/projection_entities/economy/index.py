from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.economic_scenarios.economic_scenario import EconomicScenario


class Index(
    ProjectionEntity
):

    """
    Projection entity that represents an economic index, like S&P 500, Big Mac, or Inverse Cramer.
    """

    data_sources: AnnuityDataSources

    economic_scenario: EconomicScenario
    index_name: str

    index_value: ProjectionValue
    pct_change: ProjectionValue

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        index_name: str
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.economic_scenario = data_sources.economic_scenario
        self.index_name = index_name

        self.index_value = ProjectionValue(
            init_t=self.init_t,
            init_value=self.economic_scenario.get_rate(
                name=self.index_name,
                t=self.init_t
            )
        )

        self.pct_change = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return f'economy.index.{self.index_name}'

    def calc_pct_change(
        self,
        t1: date,
        t2: date
    ) -> float:

        """
        Calculates the percentage growth in the index between two points in time.

        :param t1:
        :param t2:
        :return:
        """

        curr_rate = self.economic_scenario.get_rate(
            name=self.index_name,
            t=t1
        )

        next_rate = self.economic_scenario.get_rate(
            name=self.index_name,
            t=t2
        )

        pct_change = (next_rate / curr_rate) - 1.0

        return pct_change

    def age_index(
        self
    ) -> None:

        """
        Calculates:

        1. The percent change in the index from one period to the next.
        2. The index value itself.

        :return:
        """

        self.pct_change[self.time_steps.t] = self.calc_pct_change(
            t1=self.time_steps.prev_t,
            t2=self.time_steps.t
        )

        self.index_value[self.time_steps.t] = self.economic_scenario.get_rate(
            name=self.index_name,
            t=self.time_steps.t
        )
