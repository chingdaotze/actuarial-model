"""
:mod:`Data source <src.system.data_sources.data_source>` for a single annuitant.
"""

from typing import Dict

from src.data_sources.model_points.model_point.person import Person


class Annuitant(
    Person
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a single annuitant.
    """

    def __init__(
        self,
        data: Dict
    ):

        """
        Constructor method. Initializes an annuitant based on data within an annuity model point file.

        :param data: Data for a single annuitant.
        """

        Person.__init__(
            self=self,
            data=data
        )
