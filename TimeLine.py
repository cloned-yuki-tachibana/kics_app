import datetime
from tkinter import scrolledtext

timelist = []


def get_time():
    timelist.append(datetime.datetime.now())


def reset():
    timelist = []


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
        time = str(timelist[-1].hour) + ':' + \
            str(timelist[-1].minute)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[action_id] + '\n'
        self.config(state='normal')
        self.insert(str(self.stamp_count) + '.0', log_msg)
        self.config(state='disable')
        self.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1

if __name__ == "__main__":
    pass
