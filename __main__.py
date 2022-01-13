#!/bin/env python

import timeline as tl
import win_design
import StateMachine
import kics_register
import vpn_control


def main():
    kics_app_sm = StateMachine.SM_KICS()
    root_window = win_design.KicsAppWindow()

    timeline = tl.KicsAppTimeline(kics_app_sm)
    setattr(kics_app_sm, 'timeline', timeline)

    frame = win_design.KicsAppFrame(kics_app_sm)
    setattr(kics_app_sm, 'frame', frame)

    kics = kics_register.KicsRegister(kics_app_sm)
    vpn = vpn_control.VPNConnector(kics_app_sm)

    root_window.register(frame)
    root_window.mainloop()


def show_registered_action(sm):
    print(vars(sm.common_action_list))


if __name__ == '__main__':
    main()
