from sys import argv
from datetime import date
from dateutil.relativedelta import relativedelta

from src.system.odometer import odometer
from src.system.projection.processor.multiple_process import MultiProcessProjectionProcessor
from src.system.projection.processor.single_process import SingleProcessProjectionProcessor

from src.system.enums import ProcessingType
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import Logger


@odometer
def main() -> None:

    r"""
    Sample function that:

    #. Constructs a :class:`~src.system.projection.parameters.ProjectionParameters` object.
    #. Constructs a :class:`~src.system.projection.processor.ProjectionProcessor` object.
    #. Uses the :class:`~src.system.projection.processor.ProjectionProcessor` to run the projections
       specified in :class:`~src.system.projection.parameters.ProjectionParameters`.

    :return: Nothing.
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
        resource_dir_path=resource_dir_path,
        output_dir_path=output_dir_path,
        processing_type=ProcessingType.MULTI_PROCESS,
        projection='src.projections.annuity.base.economic_liability.EconomicLiabilityProjection',
        data_source='src.data_sources.annuity.AnnuityDataSources'
    )

    # Create projection processor
    projection_processor = None  # FIXME: https://youtrack.jetbrains.com/issue/PY-24273

    if projection_parameters.processing_type == ProcessingType.MULTI_PROCESS:

        projection_processor = MultiProcessProjectionProcessor(
            projection_parameters=projection_parameters
        )

    elif projection_parameters.processing_type == ProcessingType.SINGLE_PROCESS:

        projection_processor = SingleProcessProjectionProcessor(
            projection_parameters=projection_parameters
        )

    else:

        Logger().raise_expr(
            expr=NotImplementedError(
                f'Unhandled processing type: {projection_parameters.processing_type} !'
            )
        )

    # Setup output
    projection_processor.setup_output()

    # Run projections
    projection_processor.run_projections()


if __name__ == '__main__':

    main()
