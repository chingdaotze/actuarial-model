"""
System-wide message and event logging.
"""

from typing import (
    ClassVar,
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
from src.system.enums import LoggerLevel


class Logger:

    """
    Singleton logger class. Writes messages to disk and prints messages to console.
    """

    instance: ClassVar[Self] = None     #: Global singleton instance.
    log_file: ClassVar[TextIO] = None   #: Log file object; console output is piped here.
    lock: ClassVar[Lock] = Lock()       #: Lock object to prevent race conditions when writing to the log file.

    def __new__(
        cls
    ):

        """
        Singleton constructor. If an instance does not exist, create a new instance and store it. If an instance
        does exist, return the existing instance.
        """

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

        :return: Returns a timestamp as a string.
        """

        return datetime.now().strftime(
            DATETIME_FORMAT
        )

    def print(
        self,
        message: str,
        level: LoggerLevel = LoggerLevel.MESSAGE
    ) -> None:

        """
        Prints a message to both console and log file.

        :param message: Message to print.
        :param level: Logging level and severity.
        :return: Nothing.
        """

        wrapped_message = f'{level} || {self.timestamp} || {message}'

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
        Logs an exception in both the console and log file, then raises the exception.

        :param expr: Exception to raise and log.
        :return: Never.
        """

        self.print(
            message='Traceback below:',
            level=LoggerLevel.ERROR
        )

        self.lock.acquire()

        print(
            expr,
            file=self.log_file
        )

        self.lock.release()

        raise expr
