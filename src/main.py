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
    for model_point in data_sources.model_points:

        for economic_scenario in data_sources.economic_scenarios:

            logger.print(
                message=f'Calculating model point: {model_point.id}, scenario: {economic_scenario.scenario_index} ...'
            )

            # Construct projection object
            projection = EconomicLiabilityProjection(
                projection_parameters=projection_parameters,
                data_sources=data_sources,
                model_point=model_point,
                economic_scenario=economic_scenario
            )

            # Run projection
            projection.run_projection()

            # Write projection output
            projection_output_path = join(
                output_dir_path,
                f'{model_point.id}_{economic_scenario.scenario_index}'
            )

            if not exists(path=projection_output_path):

                mkdir(
                    path=projection_output_path
                )

            projection.write_output(
                output_dir_path=projection_output_path
            )


if __name__ == '__main__':

    main()
