import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

with open("./secrets/password.txt", "r") as file:
    Lines = file.readlines()

username = Lines[0].strip()
password = Lines[1].strip()

opt = Options()
opt.headless = True
driver = webdriver.Firefox(options=opt, log_path='/tmp')
driver.get('https://ucf.libcal.com/r/accessible?lid=2824&gid=4779')
location = Select(driver.find_element_by_id('s-lc-location'))
location.select_by_index(1)

capacity = Select(driver.find_element_by_id('s-lc-type'))
capacity.select_by_index(3)

show_avail_button = driver.find_element_by_id('s-lc-go')
show_avail_button.click()

date = Select(driver.find_element_by_id('date'))
date.select_by_index(7)

show_avail_button = driver.find_element_by_id('s-lc-submit-filters')
show_avail_button.click()

checkboxes = driver.find_elements_by_class_name('booking-checkbox')
start = 7
stop = start + 8
for i in range(start,len(checkboxes)):
    if i == stop:
        break
    if checkboxes[i]:
        checkboxes[i].click()

submit_button = driver.find_element_by_id('s-lc-submit-times')
submit_button.click()

time.sleep(3)

username = driver.find_element_by_name('UserName')
username.send_keys(username)

password = driver.find_element_by_name('Password')
password.send_keys(password)

sign_on_button = driver.find_element_by_id('submitButton')
sign_on_button.click()

time.sleep(3)

continue_button = driver.find_element_by_name('continue')
continue_button.click()

time.sleep(3)

public_name = driver.find_element_by_id('nick')
public_name.send_keys('Graduate Study Group')

status = Select(driver.find_element_by_id('q2613'))
status.select_by_index(2)

ucfid = driver.find_element_by_id('q2614')
ucfid.send_keys(2788042)

submit_button = driver.find_element_by_id('s-lc-eq-bform-submit')
submit_button.click()

time.sleep(5)

driver.quit()

with open('/tmp/test.txt', 'a') as f:
    f.write('Hooray! We booked a room for a week after today, {}.\n'.format(datetime.now()))

