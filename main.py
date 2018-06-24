from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

from DeviceListLogger import DeviceListLogger
from constants import *
from credentials import *
import platform

# used for testing on computer
def get_mac_driver():
    driver=webdriver.Chrome(executable_path="./chromedriver")
    return driver

# used on PI, actual run
def get_pi_driver():
    pass

def get_system():
    return platform.system()

def login_driver(driver:WebDriver):
    driver.get(ROUTER_IP)
    sleep(1)
    usernameEle=driver.find_element_by_id(LOGIN_USERNAME_ID)
    usernameEle.send_keys(USERNAME)
    pwdEle=driver.find_element_by_name(LOGIN_PWD_NAME)
    pwdEle.send_keys(PASSWORD)
    driver.execute_script("login();")




if __name__ == '__main__':
    # ONLY ONE DRIVER
    # since the asus router admin page only allows one user to be logged in
    # once the admin account is logged in from the second device, the first will be logged out automatically
    if get_system() == SYSTEM_MAC_PLATFORM:
        driver=get_mac_driver()
    elif get_system() == SYSTEM_PI_PLATFORM:
        driver=get_pi_driver()
    else:
        raise Exception("Unsupported system")

    login_driver(driver)
    deviceListLogger=DeviceListLogger(driver)
    deviceListLogger.run()

