from typing import TYPE_CHECKING

from src.projection_entities.products.annuity.riders.gmdb.base import GmdbBase

from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmdb import Gmdb as GmdbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.contracts.base import Contract


class GmdbMav(
    GmdbBase
):

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        gmdb_data_source: GmdbDataSource
    ):

        GmdbBase.__init__(
            self=self,
            time_steps=time_steps,
            data_sources=data_sources,
            gmdb_data_source=gmdb_data_source
        )

    def update_benefit_base(
        self,
        base_contract: 'Contract'
    ) -> None:

        if base_contract.anniversaries.latest_value:

            self.benefit_base[self.time_steps.t] = max(
                self.benefit_base.latest_value,
                base_contract.account_value.latest_value
            )

        else:

            self.benefit_base[self.time_steps.t] = self.benefit_base.latest_value
