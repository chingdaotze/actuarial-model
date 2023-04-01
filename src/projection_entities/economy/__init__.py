from typing import List

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.economy.index import Index


class Economy(
    ProjectionEntity
):

    data_sources: AnnuityDataSources

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.indexes: List[Index] = [
            Index(
                time_steps=self.time_steps,
                data_sources=self.data_sources,
                index_name=index_name
            ) for index_name in self.data_sources.economic_scenarios.rates
        ]

    def __str__(
        self
    ) -> str:

        return 'economy'

    def age_economy(
        self
    ):

        for economic_index in self.indexes:

            economic_index.age_index()
