#!/bin/env python

from enum import Enum

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

if __name__=="__main__":
    pass