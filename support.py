import re
import os
import math
import random
import smtplib
from datetime import datetime, timedelta

import crud
from sqlalchemy.orm import Session
 

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 

def checkEmail(email: str) -> bool:
 
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
    
def sendOTP(email: str) -> str:
    digits="0123456789"
    OTP=""
    for i in range(4):
        OTP+=digits[math.floor(random.random()*10)]
    otp = OTP + " is your OTP for SchedoMeet"
    msg= otp
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("schedomeet.app@gmail.com", "yflwijxsnfybizwe")
    s.sendmail('&&&&&&&&&&&',email,msg)
    return OTP



def get_slots(hours, appointments, min):
            duration = timedelta(minutes=min)
            freeSlots = []
            appointments.sort()
            slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
            for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
                # assert start <= end, "Cannot attend all appointments"
                while start + duration <= end:
                    if start > hours[0] and (start + duration)<hours[1]:
                        freeSlots.append((datetime.strftime(start,'%Y-%m-%dT%H:%M:%SZ'),datetime.strftime(start+duration,'%Y-%m-%dT%H:%M:%SZ')))
                    # print ("{:%H:%M} - {:%H:%M}".format(start, start + duration))
                    start += duration
            return freeSlots





def checkSlots(uids: list[int], dt: str,pst: str, pet: str, db: Session, min: int):
    print("starting check slots")
    allFreeSlots = []
    commonFreeSlots = []
    for x in uids:
        meetings = crud.get_user_meetings(db=db, date=dt,userId=x)
        
        print("meeting len: ")
        print(len(meetings))
    
        appointments = []
        for y in meetings:
            appointments.append((datetime.strptime(y.start_time,'%Y-%m-%dT%H:%M:%SZ'),datetime.strptime(y.end_time,'%Y-%m-%dT%H:%M:%SZ')))

        print("appointment len: ")
        print(len(appointments))
        
        hours = (datetime.strptime(pst,'%Y-%m-%dT%H:%M:%SZ'), datetime.strptime(pet,'%Y-%m-%dT%H:%M:%SZ'))
        
        

        allFreeSlots.append(get_slots(hours, appointments, min)) 
        
    commonFreeSlots = set(
    allFreeSlots[0]
    ).intersection(*allFreeSlots)
    
    
    
    # for x in commonFreeSlots:
    return commonFreeSlots

    # if __name__ == "__main__":
    #     get_slots(hours, appointments)
    
    
def checkSlotsEvents(uids: list[int], dt: str,pst: str, pet: str, db: Session, min: int):
    print("starting check slots")
    allFreeSlots = []
    commonFreeSlots = []
    for x in uids:
        meetings = crud.get_user_events(db=db, date=dt,userId=x)
        
        print("meeting len: ")
        print(len(meetings))
    
        appointments = []
        for y in meetings:
            appointments.append((datetime.strptime(y.start_time,'%Y-%m-%dT%H:%M:%SZ'),datetime.strptime(y.end_time,'%Y-%m-%dT%H:%M:%SZ')))

        print("appointment len: ")
        print(len(appointments))
        
        hours = (datetime.strptime(pst,'%Y-%m-%dT%H:%M:%SZ'), datetime.strptime(pet,'%Y-%m-%dT%H:%M:%SZ'))
        
        

        allFreeSlots.append(get_slots(hours, appointments, min)) 
        
    commonFreeSlots = set(
    allFreeSlots[0]
    ).intersection(*allFreeSlots)
    
    
    
    # for x in commonFreeSlots:
    return commonFreeSlots

    # if __name__ == "__main__":
    #     get_slots(hours, appointments)