#!/usr/bin/env python

import subprocess
import StateMachine as SM


class VPNConnector():

    def __init__(self, sm: SM.StateMachine):
        self.register2sm(sm)

    def vpn_control(self, action):
        subprocess.run(['vpn_toggle.bat', action])

    def register2sm(self, sm: SM.StateMachine):
        sm.add_act(type(sm).ACTION_VAR.KINMU_START, 5, self.act_vpn_connect)
        sm.add_act(type(sm).ACTION_VAR.KINMU_END, 5, self.act_vpn_disconnect)
        sm.add_act(
            type(sm).ACTION_VAR.KYUKEI_START,
            5,
            self.act_vpn_disconnect)
        sm.add_act(type(sm).ACTION_VAR.KYUKEI_END, 5, self.act_vpn_connect)

    def act_vpn_connect(self, *args, **kwargs):
        print('connect')
        return
        self.vpn_control("connect")

    def act_vpn_disconnect(self, *args, **kwargs):
        print('disconnect')
        return
        self.vpn_control("disconnect")


if __name__ == "__main__":
    vpn = VPNConnector()
    vpn.vpn_control("connect")
