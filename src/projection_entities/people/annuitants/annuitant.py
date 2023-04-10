from datetime import date

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.date import (
    calc_partial_years,
    calc_whole_years
)

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

    id: str
    gender: Gender
    date_of_birth: date

    attained_age: ProjectionValue
    base_mortality_rate: ProjectionValue
    mortality_improvement_rate: ProjectionValue
    mortality_improvement_factor: ProjectionValue
    mortality_rate: ProjectionValue

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

        self.id = annuitant_data_source.id
        self.gender = annuitant_data_source.gender
        self.date_of_birth = annuitant_data_source.date_of_birth

        self.attained_age = ProjectionValue(
            init_t=self.init_t,
            init_value=calc_whole_years(
                dt1=self.init_t,
                dt2=self.date_of_birth
            )
        )

        self.base_mortality_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.mortality_improvement_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.mortality_improvement_factor = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.mortality_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return f'annuitant.{self.id}'

    def update_mortality(
        self
    ) -> None:

        # Set attained age
        self.attained_age[self.time_steps.t] = calc_whole_years(
            dt1=self.time_steps.t,
            dt2=self.date_of_birth
        )

        # Get base mortality
        self.base_mortality_rate[self.time_steps.t] = self.data_sources.mortality.base_mortality.base_mortality_rate(
            gender=self.gender,
            attained_age=self.attained_age
        )

        # Get mortality improvement rate
        self.mortality_improvement_rate[self.time_steps.t] = \
            self.data_sources.mortality.mortality_improvement.mortality_improvement_rate(
                gender=self.gender,
                attained_age=self.attained_age
            )

        # Calculate mortality improvement factor
        mortality_improvement_start_date = \
            self.data_sources.mortality.mortality_improvement_dates.mortality_improvement_start_date

        mortality_improvement_end_date = \
            self.data_sources.mortality.mortality_improvement_dates.mortality_improvement_end_date

        mortality_improvement_duration = calc_partial_years(
            dt1=mortality_improvement_end_date,
            dt2=mortality_improvement_start_date
        )

        self.mortality_improvement_factor[self.time_steps.t] = \
            (1.0 - self.mortality_improvement_rate) ** mortality_improvement_duration

        # Calculate mortality rate
        self.mortality_rate[self.time_steps.t] = \
            self.base_mortality_rate * self.mortality_improvement_factor
