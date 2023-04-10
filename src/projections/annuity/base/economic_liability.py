from os.path import (
    exists,
    join
)
from os import mkdir

from src.system.projection import Projection
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.annuity import AnnuityDataSources

from src.projection_entities.economy import Economy
from src.projection_entities.products.annuity.base_contract import BaseContract


class EconomicLiabilityProjection(
    Projection
):

    """
    Sample economic liability projection.
    """

    data_sources: AnnuityDataSources

    def __init__(
        self,
        projection_parameters: ProjectionParameters,
        data_sources: AnnuityDataSources
    ):

        Projection.__init__(
            self=self,
            projection_parameters=projection_parameters,
            data_sources=data_sources
        )

        self.economy: Economy = Economy(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

        self.base_contract: BaseContract = BaseContract(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

    def __str__(
        self
    ) -> str:

        return f'{self.data_sources.model_point.id} || {self.data_sources.economic_scenario.scenario_index}'

    def setup_output(
        self
    ) -> None:

        model_point_dir_path = join(
            self.projection_parameters.output_dir_path,
            self.data_sources.model_point.id
        )

        if not exists(path=model_point_dir_path):

            mkdir(
                path=model_point_dir_path
            )

        economic_scenario_dir_path = join(
            model_point_dir_path,
            str(self.data_sources.economic_scenario.scenario_index)
        )

        if not exists(path=economic_scenario_dir_path):
            mkdir(
                path=economic_scenario_dir_path
            )

        self.output_dir_path = economic_scenario_dir_path

    def project_time_step(
        self
    ) -> None:

        self.economy.age_economy()

        self.base_contract.age_contract()

        self.base_contract.process_premiums()

        self.base_contract.credit_interest()

        self.base_contract.assess_charges()

        self.base_contract.process_withdrawals()

        self.base_contract.update_gmdb_naar()

        self.base_contract.update_cash_surrender_value()

        self.base_contract.annuitants.update_decrements()
