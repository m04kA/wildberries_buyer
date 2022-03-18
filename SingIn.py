import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2F")
while True:
    try:
        els = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//a[@class="navbar-pc__link" and @href="/lk"]')))
        break
    except TimeoutException:
        pass
# els = driver.find_elements_by_xpath('//input[@data-link="phoneMobile"]')
if els:
    print(els)
    for el in els:
        el.send_keys("+79151901722")

print(1)
driver.close()
