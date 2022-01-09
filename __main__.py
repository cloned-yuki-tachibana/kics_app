#!/bin/env python

from tkinter.constants import FALSE, TRUE

import timeline
from tkinter import Tk, mainloop, messagebox

import win_design
import SM_constants


CONFIRM_MSG_TBL = ("在宅勤務を開始します。よろしいですか",
                   "在宅勤務を終了します。よろしいですか",
                   "休憩を開始し勤務を中断します（業務外）。 \
                    \nよろしいですか",
                   "在宅勤務を再開します。よろしいですか")


class StateMachine():
    state_var = SM_constants.INITIAL_STATE

    @classmethod
    def do_action(cls, obj, event_id: SM_constants.EVENT_VAR):
        global window
        cls.new_state = SM_constants.NEXT_STATE_TBL[event_id.value][cls.state_var.value]
        cls.action = SM_constants.ACTION_TBL[event_id.value][cls.state_var.value]

        ret = TRUE
        #msg = CONFIRM_MSG_TBL[EventManage.action.value]
        #ret = messagebox.askyesno(title="確認", message=msg, parent=window)
        if ret == TRUE:
            ACTION_FUNC_TBL[cls.action.value](obj, window)
            cls.state_var = cls.new_state

    @classmethod
    def act_common(cls, window: win_design.WindowSetting):
        win_design.ButtonElement.update_buttons(cls.new_state.value)
        timeline.push_time()
        window.statebox.state_update(action_id=cls.action.value)
        #window.logbox.stamp(action_id=cls.action.value)

    @classmethod
    def act_kinmu_start(cls, obj, window: win_design.WindowSetting):
        cls.act_common(window)
        window.statebox.start_update(timeline.timelist[0])
        # vpn_control.vpn_control("connect")

    @classmethod
    def act_kinmu_end(cls, obj, window: win_design.WindowSetting):
        cls.act_common(window)
        register = {'id': window.f_form_id.get(),
                    'password': window.f_form_pass.get()}
        # err = kics_register.KICS_acess(TimeLine.timelist, register)
        # vpn_control.vpn_control("disconnect")
        timeline.reset()
        window.statebox.time_reset()
        err = True
        if not err:
            error('kics_err')

    @classmethod
    def act_kyukei_start(cls, obj, window: win_design.WindowSetting):
        cls.act_common(window)
        # vpn_control.vpn_control("disconnect")

    @classmethod
    def act_kyukei_end(cls, obj, window: win_design.WindowSetting):
        cls.act_common(window)
        # vpn_control.vpn_control("connect")


def error(num: str):
    messagebox.showerror("error", "error occur" + num)
    exit(False)


ACTION_FUNC_TBL = (
    StateMachine.act_kinmu_start,
    StateMachine.act_kinmu_end,
    StateMachine.act_kyukei_start,
    StateMachine.act_kyukei_end
)


def main():
    global window
    window = win_design.WindowSetting()

    # event_setting
    win_design.ButtonElement.button_click_event_setting(StateMachine.do_action)

    window.mainloop()


if __name__ == '__main__':
    main()
