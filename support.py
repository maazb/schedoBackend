import re
import os
import math
import random
import smtplib
 

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