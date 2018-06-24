from time import sleep

from selenium.webdriver.remote.webdriver import WebDriver
from constants import *
from BaseLogger import BaseLogger


class BandwidthLogger(BaseLogger):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def go_required_page(self):
        super().go_required_page()
        self.driver.get(ADAPTIVE_QOS_PAGE)
        sleep(1)

    def gather_info(self):
        super().gather_info()


    def upload(self):
        super().upload()