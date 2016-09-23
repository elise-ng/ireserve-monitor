from urllib.request import urlopen
from time import strftime
import json
import threading
import os
from colorama import init, Fore, Back, Style
init()

modeldict = {"MN8K2ZP/A":"iP7 32G Rose Gold","MN8J2ZP/A":"iP7 32G Gold","MN8H2ZP/A":"iP7 32G Silver","MN8G2ZP/A":"iP7 32G Black","MN8P2ZP/A":"iP7 128G Rose Gold","MN8N2ZP/A":"iP7 128G Gold","MN8M2ZP/A":"iP7 128G Silver","MN8L2ZP/A":"iP7 128G Black","MN8Q2ZP/A":"iP7 128G Jet Black","MN8V2ZP/A":"iP7 256G Rose Gold","MN8U2ZP/A":"iP7 256G Gold","MN8T2ZP/A":"iP7 256G Silver","MN8R2ZP/A":"iP7 256G Black","MN8W2ZP/A":"iP7 256G Jet Black","MNQL2ZP/A":"iP7+ 32G Rose Gold","MNQK2ZP/A":"iP7+ 32G Gold","MNQJ2ZP/A":"iP7+ 32G Silver","MNQH2ZP/A":"iP7+ 32G Black","MN4C2ZP/A":"iP7+ 128G Rose Gold","MN4A2ZP/A":"iP7+ 128G Gold","MN492ZP/A":"iP7+ 128G Silver","MN482ZP/A":"iP7+ 128G Black","MN4D2ZP/A":"iP7+ 128G Jet Black","MN4K2ZP/A":"iP7+ 256G Rose Gold","MN4J2ZP/A":"iP7+ 256G Gold","MN4F2ZP/A":"iP7+ 256G Silver","MN4E2ZP/A":"iP7+ 256G Black","MN4L2ZP/A":"iP7+ 256G Jet Black"}
storedict = {"R499":"Tsim Sha Tsui","R409":"Causeway Bay","R485":"Festival Walk","R428":"IFC","R610":"Sha Tin","R673":"APM"}
log = ""

def refreshdisplay():
    global localdata
    global log
    os.system('cls')
    print("iReserve Monitor (iPhone 7) by chihimng")
    print()
    print("Models in stock:")
    print()
    for mk,mv in modeldict.items():
        for sk,sv in storedict.items():
            if localdata[sk][mk]!="NONE":
                    print(mv,"/",sv,"/",localdata[sk][mk])
    print("Updated at",strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print("Changelog:")
    print(log)

def updater():
    global localdata
    global log
    threading.Timer(5.0, updater).start()
    response = urlopen('https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability.json')
    data = json.loads(response.readall().decode('utf'))
    if data == {}:
        if localdata != {}:
            log+="iReserve Closed at "+strftime("%Y-%m-%d %H:%M:%S")
    else:
        if localdata == {}:
            localdata = data
            log+="iReseve Opened at "+strftime("%Y-%m-%d %H:%M:%S")
        else:
            changeflag = False

            for mk,mv in modeldict.items():
                for sk,sv in storedict.items():
                    if localdata[sk][mk] != data[sk][mk]:
                        log += "\n"+mv+" / "+sv+" : "+localdata[sk][mk]+" --> "+data[sk][mk]+" at "+strftime("%H:%M:%S")
                        changeflag = True

            if changeflag:
                localdata = data
    refreshdisplay()


print("Initializing...")
response = urlopen('https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability.json')
localdata = json.loads(response.readall().decode('utf'))
if localdata == {} :
    log += "iReserve Closed as of "+strftime("%H:%M:%S")
refreshdisplay()
threading.Timer(5.0, updater).start()
