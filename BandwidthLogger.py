from time import sleep

from selenium.webdriver.remote.webdriver import WebDriver
from constants import *
from credentials import *
from BaseLogger import BaseLogger
import requests



class BandwidthLogger(BaseLogger):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.deviceTrafficList=[]

    def go_required_page(self):
        super().go_required_page()
        sleep(1)
        self.driver.get(ADAPTIVE_QOS_PAGE)
        sleep(3)

    def gather_info(self):
        super().gather_info()
        trafficListDivEle=self.driver.find_element_by_id("sortable")
        # seems difficult to extract info by elements
        # okay so we process string...
        trafficListStrList=trafficListDivEle.text.split("\n")
        #print(trafficListStrList)
        # one device has 5 strings
        # 0 -> device name
        # 1 -> upload rate
        # 2 -> upload rate unit
        # 3 -> download rate
        # 4 -> download rate unit
        for i in range(0,len(trafficListStrList),5):
            deviceTraffic={
                "name":trafficListStrList[i],
                "uploadRate":self.unify_rate(trafficListStrList[i+1],trafficListStrList[i+2]),
                "downloadRate":self.unify_rate(trafficListStrList[i+3],trafficListStrList[i+4])
            }
            self.deviceTrafficList.append(deviceTraffic)
        print(self.deviceTrafficList)

    def unify_rate(self,rate:str,unit:str):
        if unit.lower()=="kb":
            return float(rate)
        if unit.lower()=="mb":
            return float(rate)*1024
        


    def upload(self):
        super().upload()
        res=requests.post(SERVER_BANDWIDTH_API,json=self.deviceTrafficList)
        print("[RESULT][BANDWIDTH]" + str(res.status_code))
