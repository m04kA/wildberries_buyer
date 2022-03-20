from pprint import pprint
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_cookie_user() -> str:
    try:
        logger.info("Open Chrome for sing in.")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    except ConnectionError:
        logger.error("Wrong connect!")
        raise ConnectionError("Check internet connection.")

    driver.get("https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2F")
    while True:
        try:
            logger.info("Wait sign in")
            els = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="navbar-pc__link" and @href="/lk"]')))
            break
        except TimeoutException:
            pass
    logger.debug("Get cookie")
    my_cookies = driver.get_cookie('WILDAUTHNEW_V3')["value"]
    # driver.get("https://www.wildberries.ru/data?")
    # headers = driver.execute_script("var req = new XMLHttpRequest();req.open('GET', document.location, false);req.send(null);return req.getAllResponseHeaders()")

    # type(headers) == str

    # headers = headers.splitlines()
    # print(headers)

    driver.close()
    logger.debug("Close chrome")
    return my_cookies

