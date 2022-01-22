#!/bin/env python


import credential as cd
import timeline as tl
import win_design
import StateMachine
import kics_register
import vpn_control


def main():
    cd.CredentialController()

    kics_app_sm = StateMachine.SM_KICS()
    main_window = win_design.KicsAppWindow()

    menu = win_design.KicsAppMenuBar()
    main_window.configure(menu=menu)

    timeline = tl.KicsAppTimeline(kics_app_sm)
    setattr(kics_app_sm, 'timeline', timeline)

    frame = win_design.KicsAppFrame(kics_app_sm)
    setattr(kics_app_sm, 'frame', frame)

    kics = kics_register.KicsRegister(kics_app_sm)
    vpn = vpn_control.VPNConnector(kics_app_sm)

    main_window.register(frame)
    main_window.mainloop()


def show_registered_action(sm):
    print(vars(sm.common_action_list))


if __name__ == '__main__':
    main()
