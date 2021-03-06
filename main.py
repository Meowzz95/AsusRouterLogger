from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

from BandwidthLogger import BandwidthLogger
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
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(1024, 768))
    display.start()
    print("getting pi driver")
    option = webdriver.FirefoxOptions()
    #option.add_argument("headless")
    driver=webdriver.Firefox(executable_path="./geckodriver",options=option)
    return driver

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

    while True:
        deviceListLogger=DeviceListLogger(driver)
        bandwidthLogger=BandwidthLogger(driver)
        try:
            deviceListLogger.run()
        except Exception as ex:
            print("Error in device list logger:")
            print(ex)

        # try:
        #     bandwidthLogger.run()
        # except Exception as ex:
        #     print("Error in bandwidth logger:")
        #     print(ex)
        sleep(2)

