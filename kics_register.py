#!/usr/bin/env python
from tkinter.constants import TRUE
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import datetime
import time


class KINMU_JOHO():
    def __init__(self, timelist):
        self.time_calc(timelist)
        self.USER = ""
        self.PASSWORD = ""

    def time_calc(self, timelist):
        work_time_sum = datetime.timedelta()
        for i in range(0, len(timelist), 2):
            work_time_sum += (timelist[i + 1] - timelist[i])
        work_time_sum_hour = work_time_sum // datetime.timedelta(hours=1)
        work_time_sum_minute = work_time_sum.seconds % datetime.timedelta(
            hours=1).seconds // 60

        self.S_hour = str(timelist[0].hour).zfill(2)
        self.S_min = str(timelist[0].minute).zfill(2)
        self.E_hour = str(timelist[-1].hour).zfill(2)
        self.E_min = str(timelist[-1].minute).zfill(2)
        self.G_hour = str(work_time_sum_hour).zfill(2)
        if work_time_sum_minute >= 45:
            self.G_min = "45"
        elif work_time_sum_minute >= 30:
            self.G_min = "30"
        elif work_time_sum_minute >= 15:
            self.G_min = "15"
        else:
            self.G_min = "00"


def KICS_acess(timelist, user, password):

    kics_info = KINMU_JOHO(timelist)
    kics_info.USER = user
    kics_info.PASSWORD = password

    options = EdgeOptions()
    options.use_chromium = True

    options.add_argument("--headless")
    with Edge(executable_path='C:\\WebDriver\\bin\\msedgedriver.exe') as driver:
        wait = WebDriverWait(driver=driver, timeout=30)
        kics_url = 'http://kics.jinji.denso.co.jp/siteminderagent/forms_ja-JP/login-kics.fcc?TYPE=33554433&REALMOID=06-0007e4b9-ceba-18d0-b029-0e0e0a06b0a4&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-HRqQr6ufcyxhIF0WsEzBihlJmLjJf14Q%2fr%2f7bkyx2DuLbqMW%2bF2WWjM%2fvtW%2bhiy1&TARGET=-SM-http%3a%2f%2fkics%2ejinji%2edenso%2eco%2ejp%2fa0tpkkics%2fapl%2fjsp%2fTop%2ejsp'
        driver.get(kics_url)

        js = 'document.Login.USER.value=\"' + kics_info.USER + '\"; \
              document.Login.PASSWORD.value=\"' + kics_info.PASSWORD + '\"; \
              submitForm();'

        driver.execute_script(js)
        wait.until(EC.presence_of_all_elements_located)

        handle_array = driver.window_handles
        driver.switch_to.window(handle_array[-1])

        js = ' appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartHour.value = "' + kics_info.S_hour + '"; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartMin.value  = "' + kics_info.S_min + '" ; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndHour.value   = "' + kics_info.E_hour + '"; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndMin.value    = "' + kics_info.E_min + '" ; \
               appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuHour.value      = "' + kics_info.G_hour + '"; \
               appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuMin.value       = "' + kics_info.G_min + '" ;'
        driver.execute_script(js)

        driver.execute_script('appFrame.ok_onClick();')
        wait.until(EC.presence_of_all_elements_located)
        time.sleep(3)
        driver.execute_script('appFrame.doAction("/KinmuTorokuKakuninEntry");')

        # input() #pause

    #todo : 確認
    # todo : if ちゃんと勤務登録できている
    error = TRUE

    return error


def main():
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
