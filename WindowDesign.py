#!/bin/env python

import tkinter as tk
import kics_register
import vpn_control
import TimeLine
import functools
from enum import Enum

import SMConstants


KINMU_START_ARGS = {
    'text': "勤務開始",
    'event_id': SMConstants.EVENT_VAR.KINMU_START_BUTTON_PUSHED,
    'button_state': ('activate', 'inactivate', 'inactivate'),
}

KINMU_END_ARGS = {
    'text': "勤務終了",
    'event_id': SMConstants.EVENT_VAR.KINMU_END_BUTTON_PUSHED,
    'button_state': ('inactivate', 'activate', 'inactivate'),
}

KYUKEI_START_ARGS = {
    'text': "休憩開始",
    'event_id': SMConstants.EVENT_VAR.KYUKEI_START_BUTTON_PUSHED,
    'button_state': ('inactivate', 'activate', 'inactivate'),
}

KYUKEI_END_ARGS = {
    'text': "休憩終了",
    'event_id': SMConstants.EVENT_VAR.KYUKEI_END_BUTTON_PUSHED,
    'button_state': ('inactivate', 'inactivate', 'activate'),
}

class ButtonElement():
    b_obj_list = []
    b_state_dict = {}

    def __init__(
            self,
            text: str = '',
            event_id = None,
            button_state: tuple = (),
            *args):
        self.text = tk.StringVar()
        self.text.set(text)
        self.event_id = event_id
        self.font = ("MSゴシック", "15", "bold")
        self.b_element = tk.Button(
            textvariable=self.text,
            font=self.font,
            state=tk.NORMAL)

        ButtonElement.b_obj_list.append({'id': id(self), 'obj': self})
        ButtonElement.b_state_dict[id(self)] = button_state

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

    @classmethod
    def update_button(cls, new_state:int):
        for b_tuple in cls.b_obj_list:
            if cls.b_state_dict[b_tuple['id']
                                ][new_state] == 'activate':
                b_tuple['obj'].activate()
            elif cls.b_state_dict[b_tuple['id']][new_state] == 'inactivate':
                b_tuple['obj'].inactivate()

    @classmethod
    def button_click_event_setting(cls, func):
        for b_tuple in cls.b_obj_list:
            b_tuple['obj'].b_element.configure(command=functools.partial(func, b_tuple['obj'], b_tuple['obj'].event_id))

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

        self.logbox = TimeLine.TimeStampLogBox()

        self.statebox = TimeLine.TimeInfoFrame()
        # 配置

        self.statebox.pack(in_=self)
        self.f_form_id.pack(in_=self)
        self.f_form_pass.pack(in_=self)

        self.f_button_kinmu.pack(in_=self, pady=2)
        self.f_button_kyukei.pack(in_=self, pady=2)

        self.logbox.pack(in_=self)

if __name__=='___main__':
    pass