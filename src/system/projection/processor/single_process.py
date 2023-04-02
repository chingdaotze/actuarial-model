from tqdm import tqdm

from src.system.projection.processor import ProjectionProcessor
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import logger


class SingleProcessProjectionProcessor(
    ProjectionProcessor
):

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        ProjectionProcessor.__init__(
            self=self,
            projection_parameters=projection_parameters
        )

    def run_projections(
        self
    ) -> None:

        logger.print(
            message=f'Running projections ...'
        )

        projections = tqdm(self.projections, desc=r'Progress: ', unit=r' projection(s) ')

        for projection in projections:

            self.run_projection(
                projection=projection
            )
