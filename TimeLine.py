import datetime
from time import time
from tkinter import scrolledtext
import tkinter as tk

timelist = []


def get_time():
    timelist.append(datetime.datetime.now())


def reset():
    timelist = []


def bind_sample(event):
    # bindsample
    # window.bind("<Button-3>", bind_sample)
    print('a')


class TimeStampLogBox(scrolledtext.ScrolledText):
    def __init__(self):
        logbox_dict = {'width': 20, 'height': 10, 'bd': 5, 'state': 'disabled'}
        super().__init__(**logbox_dict)
        self.stamp_count = 1
        self.stamp_str = []

    def stamp(self, action_id: int):
        MSG_TABLE = ("勤務開始", "勤務終了", "休憩開始", "休憩終了")
        date = str(timelist[-1].month) + \
            '/' + str(timelist[-1].day)
        time = str(timelist[-1].hour).zfill(2) + ':' + \
            str(timelist[-1].minute).zfill(2)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[action_id] + '\n'
        self.config(state='normal')
        self.insert(str(self.stamp_count) + '.0', log_msg)
        self.config(state='disable')
        self.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1


class TimeInfoFrame(tk.Frame):
    def __init__(self):
        super().__init__(width=200, bd=1, relief=tk.RAISED)
        self.l_work_state_text = tk.StringVar()
        self.l_work_start_text = tk.StringVar()
        self.l_work_sum_text = tk.StringVar()

        self.l_work_state_text.set("勤務前")
        self.l_work_sum_text.set("勤務時間合計")

        self.l_work_state = tk.Label(
            textvariable=self.l_work_state_text, font=(
                "MSポップ", "20", "bold"))
        self.l_work_start = tk.Label(font=("MSポップ", "10", "bold"))
        self.l_work_sum = tk.Label(
            textvariable=self.l_work_sum_text, font=(
                "MSポップ", "10", "bold"))

        self.time_reset()

        self.l_work_state.pack(in_=self)
        self.l_work_start.pack(in_=self)
        self.l_work_sum.pack(in_=self)

    def state_update(self, text: str):
        self.l_work_state_text.set(text)
        self.l_work_state.config(textvariable=self.l_work_state_text)

    def start_update(self, start_time: datetime):
        self.start_time = start_time
        self.start_hour = str(start_time.hour).zfill(2)
        self.start_min = str(start_time.minute).zfill(2)
        self.l_work_start_text.set(
            "開始時刻 " + self.start_hour + ':' + self.start_min)
        self.l_work_start.config(textvariable=self.l_work_start_text)
        self.sum_update()

    def sum_update(self):
        try:
            now_time = datetime.datetime.now()
            time_diff: datetime.timedelta = now_time - self.start_time
            sum_hour = str(time_diff // datetime.timedelta(hours=1)).zfill(2)
            sum_minute = str(
                time_diff.seconds %
                datetime.timedelta(
                    hours=1).seconds //
                60).zfill(2)
            self.l_work_sum_text.set(
                "勤務時間合計 " + sum_hour + "時間" + sum_minute + "分")
            self.l_work_sum.config(textvariable=self.l_work_sum_text)

        except BaseException:
            pass
        finally:
            self.after_id = self.after(60000, self.sum_update)

    def time_reset(self):
        self.l_work_start_text.set("開始時刻 -- : --")
        self.l_work_start.config(textvariable=self.l_work_start_text)
        try :
            self.after_cancel(self.after_id)
        except :
            pass


if __name__ == "__main__":
    pass
