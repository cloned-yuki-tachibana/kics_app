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
    KYUKEI_START = 2
    KYUKEI_END = 3
    ACTION_TOAL = 4  # dummy


# タプルにオブジェクトidを登録する形の方がいい？
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


# [event][state]
NEXT_STATE_TBL = (
    (STATE_VAR.KINMU_CHU, STATE_VAR.STATE_TOTAL, STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL, STATE_VAR.KINMU_MAE, STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL, STATE_VAR.KYUKEI_CHU, STATE_VAR.STATE_TOTAL),
    (STATE_VAR.STATE_TOTAL, STATE_VAR.STATE_TOTAL, STATE_VAR.KINMU_CHU))

ACTION_TBL = (
    (ACTION_VAR.KINMU_START, ACTION_VAR.ACTION_TOAL, ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL, ACTION_VAR.KINMU_END, ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL, ACTION_VAR.KYUKEI_START, ACTION_VAR.ACTION_TOAL),
    (ACTION_VAR.ACTION_TOAL, ACTION_VAR.ACTION_TOAL, ACTION_VAR.KYUKEI_END))

CONFIRM_MSG_TBL = ("在宅勤務を開始します。よろしいですか",
                   "在宅勤務を終了します。よろしいですか",
                   "休憩を開始し勤務を中断します（業務外）。 \
                    \nよろしいですか",
                   "在宅勤務を再開します。よろしいですか")


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
            ButtonElement.update_button()
            # ここで直接gyomuを参照してるのが微妙感ある
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
    b_obj_list = []
    b_state_dict = {}

    def __init__(
            self,
            text: str = '',
            event_id: EVENT_VAR = EVENT_VAR.EVENT_TOTAL,
            button_state: tuple = (),
            *args):
        self.text = tk.StringVar()
        self.text.set(text)
        self.event_id = event_id
        self.font = ("MSゴシック", "15", "bold")
        self.b_element = tk.Button(
            textvariable=self.text,
            font=self.font,
            command=self.click,
            state=tk.NORMAL,
            cursor="hand2")

        ButtonElement.b_obj_list.append({'id': id(self), 'obj': self})
        ButtonElement.b_state_dict[id(self)] = button_state

        self.initial_button_state(button_state[0])

    def click(self):
        super().do_action(self.event_id)

    def activate(self):
        self.b_element.config(state=tk.NORMAL, background="palegreen",
                              activebackground="limegreen", relief=tk.RAISED)

    def inactivate(self):
        self.b_element.config(
            state=tk.DISABLED, background="gray", relief=tk.GROOVE)

    def initial_button_state(self, initial_state):
        if initial_state == 'activate':
            self.activate()
        elif initial_state == 'inactivate':
            self.inactivate()

    @classmethod
    def update_button(cls):
        for b_tuple in cls.b_obj_list:
            if cls.b_state_dict[b_tuple['id']
                                ][EventManage.new_state.value] == 'activate':
                b_tuple['obj'].activate()
            elif cls.b_state_dict[b_tuple['id']][EventManage.new_state.value] == 'inactivate':
                b_tuple['obj'].inactivate()


class ButtonFrame(tk.Frame):
    def __init__(self, leftb_dict: dict, rightb_dict: dict):
        super().__init__()
        self.left_button = ButtonElement(**leftb_dict)
        self.right_button = ButtonElement(**rightb_dict)
        self.left_button.b_element.pack(in_=self, side=tk.LEFT)
        self.right_button.b_element.pack(in_=self, side=tk.RIGHT)


class InputForm(tk.Frame):
    def __init__(self, label_dict: dict, entry_dict: dict):
        super().__init__()
        self.label = tk.Label(**label_dict)
        self.entry = tk.Entry(**entry_dict)
        self.label.pack(in_=self)
        self.entry.pack(in_=self)

    def get(self):
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
        MSG_TABLE = ("勤務開始", "勤務終了", "休憩開始", "休憩終了")
        date = str(gyomu.timelist[-1].month) + \
            '/' + str(gyomu.timelist[-1].day)
        time = str(gyomu.timelist[-1].hour) + ':' + \
            str(gyomu.timelist[-1].minute)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[EventManage.action.value] + '\n'
        self.log_area.config(state='normal')
        self.log_area.insert(str(self.stamp_count) + '.0', log_msg)
        self.log_area.config(state='disable')
        self.log_area.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1


def error(num):
    messagebox.showerror("error", "error occur" + num)
    exit(False)


def act_kinmu_end(obj):
    user = f_form_id.get()
    password = f_form_pass.get()
    # err = kics_register.KICS_acess(gyomu.timelist, user, password)
    gyomu.reset()
    err = True
    if not err:
        error('kics_err')


def bind_sample(event):
    # bindsample
    # window.bind("<Button-3>", bind_sample)
    print('a')


if __name__ == "__main__":
    # ウィンドウ設定
    window = tk.Tk()
    window.geometry('200x400')
    window.title('KICS AUTO')
    window.resizable(False, False)

    default_font = ("MSゴシック", "10", "bold")

    id_label_args = {'text': "DSC-ID", 'font': default_font}
    f_form_id = InputForm(label_dict=id_label_args, entry_dict={})

    pass_label_args = {'text': "Password", 'font': default_font}
    f_form_pass = InputForm(
        label_dict=pass_label_args,
        entry_dict={
            'show': "*"})

    kinmu_start_button_options = {
        'text': "勤務開始",
        'event_id': EVENT_VAR.KINMU_START_BUTTON_PUSHED,
        'button_state': ('activate', 'inactivate', 'inactivate'),
    }
    kinmu_end_button_options = {
        'text': "勤務終了",
        'event_id': EVENT_VAR.KINMU_END_BUTTON_PUSHED,
        'button_state': ('inactivate', 'activate', 'inactivate'),
    }
    f_button_kinmu = ButtonFrame(leftb_dict=kinmu_start_button_options,
                                 rightb_dict=kinmu_end_button_options)

    kyukei_start_button_options = {
        'text': "休憩開始",
        'event_id': EVENT_VAR.KYUKEI_START_BUTTON_PUSHED,
        'button_state': ('inactivate', 'activate', 'inactivate'),
    }
    kyukei_end_button_options = {
        'text': "休憩終了",
        'event_id': EVENT_VAR.KYUKEI_END_BUTTON_PUSHED,
        'button_state': ('inactivate', 'inactivate', 'activate'),
    }
    f_button_kyukei = ButtonFrame(leftb_dict=kyukei_start_button_options,
                                  rightb_dict=kyukei_end_button_options)

    # このへんもっといい実装方法ありそう
    log = scrolledtext.ScrolledText(
        master=window, width=20, height=10, bd=5, state='disabled')

    # 配置

    f_form_id.pack()
    f_form_pass.pack()

    f_button_kinmu.pack(pady=2)
    f_button_kyukei.pack(pady=2)

    log.pack()

    gyomu = TimeLine(log)

    window.mainloop()
