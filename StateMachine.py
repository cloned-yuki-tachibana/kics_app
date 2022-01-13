#!/bin/env python

from abc import ABCMeta
from distutils.log import debug
from enum import Enum, auto


class StateMachine(metaclass=ABCMeta):
    class STATE_VAR(Enum):
        pass

    class ACTION_VAR(Enum):
        pass

    class EVENT_VAR(Enum):
        pass

    def __init__(self, initial_state, priority_steps=2):
        self.state_var = initial_state
        self.new_state = None
        self.action = None
        self.NEXT_STATE_TBL = list()
        self.ACTION_TBL = list()
        self.common_func = list()
        self.priority_step_total = (priority_steps * 2) + 1
        self.make_action_dict()

    def debug(self):
        print("event = " + self.event_id.name + str(self.event_id.value))
        print("state = " + self.state_var.name + str(self.state_var.value))
        print("action= " + self.action.name + str(self.action.value))
        print("new_s = " + self.new_state.name + str(self.new_state.value))

    def debug_action_dump(self):
        print('common')
        print(self.common_action_list)

        for action in type(self).ACTION_VAR:
            print(action.name)
            for elem in self.action_dict[action.name]:
                print(elem)

    def do_action(self, event_id: EVENT_VAR, *args, **kwargs):
        self.new_state = self.NEXT_STATE_TBL[event_id.value][self.state_var.value]
        self.action = self.ACTION_TBL[event_id.value][self.state_var.value]
        self.event_id = event_id

        self.act_common(self, event_id, *args, **kwargs)

        for priority_step in range(self.priority_step_total):
            for step in range(
                    len(self.action_dict[self.action.name][priority_step])):
                self.action_dict[self.action.name][priority_step][step](
                    self, event_id, *args, **kwargs)
        self.update_state()

    def update_state(self):
        self.state_var = self.new_state

    def make_action_dict(self):
        self.action_dict = dict()
        for action in type(self).ACTION_VAR:
            self.action_dict[action.name] = list()
            for _ in range(self.priority_step_total):
                self.action_dict[action.name].append(list())
        self.common_action_list = list()

    def act_common(self, sm, event_id, *args, **kwargs):
        for step in range(len(self.common_action_list)):
            self.common_action_list[step](sm, event_id, *args, **kwargs)

    def add_common_action_item(self, func, pos=-1):
        self.common_action_list.insert(pos, func)

    def add_action_item(self, action: ACTION_VAR, func, priority=None):
        priority_ave = self.priority_step_total // 2

        if priority is None:
            priority_num = priority_ave

        elif isinstance(priority, int):
            if priority >= self.priority_step_total:
                priority_num = -1
            elif priority <= (-1 * self.priority_step_total):
                priority_num = 0
            else:
                priority_num = priority

        elif isinstance(priority, str):
            if int(priority) >= self.priority_step_total:
                priority_num = -1
            elif int(priority) < (-1 * priority_ave):
                priority_num = 0
            else:
                priority_num = (priority_ave - int(priority))

        self.action_dict[action.name][priority_num].append(func)


class SM_KICS(StateMachine):
    class STATE_VAR(Enum):
        KINMU_MAE = 0
        KINMU_CHU = auto()
        KYUKEI_CHU = auto()
        STATE_TOTAL = None

    class ACTION_VAR(Enum):
        KINMU_START = 0
        KINMU_END = auto()
        KYUKEI_START = auto()
        KYUKEI_END = auto()
        ACTION_TOTAL = None

    class EVENT_VAR(Enum):
        KINMU_START_BUTTON_PUSHED = 0
        KINMU_END_BUTTON_PUSHED = auto()
        KYUKEI_START_BUTTON_PUSHED = auto()
        KYUKEI_END_BUTTON_PUSHED = auto()
        EVENT_TOTAL = None

    def __init__(self):
        super().__init__(type(self).STATE_VAR.KINMU_MAE)
        self.window_width = 0
        self.window_height = 0
        self.NEXT_STATE_TBL = (
            (type(self).STATE_VAR.KINMU_CHU,
             type(self).STATE_VAR.STATE_TOTAL,
             type(self).STATE_VAR.STATE_TOTAL),
            (type(self).STATE_VAR.STATE_TOTAL,
             type(self).STATE_VAR.KINMU_MAE,
             type(self).STATE_VAR.STATE_TOTAL),
            (type(self).STATE_VAR.STATE_TOTAL,
             type(self).STATE_VAR.KYUKEI_CHU,
             type(self).STATE_VAR.STATE_TOTAL),
            (type(self).STATE_VAR.STATE_TOTAL,
             type(self).STATE_VAR.STATE_TOTAL,
             type(self).STATE_VAR.KINMU_CHU))

        self.ACTION_TBL = (
            (type(self).ACTION_VAR.KINMU_START,
             type(self).ACTION_VAR.ACTION_TOTAL,
             type(self).ACTION_VAR.ACTION_TOTAL),
            (type(self).ACTION_VAR.ACTION_TOTAL,
             type(self).ACTION_VAR.KINMU_END,
             type(self).ACTION_VAR.ACTION_TOTAL),
            (type(self).ACTION_VAR.ACTION_TOTAL,
             type(self).ACTION_VAR.KYUKEI_START,
             type(self).ACTION_VAR.ACTION_TOTAL),
            (type(self).ACTION_VAR.ACTION_TOTAL,
             type(self).ACTION_VAR.ACTION_TOTAL,
             type(self).ACTION_VAR.KYUKEI_END))


def test():
    test = SM_KICS()

    def test_action(sm, event_id, *args, **kwargs):
        print(vars(sm))
        print(vars(event_id))
        if sm == event_id:
            print('error')

    # print(vars(test))
    test.add_common_action_item(test_action)

    test.do_action(type(test).EVENT_VAR.KINMU_START_BUTTON_PUSHED)
    #test.do_action(None, type(test).EVENT_VAR.KINMU_END_BUTTON_PUSHED)
    #test.do_action(None, type(test).EVENT_VAR.KINMU_START_BUTTON_PUSHED)
    #test.do_action(None, type(test).EVENT_VAR.KYUKEI_START_BUTTON_PUSHED)
    #test.do_action(None, type(test).EVENT_VAR.KYUKEI_END_BUTTON_PUSHED)


def main():
    test = SM_KICS()
    # print(SM_KICS.ACTION_VAR.common)
    print(int('-1'))


if __name__ == "__main__":
    main()
