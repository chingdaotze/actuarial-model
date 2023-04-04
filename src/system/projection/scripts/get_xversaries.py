from datetime import date
from typing import List
from dateutil.relativedelta import relativedelta
from math import floor


def get_xversaries(
    issue_date: date,
    start_date: date,
    end_date: date,
    frequency: int
) -> List[date]:

    start_date_range = relativedelta(
        dt1=start_date,
        dt2=issue_date
    )

    start_xversary_months = floor((start_date_range.years * 12 + start_date_range.months) / frequency) * frequency

    end_date_rate = relativedelta(
        dt1=end_date,
        dt2=issue_date
    )

    end_xversary_months = floor((end_date_rate.years * 12 + end_date_rate.months) / frequency) * frequency

    max_xversary_date = issue_date + relativedelta(
        months=end_xversary_months
    )

    xversary_date = issue_date + relativedelta(
        months=start_xversary_months
    )

    xversary_dates = []

    while xversary_date < max_xversary_date:
        xversary_date += relativedelta(
            months=frequency
        )

        xversary_dates.append(
            xversary_date
        )

    return xversary_dates
