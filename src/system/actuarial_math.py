from dateutil.relativedelta import relativedelta

from src.system.projection_entity.projection_value import use_latest_value
from src.system.date import relativedelta_to_partial_years


@use_latest_value
def convert_decrement_rate(
    q_x: float,
    interval: relativedelta
) -> float:

    t = relativedelta_to_partial_years(
        delta=interval
    )

    t_p_x = (1.0 - q_x) ** t

    t_q_x = 1.0 - t_p_x

    return t_q_x
