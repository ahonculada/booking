import os
import platform
import random
from time import sleep
from contextlib import contextmanager
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager

# Parse a .env file in the local directory and then load all the variables found as environment variables.
load_dotenv()

# force the path to be local in this directory no matter where this script is called
os.chdir(os.path.dirname(__file__))

# using a context manager guarantees we quit out the browser after regardless of whether the program fails
@contextmanager
def driver(*args, **kwargs):
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.set_preference('detach', True)
    d = webdriver.Firefox(service=Service(GeckoDriverManager().install(), log_path='/tmp/leo_version_booking.log'), options=firefox_options,)
    try:
        yield d
    finally:
        d.quit()

class BookingBot:
    def __init__(self, driver) -> None:
        self.driver = driver

    def run(self):
        self.driver.get(f'https://ucf.libcal.com/r/accessible/availability?lid=2824&gid=4779&zone=0&space=0&capacity=3&accessible=&powered=&date={(date.today() + timedelta(days=7)).strftime("%Y-%m-%d")}')

        show_avail_button = self.driver.find_element(By.ID,'s-lc-submit-filters')
        show_avail_button.click()

        # spaces should be replaced with periods whenever searching a class name in selenium
        divPanels = self.driver.find_elements(By.CLASS_NAME, 'panel.panel-default')

        print(f'number of panels: {len(divPanels)}')

        for panel in divPanels:
            print(panel.text)
            break

        # we know the first panel is room 176 so we greedily pick that
        checkboxes = divPanels[0].find_elements(By.CLASS_NAME,'booking-checkbox')
        # for cb in checkboxes:
        #     print(cb.find_element(By.XPATH, '..').text)
        # start = 7
        # stop = start + 8
        # for i in range(start,len(checkboxes)):
        #     if i == stop:
        #         break
        #     sleep(random.uniform(0.1,0.5))
        #     if checkboxes[i]:
        #         checkboxes[i].click()

        desiredTimes = set(
            [
                '4:30pm - 5:00pm',
                '5:00pm - 5:30pm',
                '5:30pm - 6:00pm',
                '6:00pm - 6:30pm',
                '6:30pm - 7:00pm',
                '7:00pm - 7:30pm',
                '7:30pm - 8:00pm',
                '8:00pm - 8:30pm'
            ]
        )
        for cb in checkboxes:
            if cb and cb.find_element(By.XPATH, '..').text.strip() in desiredTimes:
                cb.click()
            sleep(random.uniform(0.1,0.5))

        submit_button = self.driver.find_element(By.ID,'s-lc-submit-times')
        submit_button.click()

        sleep(random.uniform(4,5))

        # clear the input fields before signing in
        username_input = self.driver.find_element(By.NAME,'UserName')
        username_input.clear()
        username_input.send_keys(os.getenv("USER_NAME"))

        password_input = self.driver.find_element(By.NAME,'Password')
        password_input.clear()
        password_input.send_keys(os.getenv("PASSWORD"))

        sign_on_button = self.driver.find_element(By.ID,'submitButton')
        sign_on_button.click()

        sleep(random.uniform(2,3))

        continue_button = self.driver.find_element(By.NAME,'continue')
        continue_button.click()

        sleep(random.uniform(2,3))

        public_name = self.driver.find_element(By.ID,'nick')
        public_name.send_keys(os.getenv("STUDY_GROUP_NAME"))

        status = Select(self.driver.find_element(By.ID,'q2613'))
        status.select_by_index(2)

        ucfid = self.driver.find_element(By.ID,'q2614')
        ucfid.send_keys(os.getenv("PID"))

        submit_button = self.driver.find_element(By.ID,'s-lc-eq-bform-submit')
        submit_button.click()

        sleep(random.uniform(4,5))

        with open('/tmp/test.txt', 'a') as f:
            submitErrors = self.driver.find_element(By.ID, 'submit-errors')
            # print(submitErrors.text)
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
        with open('leo_version_booking.log', 'a') as f:
            f.write('you need to be running this on a linux machine')
            print('you need to be running this on a linux machine')
