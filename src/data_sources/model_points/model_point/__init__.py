from abc import ABC
from datetime import (
    date,
    datetime
)

from pandas import Series

from src.system.data_sources.data_source.pandas_series import DataSourcePandasSeries
from src.system.constants import (
    DEFAULT_COL,
    DATE_FORMAT
)
from src.system.enums import ProductType


class ModelPointBase(
    DataSourcePandasSeries,
    ABC
):

    """
    Data source that represents a generic, non-product-specific model point.
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
        Unique identifier. This could be a Policy Number, counting integer, GUID, or any other unique code.

        :return:
        """

        return self.cache[DEFAULT_COL]['id']

    @property
    def product_type(
        self
    ) -> ProductType:

        """
        Product type enum that denotes what kind of product this model point is. For example, Variable Annuity or
        Universal Life.

        :return:
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

        :return:
        """

        return self.cache[DEFAULT_COL]['product_name']

    @property
    def issue_date(
        self
    ) -> date:

        """
        Policy issue date.

        :return:
        """

        return datetime.strptime(
            self.cache[DEFAULT_COL]['issue_date'],
            DATE_FORMAT
        ).date()
