"""
GMDB Ratchet rider.
"""

from typing import TYPE_CHECKING

from src.projection_entities.products.annuity.riders.gmdb.base import GmdbBase

from src.system.projection.time_steps import TimeSteps
from src.system.projection_entity.projection_value import compare_latest_value

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmdb import Gmdb as GmdbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.base_contract import BaseContract


class GmdbMav(
    GmdbBase
):

    """
    GMDB Ratchet rider.
    """

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
        base_contract: 'BaseContract'
    ) -> None:

        r"""
        On every policy anniversary, sets the benefit base to:

        .. math::
            benefit\, base_{t} = max(benefit\, base_{t-1}, account\, value_{t})

        :param base_contract: Base contract.
        :return: Nothing.
        """

        if base_contract.anniversaries:

            self.benefit_base[self.time_steps.t] = max(
                self.benefit_base,
                base_contract.account_value,
                key=compare_latest_value
            )

        else:

            self.benefit_base[self.time_steps.t] = self.benefit_base
