from enum import StrEnum


class LoggerLevel(
    StrEnum
):

    """
    Enum for different projection processing types.
    """

    MESSAGE = 'MESSAGE'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class ProcessingType(
    StrEnum
):

    """
    Enum for different projection processing types.
    """

    SINGLE_PROCESS = 'single_process'
    MULTI_PROCESS = 'multi_process'


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


class AccountType(
    StrEnum
):

    """
    Enum that represents account types.
    """

    FIXED = 'fixed'
    INDEXED = 'indexed'
    SEPARATE = 'separate'


class Rider(
    StrEnum
):

    """
    Enum that represents different riders.
    """

    GUARANTEED_MINIMUM_WITHDRAWAL_BENEFIT = 'gmwb'
    GUARANTEED_MINIMUM_DEATH_BENEFIT = 'gmdb'


class DeathBenefitOptions(
    StrEnum
):

    """
    Enum that represents different death benefit options.
    """

    RETURN_OF_ACCOUNT_VALUE = 'rav'
    RETURN_OF_PREMIUM = 'rop'
    ACCOUNT_VALUE_RATCHET = 'mav'
