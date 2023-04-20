"""
Economy, represented as a collection of indices.
"""

from typing import List

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.economy.index import Index


class Economy(
    ProjectionEntity
):

    """
    Economy, represented as a collection of indices.
    """

    data_sources: AnnuityDataSources

    indexes: List[Index]    #: List of indices.

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources
    ):

        """
        Constructor method. Initializes a list of indices from
        :class:`economic scenarios data source <src.data_sources.economic_scenarios.EconomicScenarios>`.

        :param time_steps: Projection-wide timekeeping object.
        :param data_sources: Annuity data sources.
        """

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.indexes = [
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
    ) -> None:

        """
        Projects the Economy forward one time step by calling each index's
        :meth:`~src.projection_entities.economy.index.Index.age_index` method.

        :return: Nothing.
        """

        for economic_index in self.indexes:

            economic_index.age_index()
