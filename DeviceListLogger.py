from time import sleep

from selenium.webdriver.remote.webdriver import WebDriver
from constants import *
from credentials import *
from BaseLogger import BaseLogger
import requests
from bs4 import BeautifulSoup


class DeviceListLogger(BaseLogger):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.deviceList = []

    def go_required_page(self):
        super().go_required_page()
        self.driver.get(INDEX_PAGE)


    def gather_info(self):
        super().gather_info()
        print("garthing info, device list")
        self.driver.execute_script("pop_clientlist_listview(true)")
        #wait list to load
        sleep(2)
        clientListDivEle=self.driver.find_element_by_id(CLIENT_LIST_DIV_ID)
        print(clientListDivEle.get_attribute("outerHTML"))
        bsClientListDivEle=BeautifulSoup(clientListDivEle.get_attribute("outerHTML"),"html.parser")
        bsTrs=bsClientListDivEle.findAll("tr")
        for bsTr in bsTrs:
            bsTds=bsTr.findAll("td")
            bsIpField=bsTds[3]
            bsIpTypeSpan=bsIpField.findAll("span")[0]

            bsIpStr=bsIpField.find(text=True,recursive=False)
            bsIpType=bsIpTypeSpan.getText()
            device = {
                "name": bsTds[2].getText(),
                "ip": bsIpStr,
                "ipType": bsIpType,
                "mac": bsTds[4].getText(),
                "accessTime": bsTds[8].getText()
            }
            self.deviceList.append(device)

        # trs=clientListDivEle.find_elements_by_tag_name("tr")
        # for tr in trs:
        #     tds=tr.find_elements_by_tag_name("td")
        #     ipField=tds[3].text  #type:str
        #     ipFieldStrs=ipField.split("\n")
        #     ipStr=ipFieldStrs[0]
        #     ipType=ipFieldStrs[1]
        #
        #     device= {
        #         "name": tds[2].text,
        #         "ip": ipStr,
        #         "ipType":ipType,
        #         "mac": tds[4].text,
        #         "accessTime": tds[8].text
        #     }
        #     self.deviceList.append(device)
        print(self.deviceList)

    def upload(self):
        super().upload()
        resp=requests.post(SERVER_DEVICE_LIST_API,json=self.deviceList)
        print(resp.status_code)








