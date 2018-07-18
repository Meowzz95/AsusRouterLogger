import datetime
from time import sleep

from selenium.webdriver.remote.webdriver import WebDriver
from constants import *
from credentials import *
from BaseLogger import BaseLogger
import requests
from bs4 import BeautifulSoup
from dbHelper import createOrUpdateDevice,setDeviceState,getAllDevices
from mailHelper import send_email


class DeviceListLogger(BaseLogger):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.deviceList = []
        self.textToBeSent=""


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
        #print(clientListDivEle.get_attribute("outerHTML"))
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
        self.processSmartHome()
        print(self.deviceList)

    def processSmartHome(self):
        self.textToBeSent=""
        self.updateDb()
        deviceDbObjList=getAllDevices()
        for deviceDbObj in deviceDbObjList:
            self.processState(deviceDbObj)
        if self.textToBeSent:
            print("SENDING EMAIL")
            send_email(NOTIFY_EMAIL,"FROM MIMIMI'S SMART HOME",self.textToBeSent)
        pass

    def processState(self,deviceDbObj):
        nowDt=datetime.datetime.now()
        print("processState  device name = {}".format(deviceDbObj.name))
        if deviceDbObj.state == STATE_ONLINE:
            diff=nowDt - deviceDbObj.lastSeen
            print("current online dev check diff = {}".format(diff.seconds))
            if diff.seconds > OFFLIE_THRESHOLD_SEC:
                # this device goes offline
                self.handleOffline(deviceDbObj)
        elif deviceDbObj.state == STATE_OFFLINE:
            diff=nowDt-deviceDbObj.lastSeen
            print("current offline dev check diff = {}".format(diff.seconds))
            if diff.seconds < OFFLIE_THRESHOLD_SEC:
                #this device goes online
                self.handleOnline(deviceDbObj)

    def handleOffline(self,deviceDbObj):
        print(deviceDbObj.name,"goes offline")
        setDeviceState(deviceDbObj.mac,STATE_OFFLINE)
        self.textToBeSent+="\n{} goes OFFLINE".format(deviceDbObj.name)
        pass
    def handleOnline(self,deviceDbObj):
        print(deviceDbObj.name,"goes online")
        setDeviceState(deviceDbObj.mac, STATE_ONLINE)
        self.textToBeSent += "\n{} goes ONLINE".format(deviceDbObj.name)
        pass

    def updateDb(self):
        for deviceObj in self.deviceList:
            createOrUpdateDevice(deviceObj["mac"], deviceObj["name"])



    def upload(self):
        super().upload()
        resp=requests.post(SERVER_DEVICE_LIST_API,json=self.deviceList)
        print("[RESULT][DEVICELIST]"+str(resp.status_code))








