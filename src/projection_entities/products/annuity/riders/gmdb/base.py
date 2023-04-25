"""
Abstract base class for Guaranteed Minimum Death Benefit rider.
"""

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

    """
    Abstract base class for Guaranteed Minimum Death Benefit rider.
    """

    data_sources: AnnuityDataSources

    rider_name: str

    benefit_base: ProjectionValue           #: Benefit base, used to calculate death benefit payout.
    charge_rate: ProjectionValue            #: Charge rate, used to calculate the charge amount.
    charge_amount: ProjectionValue          #: Charge amount, assessed against the account value.
    net_amount_at_risk: ProjectionValue     #: Net Amount At Risk (NAAR).

    def __init__(
        self,
        time_steps: TimeSteps,
        data_sources: AnnuityDataSources,
        gmdb_data_source: GmdbDataSource
    ):

        """
        Constructor method.

        :param time_steps: Projection-wide timekeeping object.
        :param data_sources: Annuity data sources.
        :param gmdb_data_source: GMDB rider data source.
        """

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

        """
        Adds premiums paid from the base contract into the :attr:`benefit base <benefit_base>`.

        :param base_contract: Base contract.
        :return: Nothing.
        """

        self.benefit_base[self.time_steps.t] = \
            self.benefit_base + base_contract.premium_new[self.time_steps.t]

    def process_charge(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        r"""
        Every month, charges the base contract for the GMDB fee.

        .. math::
            GMDB \, charge = account \, value \times \frac{GMDB \, charge \, rate}{12}

        :math:`GMDB \, charge \, rate` is read from
        :meth:`~src.data_sources.annuity.product.gmdb.charge.GmdbCharge.charge_rate`.

        Applies charge to the base contract using
        :meth:`~src.projection_entities.products.annuity.base_contract.BaseContract.assess_charge`.

        :param base_contract: Base contract.
        :return: Nothing.
        """

        self.charge_amount[self.time_steps.t] = 0.0

        for _ in base_contract.monthiversaries:

            self.charge_rate[self.time_steps.t] = self.data_sources.product.gmdb_rider.gmdb_charge.charge_rate(
                rider_name=self.rider_name
            )

            self.charge_amount[self.time_steps.t] = \
                self.charge_amount + base_contract.account_value * (self.charge_rate / 12.0)

        base_contract.assess_charge(
            charge_amount=self.charge_amount,
            charge_account_name='gmdb_charge'
        )

    @abstractmethod
    def update_benefit_base(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        """
        Abstract method to update the benefit base.

        :param base_contract: Base contract.
        :return: Nothing.
        """

        ...

    def update_net_amount_at_risk(
        self,
        base_contract: 'BaseContract'
    ) -> None:

        r"""
        Calculates and updates the Net Amount At Risk (NAAR):

        .. math::
            NAAR = max(benefit\, base - account\, value, 0)

        :param base_contract: Base contract.
        :return: Nothing.
        """

        self.net_amount_at_risk[self.time_steps.t] = max(
            self.benefit_base - base_contract.account_value,
            0.0
        )
