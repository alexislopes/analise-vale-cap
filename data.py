from datetime import date
from datetime import datetime


data = date.today()
agora = datetime.now().time().hour

def eDomingo():
    return data.weekday()

def queHoras():
    return  agora

def vai():
    go = False
    if eDomingo() == 5 and queHoras()  >= 12:
        go = True
    return go