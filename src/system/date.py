from datetime import (
    date,
    datetime
)

from dateutil.relativedelta import relativedelta

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


def calc_partial_years(
    dt1: date,
    dt2: date
) -> float:

    delta = relativedelta(
        dt1=dt1,
        dt2=dt2
    )

    if delta.months or delta.days:

        prior_anniversary_date = dt2 + relativedelta(
            years=delta.years
        )

        next_anniversary_date = dt2 + relativedelta(
            years=delta.years + 1
        )

        partial_year_days = (dt1 - prior_anniversary_date).days
        total_year_days = (next_anniversary_date - prior_anniversary_date).days

        years = delta.years + (partial_year_days / total_year_days)

    else:

        years = float(delta.years)

    return years


def relativedelta_to_partial_years(
    delta: relativedelta
) -> float:

    years = (
        delta.years +
        delta.months / 12.0 +
        delta.days / 365.0
    )

    return years


def calc_whole_years(
    dt1: date,
    dt2: date
) -> int:

    delta = relativedelta(
        dt1=dt1,
        dt2=dt2
    )

    if delta:

        if delta.months or delta.days:

            years = delta.years + 1

        else:

            years = delta.years

    else:

        years = 1

    return years
