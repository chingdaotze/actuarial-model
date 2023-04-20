"""
GMDB Return of Account Value rider.
"""

from typing import TYPE_CHECKING

from src.projection_entities.products.annuity.riders.gmdb.base import GmdbBase

from src.system.projection.time_steps import TimeSteps

from src.data_sources.annuity import AnnuityDataSources
from src.data_sources.annuity.model_points.model_point.riders.gmdb import Gmdb as GmdbDataSource

if TYPE_CHECKING:
    from src.projection_entities.products.annuity.base_contract import BaseContract


class GmdbRav(
    GmdbBase
):

    """
    GMDB Return of Account Value rider.
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

        """
        Sets benefit base to
        :attr:`account value <src.projection_entities.products.annuity.base_contract.BaseContract.account_value>`.

        :param base_contract: Base contract.
        :return: Nothing.
        """

        self.benefit_base[self.time_steps.t] = base_contract.account_value
