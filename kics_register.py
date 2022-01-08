#!/usr/bin/env python

from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import datetime # for test
import time

import timeline


def KICS_acess(timelist: list, register: dict):

    timeline.get_kics_time()

    USER = register.get('id')
    PASSWORD = register.get('password')

    if USER is None or USER == '' or PASSWORD is None or PASSWORD == '':
        return (False, 'idかpassが入力されていません')

    options = EdgeOptions()
    options.use_chromium = True

    options.add_argument("--headless")
    with Edge(executable_path='C:\\WebDriver\\bin\\msedgedriver.exe') as driver:
        try:
            wait = WebDriverWait(driver=driver, timeout=30)
            kics_url = 'http://kics.jinji.denso.co.jp/siteminderagent/forms_ja-JP/login-kics.fcc?TYPE=33554433&REALMOID=06-0007e4b9-ceba-18d0-b029-0e0e0a06b0a4&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-HRqQr6ufcyxhIF0WsEzBihlJmLjJf14Q%2fr%2f7bkyx2DuLbqMW%2bF2WWjM%2fvtW%2bhiy1&TARGET=-SM-http%3a%2f%2fkics%2ejinji%2edenso%2eco%2ejp%2fa0tpkkics%2fapl%2fjsp%2fTop%2ejsp'
            driver.get(kics_url)

            js = 'document.Login.USER.value=\"' + USER + '\"; \
                document.Login.PASSWORD.value=\"' + PASSWORD + '\"; \
                submitForm();'

            driver.execute_script(js)
            wait.until(EC.presence_of_all_elements_located)

            handle_array = driver.window_handles
            driver.switch_to.window(handle_array[-1])

            js = ' appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartHour.value = "' + timeline.start_hour + '"; \
                appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartMin.value  = "' + timeline.start_min + '" ; \
                appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndHour.value   = "' + timeline.end_hour + '"; \
                appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndMin.value    = "' + timeline.end_min + '" ; \
                appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuHour.value      = "' + timeline.sum_hour + '"; \
                appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuMin.value       = "' + timeline.sum_min + '" ;'
            driver.execute_script(js)

            driver.execute_script('appFrame.ok_onClick();')
            wait.until(EC.presence_of_all_elements_located)

            time.sleep(3) # 画面の遷移待ち
            driver.execute_script(
                'appFrame.doAction("/KinmuTorokuKakuninEntry");')
            error = (True, '正常に登録できました')
        except BaseException:
            error = (False, '異常が発生し登録できませんでした')

        # input() #pause

    return error


def main():
    # for test
    timelist = []
    timelist.append(datetime.datetime(2022, 1, 2, 10, 11))
    timelist.append(datetime.datetime(2022, 1, 2, 12, 47))  # 2:36
    timelist.append(datetime.datetime(2022, 1, 2, 13, 30))
    timelist.append(datetime.datetime(2022, 1, 2, 15, 32))  # 2:02
    timelist.append(datetime.datetime(2022, 1, 2, 16, 58))
    timelist.append(datetime.datetime(2022, 1, 2, 19, 19))  # 2:21

    KICS_acess(timelist)


if __name__ == "__main__":
    main()
