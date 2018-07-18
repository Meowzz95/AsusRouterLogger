import datetime

from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('sqlite:///data.db', echo=False)
SessionClass = sessionmaker(bind=engine)
Base=declarative_base()

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    mac = Column(String)
    name = Column(String)
    lastSeen = Column(DateTime)
    state=Column(Integer,default=0)



class Record(Base):
    __tablename__='record'
    id = Column(Integer, primary_key=True)
    event = Column(String)
    datetime=Column(DateTime,server_default=func.now())

    device_id=Column(Integer,ForeignKey('device.id'))
    device= relationship("Device",backref="records")

Base.metadata.create_all(engine)


def createOrUpdateDevice(mac:str, name:str):
    session = SessionClass()
    device = session.query(Device).filter(Device.mac == mac).one_or_none()
    if not device:
        device = Device()
        device.mac=mac
        device.name=name
        device.lastSeen=datetime.datetime.now()
        session.add(device)
        session.commit()
    else:
        device.name=name
        device.lastSeen = datetime.datetime.now()
        session.commit()
    session.close()
    return device

def addRecord(device:Device,event:str):
    session = SessionClass()
    record=Record()
    record.device=device
    record.event=event
    session.add(record)
    session.commit()
    session.close()

def getAllDevices():
    session=SessionClass()
    allDevices=session.query(Device).all()
    session.expunge_all()
    session.close()
    return allDevices

def setDeviceState(mac:str,state:Integer):
    session=SessionClass()
    device = session.query(Device).filter(Device.mac == mac).one()
    device.state=state
    session.commit()
    session.close()



