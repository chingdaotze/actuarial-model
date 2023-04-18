"""
One or more annuitants.
"""

from typing import List

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue
from src.system.date import calc_whole_years
from src.system.actuarial_math import convert_decrement_rate

from src.data_sources.annuity import AnnuityDataSources
from src.projection_entities.people.annuitants.annuitant import Annuitant


class Annuitants(
    ProjectionEntity
):

    """
    One or more annuitants.
    """

    data_sources: AnnuityDataSources

    annuitants: List[Annuitant]             #: List of annuitants

    t_q_x: ProjectionValue                  #: Probability of death for the primary annuitant.
    t_q_y: ProjectionValue                  #: Probability of death for the secondary annuitant.
    base_lapse_rate: ProjectionValue        #: Base lapse rate.
    lapse_multiplier: ProjectionValue       #: Base lapse rate multiplier.
    lapse_rate: ProjectionValue             #: Final lapse rate.
    annuitization_rate: ProjectionValue     #: Annuitization rate.
    l_xy: ProjectionValue                   #: Policy count - both alive.
    l_x: ProjectionValue                    #: Policy count - only primary annuitant alive.
    l_y: ProjectionValue                    #: Policy count - only secondary annuitant alive.
    d_xy: ProjectionValue                   #: Policy count - both dead.
    d_lapse: ProjectionValue                #: Policy count - lapses.
    d_annuitization: ProjectionValue        #: Policy count - annuitizations.

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources
    ):

        """
        Constructor method. Initializes a list of annuitants from the
        :class:`annuitants data source <src.data_sources.annuity.model_points.ModelPoints>`.

        :param time_steps: Projection-wide timekeeping object.
        :param data_sources: Annuity data sources.
        """

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        # Get list of annuitants
        self.annuitants = []

        for annuitant_data_source in self.data_sources.model_point.annuitants:

            self.annuitants.append(
                Annuitant(
                    time_steps=self.time_steps,
                    data_sources=self.data_sources,
                    annuitant_data_source=annuitant_data_source
                )
            )

        # Frasierization components
        self.t_q_x = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.t_q_y = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.base_lapse_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.lapse_multiplier = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.lapse_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.annuitization_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.l_xy = ProjectionValue(
            init_t=self.init_t,
            init_value=1.0 if self.secondary_annuitant else 0.0
        )

        self.l_x = ProjectionValue(
            init_t=self.init_t,
            init_value=1.0 if not self.secondary_annuitant else 0.0
        )

        self.l_y = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.d_xy = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.d_lapse = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.d_annuitization = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return 'annuitants'

    @property
    def primary_annuitant(
        self
    ) -> Annuitant:

        """
        Returns the primary annuitant. Primary annuitant is the youngest annuitant.

        :return: Primary annuitant.
        """

        return min(
            self.annuitants,
            key=lambda annuitant_: annuitant_.date_of_birth
        )

    @property
    def secondary_annuitant(
        self
    ) -> Annuitant | None:

        """
        Returns the secondary annuitant. Secondary annuitant is the oldest annuitant. Returns ``None`` if
        there is no secondary annuitant.

        :return: Secondary annuitant.
        """

        if len(self.annuitants) > 1:

            return max(
                self.annuitants,
                key=lambda annuitant_: annuitant_.date_of_birth
            )

        else:

            return None

    def _update_mortality_rates(
        self
    ) -> None:

        # Get mortality rates
        self.primary_annuitant.update_mortality()

        self.t_q_x[self.time_steps.t] = convert_decrement_rate(
            q_x=self.primary_annuitant.mortality_rate,
            interval=self.time_steps.time_step
        )

        if self.secondary_annuitant:

            self.secondary_annuitant.update_mortality()

            self.t_q_y[self.time_steps.t] = convert_decrement_rate(
                q_x=self.secondary_annuitant.mortality_rate,
                interval=self.time_steps.time_step
            )

        else:

            self.t_q_y[self.time_steps.t] = 0.0

    def _update_lapse_rates(
        self
    ) -> None:

        # Get base lapse rate
        policy_year = calc_whole_years(
            dt1=self.time_steps.t,
            dt2=self.data_sources.model_point.issue_date
        )

        self.base_lapse_rate[self.time_steps.t] = self.data_sources.policyholder_behaviors.base_lapse.base_lapse_rate(
            policy_year=policy_year
        )

        # Get shock lapse multiplier
        cdsc_period = self.data_sources.product.base_product.surrender_charge.cdsc_period(
            product_name=self.data_sources.model_point.product_name
        )

        years_after_cdsc_period = max(
            policy_year - cdsc_period,
            0
        )

        self.lapse_multiplier[self.time_steps.t] = \
            self.data_sources.policyholder_behaviors.shock_lapse.shock_lapse_multiplier(
                years_after_cdsc_period=years_after_cdsc_period
            )

        # Calculate lapse rate
        self.lapse_rate[self.time_steps.t] = convert_decrement_rate(
            q_x=self.base_lapse_rate * self.lapse_multiplier,
            interval=self.time_steps.time_step
        )

    def _update_annuitization_rates(
        self
    ) -> None:

        # Get annuitization rate
        self.annuitization_rate[self.time_steps.t] = convert_decrement_rate(
            q_x=self.data_sources.policyholder_behaviors.annuitization.annuitization_rate(
                attained_age=self.primary_annuitant.attained_age
            ),
            interval=self.time_steps.time_step
        )

    def update_decrements(
        self
    ) -> None:

        """
        Projects annuitants forward by one time step. Applies decrements in order of:

        #. Mortality
        #. Lapse
        #. Annuitization

        :return: Nothing.
        """

        if self.time_steps.prev_t != self.time_steps.t:

            # Update decrement rates
            self._update_mortality_rates()
            self._update_lapse_rates()
            self._update_annuitization_rates()

            # Update lives
            self.l_xy[self.time_steps.t] = (
                self.l_xy[self.time_steps.prev_t] *
                (1.0 - self.t_q_x) *
                (1.0 - self.t_q_y) *
                (1.0 - self.lapse_rate) *
                (1.0 - self.annuitization_rate)
            )

            self.l_x[self.time_steps.t] = (
                self.l_x[self.time_steps.prev_t] * (1.0 - self.t_q_x) +
                (
                    self.l_xy[self.time_steps.prev_t] *
                    self.t_q_y *
                    (1.0 - self.t_q_x)
                )
            ) * (
                    (1.0 - self.lapse_rate) *
                    (1.0 - self.annuitization_rate)
                )

            self.l_y[self.time_steps.t] = (
                self.l_y[self.time_steps.prev_t] * (1.0 - self.t_q_y) +
                (
                    self.l_xy[self.time_steps.prev_t] *
                    self.t_q_x *
                    (1.0 - self.t_q_y)
                )
            ) * (
                    (1.0 - self.lapse_rate) *
                    (1.0 - self.annuitization_rate)
                )

            self.d_xy[self.time_steps.t] = (
                self.d_xy[self.time_steps.prev_t] +
                (
                    self.l_xy[self.time_steps.prev_t] * self.t_q_x * self.t_q_y +
                    self.l_x[self.time_steps.prev_t] * self.t_q_x +
                    self.l_y[self.time_steps.prev_t] * self.t_q_y
                ) * (
                    (1.0 - self.lapse_rate) *
                    (1.0 - self.annuitization_rate)
                )
            )

            self.d_lapse[self.time_steps.t] = (
                self.d_lapse[self.time_steps.prev_t] +
                (
                    self.l_xy[self.time_steps.prev_t] +
                    self.l_x[self.time_steps.prev_t] +
                    self.l_y[self.time_steps.prev_t]
                ) * self.lapse_rate * (
                    (1.0 - self.annuitization_rate)
                )
            )

            self.d_annuitization[self.time_steps.t] = (
                self.d_annuitization[self.time_steps.prev_t] +
                (
                    self.l_xy[self.time_steps.prev_t] +
                    self.l_x[self.time_steps.prev_t] +
                    self.l_y[self.time_steps.prev_t]
                ) * self.annuitization_rate
            )
