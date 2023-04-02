from tqdm import tqdm
from psutil import cpu_count
from multiprocessing import (
    Manager,
    Pool,
    Queue
)

from src.system.projection.processor import ProjectionProcessor
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import logger


class PoisonPill:

    def __init__(self):

        pass


class MultiProcessProjectionProcessor(
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

    @classmethod
    def progress_bar(
        cls,
        out_queue: Queue,
        projection_count: int,
        cpus: int
    ):

        progress_bar = tqdm(total=projection_count, desc=r'Progress: ', unit=r' projection(s) ')
        poison_pills = 0

        while True:

            work_item = out_queue.get()

            if not isinstance(work_item, PoisonPill):

                progress_bar.update(1)

            else:

                poison_pills += 1

            out_queue.task_done()

            if poison_pills == cpus:

                break

    @classmethod
    def worker(
        cls,
        in_queue: Queue,
        out_queue: Queue
    ) -> None:

        while True:

            work_item = in_queue.get()

            if not isinstance(work_item, PoisonPill):

                cls.run_projection(
                    projection=work_item
                )

            out_queue.put(
                work_item
            )

            in_queue.task_done()

            if isinstance(work_item, PoisonPill):

                break

    def run_projections(
        self,
        cpus: int = None
    ) -> None:

        logger.print(
            message='Starting manager, queue, and pool ...'
        )

        manager = Manager()

        in_queue: Queue = manager.Queue()
        out_queue: Queue = manager.Queue()

        if cpus is None:

            cpus = min(
                max(
                    cpu_count(logical=False) - 1,
                    1
                ),
                len(self.projections)
            )

        logger.print(
            message=f'Creating pool with {cpus} CPU\'s ...'
        )

        pool: Pool = Pool(
            processes=cpus
        )

        logger.print(
            message='Loading projections to queue ...'
        )

        for projection in self.projections:

            in_queue.put(
                projection
            )

        for _ in range(cpus):

            in_queue.put(
                PoisonPill()
            )

        logger.print(
            message='Processing queue ...'
        )

        for _ in range(cpus):

            pool.apply_async(
                func=self.worker,
                kwds={
                    'in_queue': in_queue,
                    'out_queue': out_queue
                }
            )

        pool.close()

        progress_bar_pool = Pool(
            processes=1
        )

        progress_bar_pool.apply_async(
            func=self.progress_bar,
            kwds={
                'out_queue': out_queue,
                'projection_count': len(self.projections),
                'cpus': cpus
            }
        )

        progress_bar_pool.close()

        # Wait here until queues are done
        in_queue.join()
        out_queue.join()

        # Join pools
        pool.join()
        progress_bar_pool.join()
