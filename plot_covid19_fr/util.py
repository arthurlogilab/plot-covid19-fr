from datetime import datetime, timedelta

import numpy as np

from numba import jit

# from transonic import jit

from .load_data import population

default_first_day_in_plot = "2020-09-01"


fmt_date = "%Y-%m-%d"


def create_date_object(date: str):
    return datetime.strptime(date, fmt_date)


def format_date_for_human(date: str):
    date_obj = create_date_object(date)
    return date_obj.strftime("%d/%m/%Y")


def format_date(date_obj):
    return date_obj.strftime(fmt_date)


def shift_date_str(date: str, nb_days: int):
    date_new = create_date_object(date) + timedelta(nb_days)
    return format_date(date_new)


@jit
def cumul7(data: "int[]"):
    n = 7
    ret = np.empty_like(data)

    tmp = 0
    for i in range(n):
        ret[i] = tmp = tmp + data[i]

    for i in range(n, len(data)):
        ret[i] = tmp = tmp + data[i] - data[i - n]

    return ret


def complete_df_1loc_1age(tmp, dep=None):

    tmp["Tc"] = cumul7(tmp["T"].values)
    tmp["Pc"] = cumul7(tmp["P"].values)
    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]

    if dep is not None:
        tmp["incidence"] = 100000 / population[dep] * tmp["Pc"]
