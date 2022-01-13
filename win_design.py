#!/bin/env python

import tkinter as tk
from tkinter import scrolledtext
import functools

import timeline as tl
import StateMachine as SM


class KicsAppButton(tk.Button):
    def __init__(self, sm: SM.StateMachine,
                 text='', event_id=None, state_list=()):
        self.text = tk.StringVar(value=text)
        self.event_id = event_id
        self.state_list = state_list
        super().__init__(
            textvariable=self.text,
            font=(
                "MSゴシック",
                "15",
                "bold"),
            command=functools.partial(sm.do_action, self.event_id),
            state=tk.NORMAL)

        self.set_initial_state()
        self.register2sm(sm)

    def set_initial_state(self):
        self.update_state(self.state_list[0])

    def update_state(self, state):
        if state == 'activate':
            self.activate()
        elif state == 'inactivate':
            self.inactivate()

    def activate(self):
        self.configure(
            state=tk.NORMAL,
            background="palegreen",
            activebackground="limegreen",
            relief=tk.RAISED,
            cursor="hand2",
            takefocus=True)

    def inactivate(self):
        self.configure(
            state=tk.DISABLED,
            background="gray",
            relief=tk.GROOVE,
            cursor="arrow",
            takefocus=False)

    def register2sm(self, sm: SM.StateMachine):
        sm.add_common_action_item(self.act_update_state)

    def act_update_state(
            self,
            sm: SM.StateMachine,
            event_id: int,
            *args,
            **kwargs):
        self.update_state(self.state_list[sm.new_state.value])


class TwoButtonFrame(tk.Frame):
    def __init__(
            self,
            button_class,
            sm: SM.StateMachine,
            leftb_dict: dict,
            rightb_dict: dict,
            **frame_dict):
        super().__init__(**frame_dict)
        self.left_button: tk.Button = button_class(sm=sm, **leftb_dict)
        self.right_button: tk.Button = button_class(sm=sm, **rightb_dict)

        self.left_button.pack_configure(in_=self, side=tk.LEFT)
        self.right_button.pack_configure(in_=self, side=tk.RIGHT)


class FourButtonFrame(tk.Frame):
    # not yet
    pass


class InputFrame(tk.Frame):
    def __init__(self, label_dict: dict, entry_dict: dict, **frame_dict):
        super().__init__()
        default_font = ("MSゴシック", "10", "bold")
        if 'font' in label_dict:
            label_dict['font'] = default_font
        if 'font' in entry_dict:
            entry_dict['font'] = default_font
        self.label = tk.Label(**label_dict)
        self.entry = tk.Entry(**entry_dict)
        self.label.pack(in_=self)
        self.entry.pack(in_=self)

    def get(self):
        return self.entry.get()

    def insert(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class LogBox(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs, state=tk.DISABLED)
        self.stamp_count = 1

    def stamp(self, msg):
        now = tl.nichiji.now('all')
        log_msg = now.date + ' ' + now.jikan + ' ' + msg + '\n'
        self.configure(state=tk.NORMAL)
        self.insert(str(self.stamp_count) + '.0', log_msg)
        self.configure(state='disable')
        self.see(str(self.stamp_count) + '.0')
        self.stamp_count += 1

    def clear(self):
        self.delete('0', tk.END)
        self.stamp_count = 1


class KicsAppTimeStampLogBox(LogBox):
    def __init__(self, sm: SM.StateMachine):
        super().__init__(width=20, height=10, bd=10)
        self.register2sm(sm)

    def register2sm(self, sm: SM.StateMachine):
        sm.add_common_action_item(self.act_stamp)

    def act_stamp(self, sm: SM.StateMachine, event_id, *args, **kwargs):
        MSG_TABLE = ("勤務開始", "勤務終了", "休憩開始", "休憩終了")
        super().stamp(MSG_TABLE[sm.action.value])


class KicsAppTimeInfoFrame(tk.Frame):
    def __init__(self, sm, *args, **kwargs):
        bg = "powderblue"
        super().__init__(width=200, bd=1, relief=tk.RAISED, background=bg, *args, **kwargs)
        self.l_work_state_text = tk.StringVar(value="勤務前")
        self.l_work_start_text = tk.StringVar(value="開始時刻 -- : -- ")
        self.l_work_sum_text = tk.StringVar(value="勤務時間合計 00時間00分")

        self.l_work_state = tk.Label(
            textvariable=self.l_work_state_text, font=(
                "MSポップ", "20", "bold"), takefocus=False, bg=bg)
        self.l_work_start = tk.Label(
            textvariable=self.l_work_start_text, font=(
                "MSポップ", "10", "bold"), takefocus=False, bg=bg)
        self.l_work_sum = tk.Label(
            textvariable=self.l_work_sum_text, font=(
                "MSポップ", "10", "bold"), takefocus=False, bg=bg)

        self.l_work_state.pack_configure(in_=self)
        self.l_work_start.pack_configure(in_=self)
        self.l_work_sum.pack_configure(in_=self)

        self.register2sm(sm)

    def sum_update(self, timelist: tl.KicsAppTimeline):
        sum_time = timelist.get_kinmu_sum()
        self.l_work_sum_text.set(
            "勤務時間合計 " +
            sum_time.hour +
            "時間" +
            sum_time.minute +
            "分")
        # update every minute
        self.after_id = self.after(60000, self.sum_update, timelist)

    def register2sm(self, sm: SM.StateMachine):
        sm.add_common_action_item(self.act_state_update)

        sm.add_action_item(
            type(sm).ACTION_VAR.KINMU_START,
            self.act_start_update)
        sm.add_action_item(
            type(sm).ACTION_VAR.KINMU_END,
            self.act_time_reset,
            priority='-2')

    def act_state_update(
            self,
            sm: SM.StateMachine,
            event_id: int,
            *args,
            **kwargs):
        MSG_TABLE = ("勤務中", "お疲れ", "休憩中", "勤務中")

        self.l_work_state_text.set(MSG_TABLE[sm.action.value])

    def act_start_update(
            self,
            sm: SM.StateMachine,
            event_id: int,
            *args,
            **kwargs):
        now = tl.nichiji.now('all')
        self.l_work_start_text.set("開始時刻 " + now.jikan)
        self.sum_update(sm.timeline)

    def act_time_reset(
            self,
            sm: SM.StateMachine,
            event_id: int,
            *args,
            **kwargs):
        self.l_work_start_text.set("開始時刻 -- : -- ")
        try:
            self.after_cancel(self.after_id)
        except BaseException:
            pass


class KicsAppFrame(tk.Frame):
    def __init__(self, sm: SM.StateMachine):
        super().__init__()

        id_label_args = {'text': "DSC-ID"}
        self.f_form_id = InputFrame(label_dict=id_label_args, entry_dict={})

        pass_label_args = {'text': "Password"}
        self.f_form_pass = InputFrame(
            label_dict=pass_label_args,
            entry_dict={'show': "*"})

        KINMU_START_ARGS = {
            'text': "勤務開始",
            'event_id': type(sm).EVENT_VAR.KINMU_START_BUTTON_PUSHED,
            'state_list': ('activate', 'inactivate', 'inactivate'),
        }

        KINMU_END_ARGS = {
            'text': "勤務終了",
            'event_id': type(sm).EVENT_VAR.KINMU_END_BUTTON_PUSHED,
            'state_list': ('inactivate', 'activate', 'inactivate'),
        }

        self.f_button_kinmu = TwoButtonFrame(button_class=KicsAppButton,
                                             sm=sm,
                                             leftb_dict=KINMU_START_ARGS,
                                             rightb_dict=KINMU_END_ARGS)

        KYUKEI_START_ARGS = {
            'text': "休憩開始",
            'event_id': type(sm).EVENT_VAR.KYUKEI_START_BUTTON_PUSHED,
            'state_list': ('inactivate', 'activate', 'inactivate'),
        }

        KYUKEI_END_ARGS = {
            'text': "休憩終了",
            'event_id': type(sm).EVENT_VAR.KYUKEI_END_BUTTON_PUSHED,
            'state_list': ('inactivate', 'inactivate', 'activate'),
        }

        self.f_button_kyukei = TwoButtonFrame(button_class=KicsAppButton,
                                              sm=sm,
                                              leftb_dict=KYUKEI_START_ARGS,
                                              rightb_dict=KYUKEI_END_ARGS)

        self.statebox = KicsAppTimeInfoFrame(sm=sm)
        self.logbox = KicsAppTimeStampLogBox(sm=sm)

        # 配置
        self.statebox.pack_configure(in_=self)
        self.f_form_id.pack_configure(in_=self)
        self.f_form_pass.pack_configure(in_=self)
        self.f_button_kinmu.pack_configure(in_=self, pady=(10, 0))
        self.f_button_kyukei.pack_configure(in_=self, pady=2)
        self.logbox.pack_configure(in_=self)


class KicsAppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KICS AUTO')
        self.resizable(False, False)

    def register(self, widget):
        widget.pack_configure(in_=self)

    def resize(self, width=200, height=400):
        format = str(width) + 'x' + str(height)
        self.geometry(format)


def main():
    class test_class():
        def __init__(self):
            self.name = "test"

    def test_Factory(cls):
        test1 = cls()
        print(test1.name)
        return test1

    def bind_sample(window, event, func):
        # bindsample
        event = "<Button-3>"
        window.bind(event, func)

    test = test_Factory(test_class)
    print(test.name)


if __name__ == '__main__':
    main()
