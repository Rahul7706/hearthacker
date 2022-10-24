from asyncore import loop
import os
import json
import datetime
import os.path
import time
interval=2
loopr=False
print('created by hearthacker')
def smsforward():
    global loopr
    lastSMS=datetime.datetime.now()
    tmpFile= "tmpLastTime.txt"
    cfgFile="config.txt"

    if not os.path.exists(cfgFile):
        cfile= open(cfgFile, "a")
        filters=input("sms formate ',' :")
        filter_s=filters.split(',')
        cfile.write(filters.lower())
        cfile.write("/n")
        mnum=input("mobile num ',' :")
        mnum_s=mnum.split(",")
        cfile.write(mnum_s)
        cfile.close()
    else:
        cfile=open(cfgFile, "r")
        cdata=cfile.read().splitlines()
        filter_s=cdata[0].split(",")
        mnum_s=cdata[1].split(",")

    if not os.path.exists(tmpFile):
        print("Welcome it is your First Time in my coding")
        tfile=open(tmpFile,"w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        tfile=open(tmpFile,"r")
        lastSMS=datetime.datetime.fromisoformat(tfile.read())
        tfile.close()
    
    if not loopr:
        lop=input(f"keep running after each {interval} second (Yes/No) ? ")
        if lop=="Yes" or "yes" or "y" or "Y":
            loopr=True
            print("Thanks for start>>>  stop(CTRL+C)")
    print(f"Last SMS forward on {lastSMS}")
    jdata= os.popen("termux-sms-list -1 50").read()
    jd=json.loads(jdata)
    print(f"Reading{len(jd)} latest SMS")
    for j in jd:
        if datetime.datetime.fromisoformat(j['received'])>lastSMS:
            for f in filter_s:
                if f in j['body'].lower() and j['type']== "inbox":
                    print(f"{f} found")
                    for m in mnum_s:
                        print(f"Forwarding to {m}")
                        resp=os.popen(f"termux-sms-send -n {m} {j['body']}")
                        tfile= open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
smsforward()
while loopr:
    time.sleep(interval)
    smsforward()
