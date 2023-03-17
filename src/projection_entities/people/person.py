from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection_entity.projection_values import ProjectionValues
from src.data_sources.annuity.base import AnnuityBaseDataSources
from src.system.enums import Gender


class PersonValues(
    ProjectionValues
):

    def __init__(
        self,
        data_sources
    ):

        ProjectionValues.__init__(
            self=self,
            data_sources=data_sources
        )

        self.age: relativedelta = relativedelta(
            years=0,
            months=0,
            days=0
        )  # TODO: Initialize from data source

        self.gender: Gender =


class Person(
    ProjectionEntity
):

    """
    Projection entity that represents a person.
    """

    def __init__(
        self,
        data_sources
    ):

        ProjectionEntity.__init__(
            self=self,
            data_sources=data_sources,
            values_type=PersonValues
        )

    def roll_forward(
        self,
        duration: relativedelta
    ) -> None:

        self.values.age += duration
