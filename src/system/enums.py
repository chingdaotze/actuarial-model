from enum import StrEnum


class Gender(
    StrEnum
):

    """
    Enum that represents gender.
    """

    MALE = 'male'
    FEMALE = 'female'


class ProductType(
    StrEnum
):

    """
    Enum that represents product types.
    """

    FIXED_ANNUITY = 'fa'
    FIXED_INDEXED_ANNUITY = 'ia'
    VARIABLE_ANNUITY = 'va'
