#!/bin/env python

from enum import Enum
import tkinter as tk
from tkinter import Event, messagebox
from tkinter import font
from tkinter.constants import DISABLED, FALSE, TRUE


import kics_register
import vpn_control
import TimeLine


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

    @classmethod
    def do_action(cls, obj, event_id: EVENT_VAR):
        cls.new_state = NEXT_STATE_TBL[event_id.value][cls.state_var.value]
        cls.action = ACTION_TBL[event_id.value][cls.state_var.value]
        # print("confirm")
        ret = TRUE
        #msg = CONFIRM_MSG_TBL[EventManage.action.value]
        #ret = messagebox.askyesno(title="確認", message=msg, parent=window)
        if ret == TRUE:
            ButtonElement.update_button()
            TimeLine.get_time()
            logbox.stamp(action_id=cls.action.value)
            if cls.action == ACTION_VAR.KINMU_END:
                act_kinmu_end(obj)

            elif cls.action == ACTION_VAR.KINMU_START:
                statebox.start_update(TimeLine.timelist[0])

            if cls.state_var==STATE_VAR.KINMU_CHU:
                pass
                # vpn_control.vpn_control("disconnect")
            else :
                pass
                # vpn_control.vpn_control("connect")

            cls.state_var = cls.new_state


class ButtonElement():
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
            state=tk.NORMAL)

        ButtonElement.b_obj_list.append({'id': id(self), 'obj': self})
        ButtonElement.b_state_dict[id(self)] = button_state

        self.initial_button_state(button_state[0])

    def click(self):
        EventManage.do_action(self, self.event_id)

    def activate(self):
        self.b_element.config(
            state=tk.NORMAL,
            background="palegreen",
            activebackground="limegreen",
            relief=tk.RAISED,
            cursor="hand2")

    def inactivate(self):
        self.b_element.config(
            state=tk.DISABLED,
            background="gray",
            relief=tk.GROOVE,
            cursor="arrow")

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


class InputFrame(tk.Frame):
    def __init__(self, label_dict: dict, entry_dict: dict):
        super().__init__()
        default_font = ("MSゴシック", "10", "bold")
        self.label = tk.Label(**label_dict, font=default_font, takefocus=True)
        self.entry = tk.Entry(**entry_dict, font=default_font, takefocus=True)
        self.label.pack(in_=self)
        self.entry.pack(in_=self)

    def get(self):
        return self.entry.get()

    def insert(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


def error(num):
    messagebox.showerror("error", "error occur" + num)
    exit(False)


def act_kinmu_end(obj):
    register = {'id': f_form_id.get(), 'password': f_form_pass.get()}
    # err = kics_register.KICS_acess(TimeLine.timelist, register)
    TimeLine.reset()
    statebox.time_reset()
    err = True
    if not err:
        error('kics_err')


if __name__ == "__main__":
    # ウィンドウ設定
    window = tk.Tk()
    window.geometry('200x400')
    window.title('KICS AUTO')
    window.resizable(False, False)



    id_label_args = {'text': "DSC-ID"}
    f_form_id = InputFrame(label_dict=id_label_args, entry_dict={})

    pass_label_args = {'text': "Password"}
    f_form_pass = InputFrame(
        label_dict=pass_label_args,
        entry_dict={'show': "*"})

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

    logbox = TimeLine.TimeStampLogBox()

    statebox = TimeLine.TimeInfoFrame()
    # 配置

    statebox.pack(in_=window)
    f_form_id.pack(in_=window)
    f_form_pass.pack(in_=window)

    f_button_kinmu.pack(in_=window, pady=2)
    f_button_kyukei.pack(in_=window, pady=2)

    logbox.pack(in_=window)

    window.mainloop()
