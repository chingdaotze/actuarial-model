"""
:mod:`Data source <src.system.data_sources.data_source>` for a single generic, non-product-specific model point.
"""

from abc import ABC
from datetime import date

from pandas import Series

from src.system.data_sources.data_source.pandas_series import DataSourcePandasSeries
from src.system.constants import DEFAULT_COL
from src.system.enums import ProductType
from src.system.date import str_to_date


class ModelPointBase(
    DataSourcePandasSeries,
    ABC
):

    """
    :mod:`Data source <src.system.data_sources.data_source>` for a single generic, non-product-specific model point.
    Contains attributes common across all model points.
    """

    def __init__(
        self,
        data: Series
    ):

        DataSourcePandasSeries.__init__(
            self=self,
            data=data
        )

    @property
    def id(
        self
    ) -> str:

        """
        Unique identifier for this model point. This could be a Policy Number, integer,
        `GUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_,
        or any other unique code.

        :return: Model point ID.
        """

        return self.cache[DEFAULT_COL]['id']

    @property
    def product_type(
        self
    ) -> ProductType:

        """
        Product type enum that denotes what kind of product this model point is. For example, Variable Annuity or
        Universal Life.

        :return: Product type.
        """

        return ProductType(
            self.cache[DEFAULT_COL]['product_type']
        )

    @property
    def product_name(
        self
    ) -> str:

        """
        Human-readable product name.

        :return: Friendly product name.
        """

        return self.cache[DEFAULT_COL]['product_name']

    @property
    def issue_date(
        self
    ) -> date:

        """
        Policy issue date.

        :return: Issue date.
        """

        return str_to_date(
            target_str=self.cache[DEFAULT_COL]['issue_date']
        )
