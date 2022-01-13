#!/usr/bin/env python

import subprocess

import StateMachine as SM


class VPNConnector():

    def __init__(self, sm: SM.StateMachine):
        self.register2sm(sm)

    def vpn_control(self, action):
        subprocess.run(['vpn_toggle.bat', action])

    def register2sm(self, sm: SM.StateMachine):
        sm.add_action_item(
            type(sm).ACTION_VAR.KINMU_START,
            self.act_vpn_connect,
            priority='+2')
        sm.add_action_item(
            type(sm).ACTION_VAR.KINMU_END,
            self.act_vpn_disconnect,
            priority='-2')
        sm.add_action_item(
            type(sm).ACTION_VAR.KYUKEI_START,
            self.act_vpn_disconnect, priority='-2')
        sm.add_action_item(
            type(sm).ACTION_VAR.KYUKEI_END,
            self.act_vpn_connect,
            priority='+2')

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
