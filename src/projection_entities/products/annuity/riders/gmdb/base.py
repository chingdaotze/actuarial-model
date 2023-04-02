from typing import TYPE_CHECKING
from abc import (
    ABC,
    abstractmethod
)

from src.system.projection_entity import ProjectionEntity
from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import ProjectionValue

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmdb import Gmdb as GmdbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.base_contract import BaseContract


class GmdbBase(
    ProjectionEntity,
    ABC
):

    data_sources: AnnuityDataSources
    rider_name: str
    benefit_base: ProjectionValue

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        gmdb_data_source: GmdbDataSource
    ):

        ProjectionEntity.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources
        )

        self.rider_name = gmdb_data_source.rider_name

        self.benefit_base = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.charge_rate = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.charge_amount = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

        self.net_amount_at_risk = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

    def __str__(
        self
    ) -> str:

        return 'contract.riders.gmdb'

    def process_premiums(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        self.benefit_base[self.time_steps.t] = \
            self.benefit_base.latest_value + base_contract.premium_new[self.time_steps.t]

    def process_charge(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        for _ in base_contract.monthiversaries.latest_value:

            self.charge_rate[self.time_steps.t] = self.data_sources.product.gmdb_rider.charge.charge_rate(
                rider_name=self.rider_name
            )

            self.charge_amount[self.time_steps.t] = \
                base_contract.account_value.latest_value * (self.charge_rate.latest_value / 12.0)

            base_contract.assess_charge(
                charge_amount=self.charge_amount.latest_value,
                charge_account_name='gmdb_charge'
            )

    @abstractmethod
    def update_benefit_base(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        ...

    def update_net_amount_at_risk(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        self.net_amount_at_risk[self.time_steps.t] = max(
            self.benefit_base.latest_value - base_contract.account_value.latest_value,
            0.0
        )

    def process_death_benefit(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        pass
