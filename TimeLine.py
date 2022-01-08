#!/bin/env python

import datetime
import tkinter as tk

timelist = []
start_hour = ""
start_min = ""
end_hour = ""
end_min = ""
sum_hour = ""
sum_min = ""


def push_time():
    global timelist
    timelist.append(datetime.datetime.now())


def reset():
    global timelist
    timelist = []


def start_time_calc(start_time: datetime.datetime):
    global start_hour, start_min
    start_hour = str(start_time.hour).zfill(2)
    start_min = str(start_time.minute).zfill(2)


def end_time_calc(end_time: datetime.datetime):
    global end_hour, end_min
    end_hour = str(end_time.hour).zfill(2)
    end_min = str(end_time.minute).zfill(2)


def sum_time_calc():
    global timelist
    if len(timelist) % 2 == 0:  # 休憩中 or 勤務終了
        time_calc()
    else:  # 勤務中
        timelist.append(datetime.datetime.now())
        time_calc()
        timelist.pop()


def time_calc():
    global timelist, sum_hour, sum_min
    work_time_sum: datetime.timedelta = datetime.timedelta()
    for i in range(0, len(timelist), 2):
        work_time_sum += (timelist[i + 1] - timelist[i])

        sum_hour = str(work_time_sum // datetime.timedelta(hours=1)).zfill(2)
        sum_min = str(
            work_time_sum.seconds %
            datetime.timedelta(hours=1).seconds //
            60).zfill(2)


def sum_time_min_rounding():
    global sum_min

    if int(sum_min) >= 45:
        sum_min = "45"
    elif int(sum_min) >= 30:
        sum_min = "30"
    elif int(sum_min) >= 15:
        sum_min = "15"
    else:
        sum_min = "00"


def get_kics_time():
    end_time_calc()
    sum_time_calc()
    sum_time_min_rounding()


if __name__ == "__main__":
    pass
