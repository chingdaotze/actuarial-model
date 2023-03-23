from sys import argv
from datetime import date
from dateutil.relativedelta import relativedelta
from os.path import (
    join,
    exists
)
from os import mkdir

from src.system.odometer import odometer
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import logger

from src.data_sources.annuity import AnnuityDataSources
from src.projections.annuity.base.economic_liability import EconomicLiabilityProjection


@odometer
def main() -> None:

    r"""
    Sample function that:

    1. Constructs a projection parameters object.
    2. Uses the projection parameters object to construct a data sources object, which represents holds inputs
       for the model.
    3. Uses the projection parameters and data sources objects to construct a projection object.
    4. Runs the projection using the projection object.
    5. Writes projection output using the projection object, to project's the \output directory.

    :return:
    """

    # Read command-line arguments
    resource_dir_path = argv[1]
    output_dir_path = argv[2]

    # Construct projection parameters
    projection_parameters = ProjectionParameters(
        start_t=date(
            year=2023,
            month=3,
            day=16
        ),
        projection_length=relativedelta(
            years=30
        ),
        time_step=relativedelta(
            months=1
        ),
        resource_dir_path=resource_dir_path
    )

    # Construct data sources
    data_sources = AnnuityDataSources(
        projection_parameters=projection_parameters
    )

    # Run projections
    for configured_data_source in data_sources.configured_data_sources():

        logger.print(
            message=f'Calculating model point: {configured_data_source.model_point}, '
                    f'scenario: {configured_data_source.economic_scenario} ...'
        )

        # Construct projection object
        projection = EconomicLiabilityProjection(
            projection_parameters=projection_parameters,
            data_sources=data_sources
        )

        # Run projection
        projection.run_projection()

        # Write projection output
        model_point_dir_path = join(
            output_dir_path,
            configured_data_source.model_point.id
        )

        if not exists(path=model_point_dir_path):
            mkdir(
                path=model_point_dir_path
            )

        economic_scenario_dir_path = join(
            model_point_dir_path,
            str(configured_data_source.economic_scenario.scenario_index)
        )

        if not exists(path=economic_scenario_dir_path):
            mkdir(
                path=economic_scenario_dir_path
            )

        projection.write_output(
            output_dir_path=economic_scenario_dir_path
        )


if __name__ == '__main__':

    main()
