from appium import webdriver
from Functions import *

desired_cap_SIA = {
    "udid": "44aa7006",
    "platformName": "Android",
    "appPackage": "com.sia.siasc",
    "noReset": 'true',
    "appActivity": "crc642d6d50fcf88c9f72.SplashActivity",
    "automationName": "UiAutomator2",
    "fullReset": 'false',
    "newCommandTimeout": "450000",
    "uiautomator2ServerInstallTimeout": "35000",
    "uiautomator2ServerLaunchTimeout": "35000"
}
# --------------------Accounts--------------------------------------------

account_1 = {}

account_2 = {}

# ------------ ENTER DATE AND TIME JUST LIKE SHOWN HERE.......

trigger_hour = 13
trigger_minute = 9
date = "2"
time_slot = "11 AM"

# ------------------------------------------------------------------------

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap_SIA)


if is_logged_in(driver):
    print(f"Trigger Time : {trigger_hour}:{trigger_minute}")
    click_sport_facilities(driver)
    if time_countdown(trigger_hour, trigger_minute):
        click_soccer(driver)
        start_booking(driver, date=date, time_slot=time_slot)
else:
    print(f"Trigger Time : {trigger_hour}:{trigger_minute}")
    m_id, password = account_selection(account_1, account_2)
    start_login_and_navigate(driver, m_id, password)
    if time_countdown(trigger_hour, trigger_minute):
        click_soccer(driver)
        start_booking(driver, date=date, time_slot=time_slot)