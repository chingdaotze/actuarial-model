from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_values import ProjectionValues
from src.system.projection_entity import (
    ProjectionEntity,
    take_snapshot
)
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.annuity.model_points.model_point import ModelPoint
from src.data_sources.annuity.model_points.model_point.annuitants.annuitant import Annuitant as AnnuitantDataSource
from src.system.enums import Gender


class AnnuitantValues(
    ProjectionValues
):

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_source: AnnuitantDataSource
    ):

        ProjectionValues.__init__(
            self=self
        )

        self.age: relativedelta = relativedelta(
            dt1=data_source.date_of_birth,
            dt2=projection_parameters.start_t
        )


class Annuitant(
    ProjectionEntity
):

    """
    Projection entity that represents a person.
    """

    data_source: ModelPoint
    values: AnnuitantValues

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_source: ModelPoint,
        annuitant_id: str
    ):

        annuitant_data_source: AnnuitantDataSource = self.data_source.annuitants[
            annuitant_id
        ]

        ProjectionEntity.__init__(
            self=self,
            projection_parameters=projection_parameters,
            data_source=data_source,
            values=AnnuitantValues(
                projection_parameters=projection_parameters,
                data_source=annuitant_data_source
            )
        )

        self.gender: Gender = annuitant_data_source.gender

        self.issue_age: relativedelta = relativedelta(
            dt1=annuitant_data_source.date_of_birth,
            dt2=self.data_source.issue_date
        )

    @take_snapshot
    def project(
        self,
        t: date,
        duration: relativedelta
    ) -> None:

        self.values.age += duration
