#!/bin/env python

import keyring
import os

import win_design


class CredentialController():
    "singleton"
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        "シングルトンでもインスタンス化の度に呼ばれる"
        self.set_default_user()

    def set_default_user(self):
        try:
            with open('.key', 'r') as key:
                self.user = key.readline()

            print('get default user by .key')
        except BaseException:
            self.register_account()

    def register_account(self):
        self.window = win_design.CredentialWindow()

        self.user = self.window.user
        keyring.set_password('kics_' + self.user, self.user, self.window.password)
        delattr(self, 'window')

        with open('.key', 'w') as keylist:
            keylist.write(self.user)

    def get_password(self):
        return keyring.get_password('kics_' + self.user, self.user)

    def del_account(self):
        keyring.delete_password('kics_' + self.user, self.user)
        os.remove('.key')


def main():
    a = CredentialController()
    b = CredentialController()


if __name__ == '__main__':
    main()
