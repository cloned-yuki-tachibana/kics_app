#!/usr/bin/env python

import subprocess


def vpn_control(action):
    subprocess.run(['vpn_toggle.bat', action])


if __name__ == "__main__":
    vpn_control("connect")
