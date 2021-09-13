import time
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
except ImportError:
    with open('/tmp/test.txt', 'a') as f:
        f.write('CANNOT FIND IMPORT\n')

now = datetime.now()
with open('/tmp/test.txt', 'a') as f:
    f.write('{} is the current date and time\n'.format(now))

opt = Options()
opt.headless = True
driver = webdriver.Firefox(options=opt)
driver.get('https://amazon.com')

time.sleep(8)

with open('/tmp/test.txt', 'a') as f:
    f.write('Horray! Successfully opened website.\n')


driver.quit()


