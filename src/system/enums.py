"""
System-wide enumerations.
"""

from enum import StrEnum


class LoggerLevel(
    StrEnum
):

    """
    Enum for different logging levels.
    """

    MESSAGE = 'MESSAGE'     #: Message-level indicator.
    WARNING = 'WARNING'     #: Warning-level indicator.
    ERROR = 'ERROR'         #: Error-level indicator. Using this may raise an exception.


class ProcessingType(
    StrEnum
):

    """
    Enum for different projection processing types.
    """

    SINGLE_PROCESS = 'single_process'       #: Single-process (vanilla Python).
    MULTI_PROCESS = 'multi_process'         #: Multi-process (using the `multiprocessing` module).


class Gender(
    StrEnum
):

    """
    Enum that represents gender.
    """

    MALE = 'male'           #: Male gender.
    FEMALE = 'female'       #: Female gender.


class ProductType(
    StrEnum
):

    """
    Enum that represents product types.
    """

    FIXED_ANNUITY = 'fa'            #: Fixed Annuity product type.
    FIXED_INDEXED_ANNUITY = 'ia'    #: Fixed Indexed Annuity product type.
    VARIABLE_ANNUITY = 'va'         #: Variable Annuity product type.


class AccountType(
    StrEnum
):

    """
    Enum that represents account types.
    """

    FIXED = 'fixed'             #: Fixed account crediting.
    INDEXED = 'indexed'         #: Indexed account crediting.
    SEPARATE = 'separate'       #: Separate account crediting (used for Variable Annuities).


class Rider(
    StrEnum
):

    """
    Enum that represents different riders.
    """

    GUARANTEED_MINIMUM_WITHDRAWAL_BENEFIT = 'gmwb'  #: Guaranteed Minimum Withdrawal Benefit Rider (Annuity, GMWB).
    GUARANTEED_MINIMUM_DEATH_BENEFIT = 'gmdb'       #: Guaranteed Minimum Death Benefit Rider (Annuity, GMDB).


class DeathBenefitOptions(
    StrEnum
):

    """
    Enum that represents different death benefit options.
    """

    RETURN_OF_ACCOUNT_VALUE = 'rav'     #: Return of Account Value GMDB Option.
    RETURN_OF_PREMIUM = 'rop'           #: Return of Premium GMDB Option.
    ACCOUNT_VALUE_RATCHET = 'mav'       #: Annual Ratchet GMDB Option.
