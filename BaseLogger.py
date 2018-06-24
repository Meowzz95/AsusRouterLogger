from selenium.webdriver.remote.webdriver import WebDriver


class BaseLogger:
    def __init__(self,driver:WebDriver):
        self.driver=driver

    def go_required_page(self):
        pass

    def gather_info(self):
        self.go_required_page()
        pass

    def upload(self):
        pass

    def run(self):
        self.gather_info()
        self.upload()