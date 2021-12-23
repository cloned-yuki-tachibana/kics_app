#!/bin/env python
import datetime
from enum import Enum
from time import time
import tkinter as tk
from   tkinter import messagebox
from   tkinter.constants import DISABLED, FALSE, TRUE
import importlib

import kics_register

class STATE_VAR(Enum):
    KINMU_MAE=0
    KINMU_CHU=1
    KYUKEI_CHU=2
    STATE_TOTAL=3 #dummy

class ACTION_VAR(Enum):
    KINMU_START=0
    KINMU_END=1
    KINMU_RESTART=2
    KYUKEI_START=3
    ACTION_TOAL=4 #dumy

class BUTTON_NUM(Enum):
    KINMU_BUTTON=0
    KYUKEI_BUTTON=1

NEXT_STATE_TBL = [[STATE_VAR.KINMU_CHU,   STATE_VAR.KINMU_MAE,  STATE_VAR.KINMU_CHU],
                  [STATE_VAR.STATE_TOTAL, STATE_VAR.KYUKEI_CHU, STATE_VAR.STATE_TOTAL ]]

ACTION_TBL =     [[ACTION_VAR.KINMU_START, ACTION_VAR.KINMU_END,    ACTION_VAR.KINMU_RESTART  ],
                  [ACTION_VAR.ACTION_TOAL, ACTION_VAR.KYUKEI_START, ACTION_VAR.ACTION_TOAL]]

BUTTON_TBL = [["勤務開始",  "勤務終了", "勤務再開"],
              [tk.DISABLED ,tk.NORMAL, tk.DISABLED]]

CONFIRM_MSG_TBL = ["在宅勤務を開始します。よろしいですか",
                   "在宅勤務を終了します。よろしいですか",
                   "在宅勤務を再開します。よろしいですか",
                   "休憩を開始し勤務を中断します（業務外）。 \
                    \nよろしいですか"]

class TimeLine():
    def __init__(self):
        self.timelist = []
    def get_time(self):
        self.timelist.append(datetime.datetime.now())
    def time_calc(self):
        self.work_end_hour = self.timelist[-1].hour
        self.work_end_minute = self.timelist[-1].minute
        self.work_time_sum = datetime.timedelta()
        for i in range(1,len(self.timelist),2):
            self.work_time_sum += (self.timelist[i] - self.timelist[i-1])

        self.work_time_sum_hour = self.work_time_sum // datetime.timedelta(hours=1)
        self.work_time_sum_minute = self.work_time_sum.seconds % datetime.timedelta(hours=1).seconds // 60
        self.timelist.clear()

class ButonElement():
    def __init__(self, text, b_id:BUTTON_NUM, frame,state=tk.NORMAL):
        self.text = tk.StringVar(frame)
        self.text.set(text)
        self.b_id = b_id
        self.font = ("MSゴシック", "20", "bold")
        self.b_element = tk.Button(frame, textvariable=self.text, font=self.font, command=self.click, state=state)
        self.b_element.pack()
    def click(self):
        self.new_state = NEXT_STATE_TBL[self.b_id.value][state_var.value]
        self.action    = ACTION_TBL[self.b_id.value][state_var.value]
        do_action(self)

def do_action(obj:ButonElement):
    #print("confirm")
    ret = TRUE
    #msg = CONFIRM_MSG_TBL[obj.action.value]
    #ret = messagebox.askyesno("確認",msg)
    if ret == TRUE:
        vpn_control(obj)
        gyomu.get_time()
        update_button(obj)
        if obj.action == ACTION_VAR.KINMU_END:
            act_kinmu_end(obj)
        elif obj.action == ACTION_VAR.KINMU_START:
            gyomu.work_start_hour = gyomu.timelist[0].hour
            gyomu.work_start_minute = gyomu.timelist[0].minute
            print("a")

        global state_var
        state_var = obj.new_state

def error(num):
    messagebox.showerror("error","error occur"+num)
    exit(False)

def act_kinmu_end(obj):
    gyomu.time_calc()
    print("kinmu shuryo sequence")

def vpn_control(obj:ButonElement):
    if state_var==STATE_VAR.KINMU_CHU:
        print("VPN disconnet")
    else :
        print("VPN connect")

def update_button(obj:ButonElement):
    global b1,b2
    b1.text.set(BUTTON_TBL[BUTTON_NUM.KINMU_BUTTON.value][obj.new_state.value])
    b2.b_element.config(state=BUTTON_TBL[BUTTON_NUM.KYUKEI_BUTTON.value][obj.new_state.value])

if __name__=="__main__":
    # initial state
    state_var = STATE_VAR.KINMU_MAE

    gyomu = TimeLine()

    #ウィンドウ設定
    frame = tk.Tk()
    frame.geometry('150x250')
    frame.title('サンプル画面')
    frame.resizable(False,False)

    b1 = ButonElement("勤務開始",b_id=BUTTON_NUM.KINMU_BUTTON,frame=frame)
    b2 = ButonElement("休憩開始",b_id=BUTTON_NUM.KYUKEI_BUTTON,state=tk.DISABLED,frame=frame)

    frame.mainloop()
