#!/bin/env python
import datetime
from enum import Enum
from time import time
import tkinter as tk
from tkinter import Event, messagebox
import tkinter
from tkinter import font
from tkinter.constants import DISABLED, FALSE, TRUE
from tkinter import scrolledtext

import kics_register
import vpn_control


class STATE_VAR(Enum):
    KINMU_MAE = 0
    KINMU_CHU = 1
    KYUKEI_CHU = 2
    STATE_TOTAL = 3  # dummy


class ACTION_VAR(Enum):
    KINMU_START = 0
    KINMU_END = 1
    KINMU_RESTART = 2
    KYUKEI_START = 3
    ACTION_TOAL = 4  # dummy


class BUTTON_ID(Enum):
    KINMU_START_BUTTON = 0
    KINMU_END_BUTTON = 1
    KYUKEI_START_BUTTON = 2
    KYUKEI_END_BUTTON = 3
    BUTTON_TOTAL = 4  # dummy


class EVENT_VAR(Enum):
    KINMU_START_BUTTON_PUSHED = 0
    KINMU_END_BUTTON_PUSHED = 1
    KYUKEI_START_BUTTON_PUSHED = 2
    KYUKEI_END_BUTTON_PUSHED = 3
    EVENT_TOTAL = 4  # dummy


NEXT_STATE_TBL = (
    (STATE_VAR.KINMU_CHU,
     STATE_VAR.STATE_TOTAL,
     STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL,
     STATE_VAR.KINMU_MAE,
     STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL,
     STATE_VAR.KYUKEI_CHU,
     STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL,
     STATE_VAR.STATE_TOTAL,
     STATE_VAR.KINMU_CHU))

ACTION_TBL = (
    (ACTION_VAR.KINMU_START,
     ACTION_VAR.ACTION_TOAL,
     ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL,
     ACTION_VAR.KINMU_END,
     ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL,
     ACTION_VAR.KYUKEI_START,
     ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL,
     ACTION_VAR.ACTION_TOAL,
     ACTION_VAR.KINMU_RESTART))

CONFIRM_MSG_TBL = ["在宅勤務を開始します。よろしいですか",
                   "在宅勤務を終了します。よろしいですか",
                   "在宅勤務を再開します。よろしいですか",
                   "休憩を開始し勤務を中断します（業務外）。 \
                    \nよろしいですか"]


class EventManage():
    # state machine event management
    state_var = STATE_VAR.KINMU_MAE

    def do_action(self, event_id: EVENT_VAR):
        EventManage.new_state = NEXT_STATE_TBL[event_id.value][EventManage.state_var.value]
        EventManage.action = ACTION_TBL[event_id.value][EventManage.state_var.value]
        # print("confirm")
        ret = TRUE
        # msg = CONFIRM_MSG_TBL[EventManage.action.value]
        # ret = messagebox.askyesno("確認", msg)
        if ret == TRUE:
            # ここで直接gyomuを参照してるのが微妙
            gyomu.get_time()
            gyomu.log_stamp(self)
            if EventManage.action == ACTION_VAR.KINMU_END:
                act_kinmu_end(self)
            elif EventManage.action == ACTION_VAR.KINMU_START:
                pass

            # if state_var==STATE_VAR.KINMU_CHU:
                # vpn_control.vpn_control("disconnect")
            # else :
                # vpn_control.vpn_control("connect")

            EventManage.state_var = EventManage.new_state


class ButtonElement(EventManage):
    def __init__(
            self,
            frame,
            text,
            event_id: EVENT_VAR,
            button_id: BUTTON_ID,
            state=tk.NORMAL):
        self.text = tk.StringVar(frame)
        self.text.set(text)
        self.event_id = event_id
        self.button_id = button_id
        self.font = ("MSゴシック", "20", "bold")
        self.b_element = tk.Button(
            master=frame,
            textvariable=self.text,
            font=self.font,
            command=self.click,
            state=state)

    def click(self):
        super().do_action(self.event_id)
        update_button()

    def activate(self):
        self.b_element.config(state=tk.NORMAL, background="palegreen",
                              activebackground="limegreen", relief=tk.RAISED)

    def inactivate(self):
        self.b_element.config(
            state=tk.DISABLED, background="gray", relief=tk.GROOVE)


class InputForm():
    def __init__(self, master, text, font, show='init'):
        self.label = tk.Label(master=master, text=text, font=font)
        if show != 'init':
            self.entry = tk.Entry(master=master, show=show)
        else:
            self.entry = tk.Entry(master=master)

    def pack(self, *arg):
        self.label.pack(*arg)
        self.entry.pack(*arg)

    def get(self) -> str:
        return self.entry.get()

    def insert(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class TimeLine():
    def __init__(self, log_area: scrolledtext.ScrolledText):
        self.timelist = []
        self.stamp_count = 1
        self.stamp_str = []
        self.log_area = log_area
        self.log_area.config(state='disable')

    def get_time(self):
        self.timelist.append(datetime.datetime.now())
        # self.log_stamp()

    def reset(self):
        self.timelist = []

    def log_stamp(self, obj: ButtonElement):
        MSG_TABLE = ("勤務開始", "勤務終了", "休憩終了", "休憩開始")
        date = str(gyomu.timelist[-1].month) + \
            '/' + str(gyomu.timelist[-1].day)
        time = str(gyomu.timelist[-1].hour) + ':' + \
            str(gyomu.timelist[-1].minute)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[EventManage.state_var.value] + '\n'
        self.log_area.config(state='normal')
        self.log_area.insert(str(self.stamp_count) + '.0', log_msg)
        self.log_area.config(state='disable')
        self.log_area.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1


def error(num):
    messagebox.showerror("error", "error occur" + num)
    exit(False)


def act_kinmu_end(obj):
    user = form_id.get()
    password = form_pass.get()
    # err = kics_register.KICS_acess(gyomu.timelist, user, password)
    gyomu.reset()
    err = True
    if not err:
        error('kics_err')


def update_button():
    BUTTON_STATE_TBL = (('activate', 'inactivate', 'inactivate'),
                        ('inactivate', 'activate', 'inactivate'),
                        ('inactivate', 'activate', 'inactivate'),
                        ('inactivate', 'inactivate', 'activate'))

    for button in b_array:
        if BUTTON_STATE_TBL[button.button_id.value][EventManage.new_state.value] == 'activate':
            button.activate()
        elif BUTTON_STATE_TBL[button.button_id.value][EventManage.new_state.value] == 'inactivate':
            button.inactivate()


def bind_sample(event):
    # bindsample
    # window.bind("<Button-3>", bind_sample)
    print('a')


if __name__ == "__main__":
    # ウィンドウ設定
    window = tk.Tk()
    window.geometry('200x400')
    window.title('サンプル画面')
    window.resizable(False, False)

    default_font = ("MSゴシック", "10", "bold")

    form_id = InputForm(master=window, text="DSC-ID", font=default_font)
    form_pass = InputForm(master=window, text="Password",
                          font=default_font, show="*")

    b_kinmu_start = ButtonElement(
        frame=window,
        text="勤務開始",
        button_id=BUTTON_ID.KINMU_START_BUTTON,
        event_id=EVENT_VAR.KINMU_START_BUTTON_PUSHED)
    b_kinmu_end = ButtonElement(
        frame=window,
        text="勤務終了",
        button_id=BUTTON_ID.KINMU_END_BUTTON,
        event_id=EVENT_VAR.KINMU_END_BUTTON_PUSHED)
    b_kyukei_start = ButtonElement(
        frame=window,
        text="休憩開始",
        button_id=BUTTON_ID.KYUKEI_START_BUTTON,
        event_id=EVENT_VAR.KYUKEI_START_BUTTON_PUSHED)
    b_kyukei_end = ButtonElement(
        frame=window,
        text="休憩終了",
        button_id=BUTTON_ID.KYUKEI_END_BUTTON,
        event_id=EVENT_VAR.KYUKEI_END_BUTTON_PUSHED)

    # このへんもっといい実装方法ありそう
    b_array = (b_kinmu_start, b_kinmu_end, b_kyukei_start, b_kyukei_end)

    log = scrolledtext.ScrolledText(
        master=window, width=20, height=10, bd=5, state='disabled')

    # 配置

    # form_id.pack()
    # form_pass.pack()
    b_kinmu_start.b_element.pack()
    b_kinmu_end.b_element.pack()
    b_kyukei_start.b_element.pack()
    b_kyukei_end.b_element.pack()
    log.pack()

    b_kinmu_start.activate()
    b_kinmu_end.inactivate()
    b_kyukei_start.inactivate()
    b_kyukei_end.inactivate()

    gyomu = TimeLine(log)

    window.mainloop()
