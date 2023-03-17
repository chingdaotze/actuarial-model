from sys import argv
from datetime import date
from dateutil.relativedelta import relativedelta

from src.system.odometer import odometer
from src.system.projection.parameters import ProjectionParameters

from src.data_sources.annuity import AnnuityDataSources


@odometer
def main() -> None:

    # Construct projection parameters
    projection_parameters = ProjectionParameters(
        start_t=date(
            year=2023,
            month=3,
            day=17
        ),
        projection_length=relativedelta(
            years=30
        ),
        time_step=relativedelta(
            months=1
        ),
        resource_dir_path=argv[1]
    )

    # TODO: Construct data sources
    annuity_data_sources = AnnuityDataSources(
        projection_parameters=projection_parameters
    )

    # TODO: Construct projection object

    # TODO: Run projection
    ...


if __name__ == '__main__':

    main()
