from datetime import (
    date,
    datetime
)

from src.system.constants import DATE_FORMAT


def str_to_date(
    target_str: str
) -> date:

    return datetime.strptime(
        target_str,
        DATE_FORMAT
    ).date()


def date_to_str(
    target_date: date
) -> str:

    return target_date.strftime(
        DATE_FORMAT
    )

