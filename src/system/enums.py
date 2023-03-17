from enum import StrEnum


class Gender(
    StrEnum
):

    MALE = 'male'
    FEMALE = 'female'


class ProductType(
    StrEnum
):

    FIXED_ANNUITY = 'fa'
    FIXED_INDEXED_ANNUITY = 'ia'
    VARIABLE_ANNUITY = 'va'
