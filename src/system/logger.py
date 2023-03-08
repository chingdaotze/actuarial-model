from typing import (
    Self,
    TextIO,
    NoReturn
)
from uuid import uuid4
from os.path import (
    join,
    dirname,
    abspath
)
from datetime import datetime
from multiprocessing import Lock

from src.system.constants import DATETIME_FORMAT


class Logger:

    """
    Singleton logger object.
    """

    instance: Self = None
    log_file: TextIO = None
    lock: Lock = Lock()

    def __new__(
        cls
    ):

        if cls.instance is None:

            cls.instance = super(
                Logger,
                cls
            ).__new__(
                cls
            )

            log_file_path = abspath(
                join(
                    dirname(
                        __file__
                    ),
                    r'..\..\log',
                    f'{str(uuid4())}.log'
                )
            )

            cls.log_file = open(
                file=log_file_path,
                mode='w'
            )

            cls.instance.print(
                f'Created new log file here: {log_file_path} !'
            )

        return cls.instance

    @property
    def timestamp(
        self
    ) -> str:

        """
        Returns a timestamp as-of now.

        :return:
        """

        return datetime.now().strftime(
            DATETIME_FORMAT
        )

    def print(
        self,
        message: str
    ) -> None:

        """
        Prints a message to both console and log file.

        :param message:
        :return:
        """

        wrapped_message = f'MESSAGE || {self.timestamp} || {message}'

        self.lock.acquire()

        print(
            wrapped_message
        )

        print(
            wrapped_message,
            file=self.log_file
        )

        self.lock.release()

    def raise_expr(
        self,
        expr: Exception
    ) -> NoReturn:

        """
        Logs an exception in both the console and log file.

        :param expr:
        :return:
        """

        error_indicator_message = f'ERROR || {self.timestamp} || Traceback below:'

        self.lock.acquire()

        print(
            error_indicator_message
        )

        print(
            error_indicator_message,
            file=self.log_file
        )

        print(
            expr,
            file=self.log_file
        )

        self.lock.release()

        raise expr


logger = Logger()
