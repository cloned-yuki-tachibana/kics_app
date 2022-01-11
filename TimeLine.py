#!/bin/env python

import datetime as dt
import StateMachine as SM


class empty:
    pass


class nichiji(dt.datetime):
    @classmethod
    def now(cls, command=None):
        _datetime = super().now()

        return_datetime = empty()
        setattr(return_datetime, 'hour', str(_datetime.hour).zfill(2))
        setattr(return_datetime, 'minute', str(_datetime.minute).zfill(2))
        if command == 'all':
            setattr(
                return_datetime,
                'jikan',
                return_datetime.hour +
                ":" +
                return_datetime.minute)
            setattr(
                return_datetime, 'month', str(
                    _datetime.month).rjust(
                    2, ' '))
            setattr(return_datetime, 'day', str(_datetime.day).zfill(2))
            return_datetime.date = return_datetime.month + '/' + return_datetime.day
        return return_datetime


class KicsAppTimeline(list):
    def __init__(self, sm):
        list.__init__(self)
        self.start_hour = str()
        self.start_min = str()
        self.end_hour = str()
        self.end_min = str()
        self.sum_hour = str()
        self.sum_min = str()

        self.register2sm(sm)

    def get_kics_time(self):
        def round_kinmu_min(self):
            if int(self.sum_min) >= 45:
                self.sum_min = "45"
            elif int(self.sum_min) >= 30:
                self.sum_min = "30"
            elif int(self.sum_min) >= 15:
                self.sum_min = "15"
            else:
                self.sum_min = "00"
        self.calc_end_time()
        self.calc_kinmu_sum()
        round_kinmu_min(self)

    def calc_start_time(self):
        self.start_hour = self[0].hour
        self.start_min = self[0].minute

    def calc_end_time(self):
        print("len=" + str(len(self)))
        for elem in self:
            print(vars(elem))
        self.end_hour = self[-1].hour
        self.end_min = self[-1].minute

    def get_kinmu_sum(self):
        self.calc_kinmu_sum
        return_obj = empty()
        setattr(return_obj, 'hour', self.sum_hour)
        setattr(return_obj, 'minute', self.sum_min)
        return return_obj

    def calc_kinmu_sum(self):
        def kinmu_time(self: list):
            work_time_sum = 0
            for i in range(0, len(self), 2):
                work_time_sum += (int(self[i + 1].hour) - int(self[i].hour)) * 60 + (
                    int(self[i + 1].minute) - int(self[i].minute))

                self.sum_hour = str(work_time_sum // 60).zfill(2)
                self.sum_min = str(work_time_sum % 60).zfill(2)

        if len(self) % 2 == 0:  # 休憩中 or 勤務終了
            kinmu_time(self)
        else:  # 勤務中
            self.append(dt.datetime.now())
            kinmu_time(self)
            self.pop()

    def register2sm(self, sm: SM.StateMachine):
        sm.add_common_act(self.act_push)
        sm.add_act(type(sm).ACTION_VAR.KINMU_END, 5, self.act_clear)

    def act_push(self, *args, **kwargs):
        self.append(nichiji.now())

    def act_clear(self, *args, **kwargs):
        self.clear()


def test():
    pass


if __name__ == "__main__":
    test()
