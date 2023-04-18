import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from playsound import playsound
from datetime import datetime
import pytz

SST = pytz.timezone('Asia/Singapore')


def click_member_login(driver):
    member_login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.Button[@text="MEMBER LOGIN"]')))
    member_login.click()


def click_checkbox(driver):
    member_login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.CheckBox[@index="0"]')))
    member_login.click()


def click_login_button(driver):
    member_login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.Button[@text="LOGIN"]')))
    member_login.click()


def click_next_button(driver):
    try:
        member_login = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, f'//android.widget.Button[@text="NEXT"]')))
        member_login.click()
    except(NoSuchElementException, TimeoutException):
        pass


def select_member(driver, member_id):
    member_select = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.TextView[@text="{member_id}"]')))
    member_select.click()


def click_ok_button(driver):
    ok = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.Button[@text="OK"]')))
    ok.click()


def click_sport_facilities(driver):
    sf = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.TextView[@text="Sports Facilities"]')))
    sf.click()


def click_soccer(driver):
    soccer = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.TextView[@text="Soccer"]')))
    soccer.click()


def click_done(driver):
    done = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.Button[@text="Done"]')))
    done.click()


def refresh_page(driver):
    click_soccer(driver)
    click_done(driver)


def play_notification():
    playsound('noti.mp3')


def play_err_notification():
    playsound('error.mp3')


def scroll_to_date(driver):
    try:
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, "new UiScrollable("
                            + "new UiSelector().scrollable(true)).setAsHorizontalList().flingToEnd(2)")
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def check_date(driver, date):
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//android.widget.TextView[@text="{date}"]'))).click()
        return True
    except(NoSuchElementException, TimeoutException):
        return False


def select_slot(driver, time):
    time_inside = time.split(" ")[0]
    DN = time.split(" ")[1]
    try:
        time_slot = WebDriverWait(driver, 3.2).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//android.widget.TextView[contains(@text, '{time_inside}.00 {DN}')]")))
        time_slot.click()
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def check_payment_screen(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//android.widget.TextView[contains(@text, 'PROCEED PAYMENT')]")))
        return True
    except (NoSuchElementException, TimeoutException):
        pass


def type_member_id(member_id, driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.EditText[@password="false"]')))
    driver.find_element(by=By.XPATH, value=f'//android.widget.EditText[@password="false"]').send_keys(member_id)


def type_password(password, driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//android.widget.EditText[@password="true"]')))
    driver.find_element(by=By.XPATH, value=f'//android.widget.EditText[@password="true"]').send_keys(password)


def is_logged_in(driver):
    print(f"Date : {datetime.now(SST).date()}")
    print(f"Current Time : {datetime.now(SST).hour}:{datetime.now(SST).minute}\n")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//android.widget.TextView[@text="Home"]')))
        print("Logged In, Proceeding further...")
        return True
    except (NoSuchElementException, TimeoutException):
        print("---Need to Login---")
        return False


def booking_error(driver):
    try:
        WebDriverWait(driver, 3.5).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//android.widget.Button[@text="OK"]'))).click()
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def start_booking(driver, date, time_slot):
    try:
        while True:
            scroll_to_date(driver)
            if check_date(driver, date):
                print("---Date selected---")
                if select_slot(driver, time=time_slot):
                    print("Slot selecting...")
                    click_next_button(driver)
                    if booking_error(driver):
                        print("Booking box error!!")
                        refresh_page(driver)
                        play_err_notification()
                    else:
                        print("---Slot selected---")
                        click_next_button(driver)
                        click_next_button(driver)
                        click_checkbox(driver)
                        play_notification()
                        break
                else:
                    refresh_page(driver)
            else:
                print("---Given Date is not here---")
                refresh_page(driver)

    except(NoSuchElementException, TimeoutException):
        pass


def start_login_and_navigate(driver, member_id, password):
    click_member_login(driver)
    type_member_id(member_id, driver)
    type_password(password, driver)
    click_checkbox(driver)
    click_login_button(driver)
    select_member(driver, member_id)
    click_ok_button(driver)
    click_sport_facilities(driver)


def account_selection(account_1, account_2):
    account_select = input("\nSelect account 1 or 2 : ")
    if account_select == "1":
        account = account_1.copy()
        print("------------------------------------------\n")
        print(f"\nMember ID : {account['member_id']}\n"
              f"Password : {account['password']}")
    elif account_select == "2":
        account = account_2.copy()
        print("------------------------------------------\n")
        print(f"\nMember ID : {account['member_id']}\n"
              f"Password : {account['password']}")
    return account["member_id"], account["password"]


def time_countdown(hr, minit):
    while True:
        hour = datetime.now(SST).hour
        minute = datetime.now(SST).minute
        second = datetime.now(SST).second
        print(f"{hour}" + ":" + f"{minute}" + ":" + f"{second}")
        time.sleep(1)
        if hour == hr and minute == minit:
            print("Time triggered...")
            return True
            break
