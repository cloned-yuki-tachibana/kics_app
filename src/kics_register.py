#!/usr/bin/env python
from tkinter.constants import TRUE
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import time

class KINMU_JOHO():
    def __init__(self):
        self.USER     = ""
        self.PASSWORD = ""
        self.S_hour   = ""
        self.S_min    = ""
        self.E_hour   = ""
        self.E_min    = ""
        self.G_hour   = ""
        self.G_min    = ""

def KICK_acess(obj:KINMU_JOHO):
    options = EdgeOptions()
    options.use_chromium = True

    options.add_argument("--headless")
    with Edge(executable_path='C:\\WebDriver\\bin\\msedgedriver.exe') as driver:
        wait = WebDriverWait(driver=driver, timeout=30)
        driver.get('http://kics.jinji.denso.co.jp/siteminderagent/forms_ja-JP/login-kics.fcc?TYPE=33554433&REALMOID=06-0007e4b9-ceba-18d0-b029-0e0e0a06b0a4&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-HRqQr6ufcyxhIF0WsEzBihlJmLjJf14Q%2fr%2f7bkyx2DuLbqMW%2bF2WWjM%2fvtW%2bhiy1&TARGET=-SM-http%3a%2f%2fkics%2ejinji%2edenso%2eco%2ejp%2fa0tpkkics%2fapl%2fjsp%2fTop%2ejsp')

        js = 'document.Login.USER.value=\"'+obj.USER+'\"; \
              document.Login.PASSWORD.value=\"'+obj.PASSWORD+'\"; \
              submitForm();'

        driver.execute_script(js)
        wait.until(EC.presence_of_all_elements_located)

        handle_array = driver.window_handles
        driver.switch_to.window(handle_array[1])

        js = ' appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartHour.value = "'+obj.S_hour+'"; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuStartMin.value  = "'+obj.S_min+'" ; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndHour.value   = "'+obj.E_hour+'"; \
               appFrame.document.KinmuTorokuActionForm.workZaitakuKinmuEndMin.value    = "'+obj.E_min+'" ; \
               appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuHour.value      = "'+obj.G_hour+'"; \
               appFrame.document.KinmuTorokuActionForm.gyouZaitakuKinmuMin.value       = "'+obj.G_min+'" ;'
        driver.execute_script(js)

        driver.execute_script('appFrame.ok_onClick();')
        wait.until(EC.presence_of_all_elements_located)
        time.sleep(3)
        driver.execute_script('appFrame.doAction("/KinmuTorokuKakuninEntry");')

    #確認
    #if ちゃんと勤務登録できている
    error = TRUE

    return error

def main():
    obj = KINMU_JOHO()

    obj.USER     = ""
    obj.PASSWORD = ""

    obj.S_hour= "10"
    obj.S_min = "00"
    obj.E_hour= "20"
    obj.E_min = "00"
    obj.G_hour= "07"
    obj.G_min = "30"

    KICK_acess(obj)

if __name__ == "__main__":
    main()

#js = 'return document'
#
#driver.execute_script(js)
