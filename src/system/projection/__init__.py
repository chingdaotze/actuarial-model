from abc import ABC
from datetime import date


class Projection(
    ABC
):

    """
    Abstract class that represents a projection.
    """

    def __init__(
        self,
        start_t: date
    ):

        self.t: date = start_t
