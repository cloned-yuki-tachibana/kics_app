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


class EVENT_VAR(Enum):
    KINMU_BUTTON_PUSHED = 0
    KYUKEI_BUTTON_PUSHED = 1
    EVENT_TOTAL = 2  # dummy


class BUTTON_ID(Enum):
    KINMU_BUTTON = 0
    KYUKEI_BUTTON = 1
    BUTTON_TOTAL = 2  # dummy

    # state
    # kinumae              kinmu chu                 kyukei chu
NEXT_STATE_TBL = [[STATE_VAR.KINMU_CHU,      STATE_VAR.KINMU_MAE,     STATE_VAR.KINMU_CHU],      # event 0
                  [STATE_VAR.STATE_TOTAL,    STATE_VAR.KYUKEI_CHU,    STATE_VAR.STATE_TOTAL]]   # event 1

ACTION_TBL = [[ACTION_VAR.KINMU_START,   ACTION_VAR.KINMU_END,    ACTION_VAR.KINMU_RESTART],  # event 0
              [ACTION_VAR.ACTION_TOAL,   ACTION_VAR.KYUKEI_START, ACTION_VAR.ACTION_TOAL]]   # event 1

BUTTON_TBL = [[("勤務開始", tk.NORMAL),   ("勤務終了", tk.NORMAL), ("勤務再開", tk.NORMAL)],   # button id 0
              [("休憩開始", tk.DISABLED), ("休憩開始", tk.NORMAL), ("休憩開始", tk.DISABLED)]]  # button id 1

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
        #ret = TRUE
        msg = CONFIRM_MSG_TBL[EventManage.action.value]
        ret = messagebox.askyesno("確認", msg)
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
    def __init__(self, frame, text, event_id: EVENT_VAR, button_id: BUTTON_ID, state=tk.NORMAL):
        self.text = tk.StringVar(frame)
        self.text.set(text)
        self.event_id = event_id
        self.button_id = button_id
        self.font = ("MSゴシック", "20", "bold")
        self.b_element = tk.Button(
            master=frame, textvariable=self.text, font=self.font, command=self.click, state=state)

    def click(self):
        super().do_action(self.event_id)
        update_button()


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
        MSG_TABLE = [["勤務開始", "勤務終了", "休憩終了"],
                     ["？",      "休憩開始",  "?"]]
        date = str(gyomu.timelist[-1].month) + \
            '/' + str(gyomu.timelist[-1].day)
        time = str(gyomu.timelist[-1].hour) + ':' + \
            str(gyomu.timelist[-1].minute)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[obj.event_id.value][EventManage.state_var.value] + '\n'
        self.log_area.config(state='normal')
        self.log_area.insert(str(self.stamp_count)+'.0', log_msg)
        self.log_area.config(state='disable')
        self.log_area.see(str(self.stamp_count)+'.0')
        self.stamp_count += 1


def error(num):
    messagebox.showerror("error", "error occur"+num)
    exit(False)


def act_kinmu_end(obj):
    user = id_form.get()
    password = pass_form.get()
    err = kics_register.KICS_acess(gyomu.timelist, user, password)
    gyomu.reset()
    err = True
    if err == False:
        error('kics_err')


def update_button():
    for button in b_array:
        button.text.set(BUTTON_TBL[button.button_id.value]
                        [EventManage.new_state.value][0])
        button.b_element.config(
            state=BUTTON_TBL[button.button_id.value][EventManage.new_state.value][1])


def state_label_update():
    global state_label

    set()


if __name__ == "__main__":
    # ウィンドウ設定
    window = tk.Tk()
    window.geometry('200x400')
    window.title('サンプル画面')
    window.resizable(False, False)

    default_font = ("MSゴシック", "10", "bold")

    state_label = tk.Label(master=window, text="state",
                           font=("MSゴシック", "20", "bold"))

    id_form = InputForm(master=window, text="DSC-ID",   font=default_font)
    pass_form = InputForm(master=window, text="Password",
                          font=default_font, show="*")

    b1 = ButtonElement(frame=window, text="勤務開始", button_id=BUTTON_ID.KINMU_BUTTON,
                       event_id=EVENT_VAR.KINMU_BUTTON_PUSHED)
    b2 = ButtonElement(frame=window, text="休憩開始", button_id=BUTTON_ID.KYUKEI_BUTTON,
                       event_id=EVENT_VAR.KYUKEI_BUTTON_PUSHED, state=tk.DISABLED)

    # このへんもっといい実装方法ありそう
    b_array = (b1, b2)

    log = scrolledtext.ScrolledText(
        master=window, width=20, height=10, bd=5, state='disabled')

    # 配置

    state_label.pack()
    id_form.pack()
    pass_form.pack()
    b1.b_element.pack()
    b2.b_element.pack()
    log.pack()

    gyomu = TimeLine(log)

    window.mainloop()
