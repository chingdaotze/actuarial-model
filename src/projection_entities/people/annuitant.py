from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    projection_entity_init,
    take_snapshot
)

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.annuitants.annuitant import Annuitant as AnnuitantDataSource
from src.system.enums import Gender


class AnnuitantValues(
    ProjectionValues
):

    def __init__(
        self
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.age: relativedelta = relativedelta()


class Annuitant(
    ProjectionEntity
):

    """
    Projection entity that represents an annuitant.
    """

    data_sources: AnnuityDataSources
    values: AnnuitantValues

    @projection_entity_init
    def __init__(
        self,
        init_t: date,
        data_sources: AnnuityDataSources,
        annuitant_data_source: AnnuitantDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            init_t=init_t,
            data_sources=data_sources,
            values=AnnuitantValues()
        )

        self.id: str = annuitant_data_source.id

        self.gender: Gender = annuitant_data_source.gender
        self.date_of_birth: date = annuitant_data_source.date_of_birth

        self.issue_age: relativedelta = relativedelta(
            dt1=annuitant_data_source.date_of_birth,
            dt2=data_sources.model_point.issue_date
        )

    def __str__(
        self
    ) -> str:

        return f'annuitant_{self.id}'

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        next_t = t + duration

        self.values.age = relativedelta(
            dt1=self.date_of_birth,
            dt2=next_t
        )
