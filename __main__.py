#!/bin/env python

from tkinter.constants import FALSE, TRUE

import TimeLine
from tkinter import mainloop, messagebox

import WindowDesign
import SMConstants


CONFIRM_MSG_TBL = ("在宅勤務を開始します。よろしいですか",
                   "在宅勤務を終了します。よろしいですか",
                   "休憩を開始し勤務を中断します（業務外）。 \
                    \nよろしいですか",
                   "在宅勤務を再開します。よろしいですか")


state_var = SMConstants.STATE_VAR.KINMU_MAE


def do_action(obj, event_id: SMConstants.EVENT_VAR):
    global state_var
    global window
    new_state = SMConstants.NEXT_STATE_TBL[event_id.value][state_var.value]
    action = SMConstants.ACTION_TBL[event_id.value][state_var.value]
    # print("confirm")
    ret = TRUE
    #msg = CONFIRM_MSG_TBL[EventManage.action.value]
    #ret = messagebox.askyesno(title="確認", message=msg, parent=window)
    if ret == TRUE:
        WindowDesign.ButtonElement.update_button(new_state.value)
        TimeLine.get_time()
        window.logbox.stamp(action_id=action.value)
        if action == SMConstants.ACTION_VAR.KINMU_END:
            act_kinmu_end(window, obj)
        elif action == SMConstants.ACTION_VAR.KINMU_START:
            window.statebox.start_update(TimeLine.timelist[0])
        if state_var == SMConstants.STATE_VAR.KINMU_CHU:
            pass
            # vpn_control.vpn_control("disconnect")
        else:
            pass
            # vpn_control.vpn_control("connect")
        state_var = new_state


def act_kinmu_end(window:WindowDesign.WindowSetting, obj):
    register = {'id': window.f_form_id.get(),
                'password': window.f_form_pass.get()}
    # err = kics_register.KICS_acess(TimeLine.timelist, register)
    TimeLine.reset()
    window.statebox.time_reset()
    err = True
    if not err:
        error('kics_err')


def error(num):
    messagebox.showerror("error", "error occur" + num)
    exit(False)


if __name__ == '__main__':
    window = WindowDesign.WindowSetting()

    #event_setting
    WindowDesign.ButtonElement.button_click_event_setting(do_action)

    mainloop()
