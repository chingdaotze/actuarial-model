from os.path import exists
from json import load
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Self

from src.system.logger import logger
from src.system.enums import ProcessingType


class ProjectionParameters:

    """
    Container class for all projection parameters. Additional projection parameters can be added here
    (for all projections), or this class can be inherited and extended for additional parameters.
    """

    # Time
    start_t: date
    projection_length: relativedelta
    end_t: date
    time_step: relativedelta

    # Paths
    resource_dir_path: str
    output_dir_path: str

    # Processing
    processing_type: ProcessingType

    # Projection
    projection: str
    data_source: str

    def __init__(
        self,
        start_t: date,
        projection_length: relativedelta,
        time_step: relativedelta,
        resource_dir_path: str,
        output_dir_path: str,
        processing_type: ProcessingType,
        projection: str,
        data_source: str
    ):
        """
        Constructor method.

        :param start_t:
        :param projection_length:
        :param time_step:
        :param resource_dir_path:
        """

        # Time
        self.start_t: date = start_t
        self.projection_length: relativedelta = projection_length
        self.end_t: date = start_t + projection_length
        self.time_step: relativedelta = time_step

        # Paths
        self.resource_dir_path = resource_dir_path
        self.output_dir_path = output_dir_path

        # Processing
        self.processing_type = processing_type

        # Projection
        self.projection = projection
        self.data_source = data_source

    @classmethod
    def from_json(
        cls,
        path: str
    ) -> Self:

        """
        Class factory that constructs an instance by deserializing a JSON file.

        :param path:
        :return:
        """

        if not exists(path):

            logger.raise_expr(
                expr=FileNotFoundError(
                    f'Could not locate projection parameter file at this location: {path} !'
                )
            )

        with open(file=path, mode='r') as json_file:

            json_payload = load(
                fp=json_file
            )

        projection_parameters = ProjectionParameters(
            start_t=date(
                year=int(json_payload['start_year']),
                month=int(json_payload['start_month']),
                day=int(json_payload['start_day'])
            ),
            projection_length=relativedelta(
                years=int(json_payload['projection_years']),
                months=int(json_payload['projection_months']),
                days=int(json_payload['projection_days'])
            ),
            time_step=relativedelta(
                years=int(json_payload['time_step_years']),
                months=int(json_payload['time_step_months']),
                days=int(json_payload['time_step_days'])
            ),
            resource_dir_path=json_payload['resource_dir_path'],
            output_dir_path=json_payload['output_dir_path'],
            processing_type=ProcessingType(
                json_payload['processing_type']
            ),
            projection=json_payload['projection'],
            data_source=json_payload['data_source']
        )

        return projection_parameters
