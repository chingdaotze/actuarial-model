from typing import Dict

from src.data_sources.model_points.model_point.person import Person


class Annuitant(
    Person
):

    def __init__(
        self,
        data: Dict
    ):

        Person.__init__(
            self=self,
            data=data
        )
