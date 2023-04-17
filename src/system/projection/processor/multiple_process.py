"""
:class:`~src.system.projection.Projection` processing,
using Python's `multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ module.
"""

from tqdm import tqdm
from psutil import cpu_count
from multiprocessing import (
    Manager,
    Pool,
    Queue
)
from traceback import format_exc

from src.system.projection.processor import ProjectionProcessor
from src.system.projection.parameters import ProjectionParameters
from src.system.logger import Logger
from src.system.enums import LoggerLevel


class PoisonPill:

    """
    Marker that indicates the end of a work queue. Each poison pill "kills" a worker process.
    """

    def __init__(self):

        pass


class MultiProcessProjectionProcessor(
    ProjectionProcessor
):

    """
    :class:`~src.system.projection.processor.ProjectionProcessor` that uses Python's
    `multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ module to calculate
    :class:`Projections <src.system.projection.Projection>`.
    """

    def __init__(
        self,
        projection_parameters: ProjectionParameters
    ):

        ProjectionProcessor.__init__(
            self=self,
            projection_parameters=projection_parameters
        )

    @staticmethod
    def progress_bar(
        out_queue: Queue,
        projection_count: int,
        cpus: int
    ) -> None:

        """
        Progress bar display that monitors and updates based on items in a queue.

        :param out_queue: Progress bar monitoring target.
        :param projection_count: Number of expected projections.
        :param cpus: Number of parallel processes.
        :return: None
        """

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

        """
        Worker that consumes work from a queue, and executes work. If the worker consumes a :class:`PoisonPill`,
        the worker quits and "dies".

        :param in_queue: Work input queue.
        :param out_queue: Work output queue.
        :return: None
        """

        while True:

            work_item = in_queue.get()

            if not isinstance(work_item, PoisonPill):

                try:

                    cls.run_projection(
                        projection=work_item
                    )

                except Exception as expr:

                    Logger().print(
                        message=format_exc(),
                        level=LoggerLevel.ERROR
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

        """
        Runs :class:`projections <src.system.projection.Projection>` in parallel, using Python's
        `multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ module, by:

        #. Creating `Queue <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue>`_ objects.
        #. Feeding :attr:`~src.system.projection.processor.ProjectionProcessor.projections` into the Queue.
        #. Feeding :class:`poison pills <PoisonPill>` into the Queue, one for each worker process.
        #. Spinning up workers using a
           `Pool <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool>`_.
        #. Processing all items in the Queue using the Pool.
        
        .. note::
            If ``cpus`` is ``None``, allow the system to determine the number of CPU's to use. Typically,
            this would be the physical core count - 1.

        :param cpus: Number of processes to run in parallel.
        :return: None
        """

        Logger().print(
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

        Logger().print(
            message=f'Creating pool with {cpus} CPU\'s ...'
        )

        pool: Pool = Pool(
            processes=cpus
        )

        Logger().print(
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

        Logger().print(
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
