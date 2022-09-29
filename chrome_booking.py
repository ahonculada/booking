import os
import time
import platform
from contextlib import contextmanager
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()



os.chdir(os.path.dirname(__file__))

@contextmanager
def driver(*args, **kwargs):
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--start-fullscreen')
    # chrome_options.add_argument('--single-process')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument(f'user-agent={fake_agent}')
    # chrome_options.add_argument('--ignore-ssl-errors=yes')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-popup-blocking")

    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options,)
    # d.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source":
    #         "const newProto = navigator.__proto__;"
    #         "delete newProto.webdriver;"
    #         "navigator.__proto__ = newProto;"
    # })

    try:
        yield d
    finally:
        d.quit()

class BookingBot:
    def __init__(self, driver) -> None:
        self.driver = driver
        # self.driver

    def run(self):
        self.driver.get(f'https://ucf.libcal.com/r/accessible/availability?lid=2824&gid=4779&zone=0&space=0&capacity=3&accessible=&powered=&date={(date.today() + timedelta(days=7)).strftime("%Y-%m-%d")}')

        # location = Select(self.driver.find_element(By.ID,'s-lc-location'))
        # location.select_by_index(1)

        # capacity = Select(self.driver.find_element(By.ID,'s-lc-type'))
        # capacity.select_by_index(3)

        # show_avail_button = self.driver.find_element(By.ID,'s-lc-go')
        # show_avail_button.click()

        # booking_date = Select(self.driver.find_element(By.ID,'date'))
        # booking_date.select_by_index(7)

        show_avail_button = self.driver.find_element(By.ID,'s-lc-submit-filters')
        show_avail_button.click()

        checkboxes = self.driver.find_elements(By.CLASS_NAME,'booking-checkbox')
        start = 7
        stop = start + 8
        for i in range(start,len(checkboxes)):
            if i == stop:
                break
            time.sleep(1)
            if checkboxes[i]:
                checkboxes[i].click()

        submit_button = self.driver.find_element(By.ID,'s-lc-submit-times')
        submit_button.click()

        time.sleep(5)

        # clear the input fields before signing in
        username_input = self.driver.find_element(By.NAME,'UserName')
        username_input.clear()
        username_input.send_keys(os.getenv("USER_NAME"))

        password_input = self.driver.find_element(By.NAME,'Password')
        password_input.clear()
        password_input.send_keys(os.getenv("PASSWORD"))

        sign_on_button = self.driver.find_element(By.ID,'submitButton')
        sign_on_button.click()

        time.sleep(3)

        continue_button = self.driver.find_element(By.NAME,'continue')
        continue_button.click()

        time.sleep(3)

        public_name = self.driver.find_element(By.ID,'nick')
        public_name.send_keys(os.getenv("STUDY_GROUP_NAME"))

        status = Select(self.driver.find_element(By.ID,'q2613'))
        status.select_by_index(2)

        ucfid = self.driver.find_element(By.ID,'q2614')
        ucfid.send_keys(os.getenv("PID"))

        submit_button = self.driver.find_element(By.ID,'s-lc-eq-bform-submit')
        submit_button.click()

        time.sleep(5)

        with open('/tmp/test.txt', 'a') as f:
            submitErrors = self.driver.find_element(By.ID, 'submit-errors')
            print(submitErrors.text)
            if submitErrors:
                f.write('Errors: {}, date: {}.\n'.format(submitErrors.text,datetime.now()))
            else:
                f.write('Hooray! We booked a room for a week after today, {}.\n'.format(datetime.now()))


def main():
    with driver() as wd:
        bot = BookingBot(wd)
        bot.run()



if __name__ == '__main__':
    if platform.system() == 'Linux':
        main()
    else:
        print('you need to be running this on a linux machine')

'''
import os
import random as rand
from time import strftime, sleep
from secrets import Secrets
from selenium import webdriver

from fake_useragent import FakeUserAgentError, UserAgent
import concurrent.futures
import pandas as pd


ua = None
while True:
    try:
        ua = UserAgent()
        break
    except FakeUserAgentError:
        print('fake user agent error')
        continue
    except Exception:
        continue

fake_agent = ua.random




























'''
