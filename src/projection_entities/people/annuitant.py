from datetime import date

from dateutil.relativedelta import relativedelta

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.annuitants.annuitant import Annuitant as AnnuitantDataSource
from src.system.enums import Gender


class Annuitant(
    ProjectionEntity
):

    """
    Projection entity that represents an annuitant.
    """

    data_sources: AnnuityDataSources

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        annuitant_data_source: AnnuitantDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.id: str = annuitant_data_source.id
        self.gender: Gender = annuitant_data_source.gender
        self.date_of_birth: date = annuitant_data_source.date_of_birth

        self.issue_age: relativedelta = relativedelta(
            dt1=annuitant_data_source.date_of_birth,
            dt2=data_sources.model_point.issue_date
        )

        self.attained_age = ProjectionValue(
            init_t=self.init_t,
            init_value=relativedelta(
                dt1=self.date_of_birth,
                dt2=self.init_t
            )
        )

    def __str__(
        self
    ) -> str:

        return f'annuitant_{self.id}'

    def update_attained_age(
        self
    ) -> None:

        self.attained_age[self.time_steps.t] = relativedelta(
            dt1=self.date_of_birth,
            dt2=self.time_steps.t
        )
