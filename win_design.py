#!/bin/env python

import tkinter as tk
from tkinter import scrolledtext
import kics_register
import vpn_control
import timeline
import functools

import SM_constants


KINMU_START_ARGS = {
    'text': "勤務開始",
    'event_id': SM_constants.EVENT_VAR.KINMU_START_BUTTON_PUSHED,
    'button_state': ('activate', 'inactivate', 'inactivate'),
}

KINMU_END_ARGS = {
    'text': "勤務終了",
    'event_id': SM_constants.EVENT_VAR.KINMU_END_BUTTON_PUSHED,
    'button_state': ('inactivate', 'activate', 'inactivate'),
}

KYUKEI_START_ARGS = {
    'text': "休憩開始",
    'event_id': SM_constants.EVENT_VAR.KYUKEI_START_BUTTON_PUSHED,
    'button_state': ('inactivate', 'activate', 'inactivate'),
}

KYUKEI_END_ARGS = {
    'text': "休憩終了",
    'event_id': SM_constants.EVENT_VAR.KYUKEI_END_BUTTON_PUSHED,
    'button_state': ('inactivate', 'inactivate', 'activate'),
}


class ButtonElement():
    funcs_4_update = []
    funcs_4_set_click = []

    def __init__(
            self,
            text: str = '',
            event_id=None,
            button_state: tuple = (),
            *args):
        self.text = tk.StringVar()
        self.text.set(text)
        self.event_id = event_id
        self.state_list = button_state
        self.b_element = tk.Button(
            textvariable=self.text,
            font= ("MSゴシック", "15", "bold"),
            state=tk.NORMAL)

        ButtonElement.funcs_4_update.append(self.update_state)
        ButtonElement.funcs_4_set_click.append(self.set_click_func)
        self.initial_button_state(button_state[0])

    def activate(self):
        self.b_element.configure(
            state=tk.NORMAL,
            background="palegreen",
            activebackground="limegreen",
            relief=tk.RAISED,
            cursor="hand2",
            takefocus=True)

    def inactivate(self):
        self.b_element.configure(
            state=tk.DISABLED,
            background="gray",
            relief=tk.GROOVE,
            cursor="arrow",
            takefocus=False)

    def initial_button_state(self, initial_state):
        if initial_state == 'activate':
            self.activate()
        elif initial_state == 'inactivate':
            self.inactivate()

    def update_state(self, new_state:int):
        if self.state_list[new_state] == 'activate':
            self.activate()
        elif self.state_list[new_state] == 'inactivate':
            self.inactivate()

    def set_click_func(self, func):
        self.b_element.configure(command=functools.partial(func, self, self.event_id))

    @classmethod
    def update_buttons(cls, new_state):
        for b_func in cls.funcs_4_update:
            b_func(new_state)

    @classmethod
    def button_click_event_setting(cls, func):
        for b_func in cls.funcs_4_set_click:
            b_func(func)


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
        self.label = tk.Label(**label_dict, font=default_font)
        self.entry = tk.Entry(**entry_dict, font=default_font)
        self.label.pack(in_=self)
        self.entry.pack(in_=self)

    def get(self):
        return self.entry.get()

    def insert(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class TimeStampLogBox(scrolledtext.ScrolledText):
    def __init__(self):
        logbox_dict = {'width': 20, 'height': 10, 'bd': 5, 'state': 'disabled'}
        super().__init__(**logbox_dict)
        self.stamp_count = 1
        self.stamp_str = []

    def stamp(self, action_id: int):
        MSG_TABLE = ("勤務開始", "勤務終了", "休憩開始", "休憩終了")
        date = str(timeline.timelist[-1].month) + \
            '/' + str(timeline.timelist[-1].day)
        time = str(timeline.timelist[-1].hour).zfill(2) + ':' + \
            str(timeline.timelist[-1].minute).zfill(2)
        log_msg = date + ' ' + time + ' ' + \
            MSG_TABLE[action_id] + '\n'
        self.config(state='normal')
        self.insert(str(self.stamp_count) + '.0', log_msg)
        self.config(state='disable')
        self.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1


class TimeInfoFrame(tk.Frame):
    def __init__(self):
        super().__init__(width=200, bd=1, relief=tk.RAISED, background="skyblue")
        self.l_work_state_text = tk.StringVar()
        self.l_work_start_text = tk.StringVar()
        self.l_work_sum_text = tk.StringVar()

        self.l_work_state_text.set("勤務前")
        self.l_work_sum_text.set("勤務時間合計")

        self.l_work_state = tk.Label(
            textvariable=self.l_work_state_text, font=(
                "MSポップ", "20", "bold"), takefocus=False)
        self.l_work_start = tk.Label(font=("MSポップ", "10", "bold"))
        self.l_work_sum = tk.Label(
            textvariable=self.l_work_sum_text, font=(
                "MSポップ", "10", "bold"), takefocus=False)

        self.time_reset()

        self.l_work_state.pack(in_=self)
        self.l_work_start.pack(in_=self)
        self.l_work_sum.pack(in_=self)

    def state_update(self, action_id):
        MSG_TABLE = ("勤務中", "お疲れさまでした", "休憩中", "勤務中")
        self.l_work_state_text.set(MSG_TABLE[action_id])
        self.l_work_state.config(textvariable=self.l_work_state_text)

    def start_update(self, start_time):
        timeline.start_time_calc(start_time)
        self.l_work_start_text.set(
            "開始時刻 " +
            timeline.start_hour +
            ':' +
            timeline.start_min)
        self.l_work_start.config(textvariable=self.l_work_start_text)
        self.sum_update()

    def sum_update(self):
        try:
            timeline.sum_time_calc()
            self.l_work_sum_text.set(
                "勤務時間合計 " + timeline.sum_hour + "時間" + timeline.sum_min + "分")
            self.l_work_sum.config(textvariable=self.l_work_sum_text)

        except BaseException:
            pass
        finally:
            self.after_id = self.after(60000, self.sum_update)

    def time_reset(self):
        self.l_work_start_text.set("開始時刻 -- : --")
        self.l_work_start.config(textvariable=self.l_work_start_text)
        try:
            self.after_cancel(self.after_id)
        except BaseException:
            pass


def bind_sample(window, event, func):
    # bindsample
    event = "<Button-3>"
    window.bind(event, func)


class WindowSetting(tk.Tk):
    def __init__(self, *args):
        super().__init__()
        self.geometry('200x400')
        self.title('KICS AUTO')
        self.resizable(False, False)

        id_label_args = {'text': "DSC-ID"}
        self.f_form_id = InputFrame(label_dict=id_label_args, entry_dict={})

        pass_label_args = {'text': "Password"}
        self.f_form_pass = InputFrame(
            label_dict=pass_label_args,
            entry_dict={'show': "*"})

        self.f_button_kinmu = ButtonFrame(leftb_dict=KINMU_START_ARGS,
                                          rightb_dict=KINMU_END_ARGS)

        self.f_button_kyukei = ButtonFrame(leftb_dict=KYUKEI_START_ARGS,
                                           rightb_dict=KYUKEI_END_ARGS)

        self.logbox = TimeStampLogBox()

        self.statebox = TimeInfoFrame()
        # 配置

        self.statebox.pack(in_=self)
        self.f_form_id.pack(in_=self)
        self.f_form_pass.pack(in_=self)

        self.f_button_kinmu.pack(in_=self, pady=2)
        self.f_button_kyukei.pack(in_=self, pady=2)

        self.logbox.pack(in_=self)


if __name__ == '___main__':
    pass