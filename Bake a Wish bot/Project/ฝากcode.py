import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import *
import pandas as pd
import datetime
import time
from datetime import datetime, timedelta
from parinya import LINE
line = LINE('iGgobiz5gA1KGNwsJYea0ROgpgFRXPvqRoRuTCdEKCR')
# ดึงข้อมูลจากSheet
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('bakeawishcredentials.json', scope)
# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open("BaK Stock  Nov-22").worksheet("Stock")
data = sheet.get_values()
#print(data)
# แปลงข้อมูล 
df = pd.DataFrame(data)
df.columns = df.loc[1]
df.drop([0,1])
#กำหนดตัวแปรวันที่
timestamp = datetime.now()
tomorrow = timestamp + timedelta(1)
yesterday = timestamp - timedelta(1)
next2day = timestamp + timedelta(2)
next3day = timestamp + timedelta(3)
nday = tomorrow.strftime("%d/%m")
n2day = next2day.strftime("%d/%m")
n3day = next3day.strftime("%d/%m")
#print(df)
#date_time = datetime.fromtimestamp(timestamp)
today = timestamp.strftime("%d-%b")
yes = yesterday.strftime("%d-%b")
focusday = timestamp.strftime("%d/%m")
focusday1 = yesterday.strftime("%d/%m")
tomorrow1 = tomorrow.strftime("%d/%m")
#print(focusday1)
#print(focusday)
#print(tomorrow1)
#กำหนดเวลาการใช้งานโปรแกรม 21:00-03:00 นับเป็นวันเก่า
hour = timestamp.strftime("%H")
if float(hour) < 6:
    timestamp = yesterday
    tomorrow = timestamp + timedelta(1)
    yesterday = timestamp - timedelta(1)
    next2day = timestamp + timedelta(2)
    next3day = timestamp + timedelta(3)
    nday = tomorrow.strftime("%d/%m")
    n2day = next2day.strftime("%d/%m")
    n3day = next3day.strftime("%d/%m")
    today = timestamp.strftime("%d-%b")
    yes = yesterday.strftime("%d-%b")
    focusday = timestamp.strftime("%d/%m")
    focusday1 = yesterday.strftime("%d/%m")
    tomorrow1 = tomorrow.strftime("%d/%m")
#เรียกใช้ตาราง
focus = df[['name',focusday]]
focus.columns = focus.loc[3]
focusm = focus.loc[4:]
focus1 = df[['name',focusday1]]
focus1.columns = focus1.loc[3]
focus1m = focus1.loc[4:]
bbfday = tomorrow1
focusm['รับ'] = focusm['รับ'].replace([''], '0')
#print(focusm)
#print(focus1m)
df1 = focusm[['รับ','name','BBF',today]]
df2 = focus1m[['รับ','name','BBF',yes]]
df2.rename(columns = {'BBF':'BBFO'}, inplace = True)
df1 = pd.concat([df1,df2[yes]], axis=1)
df1 = pd.concat([df1,df2['BBFO']],axis=1)
df1 = df1.replace(['-'], '0')
#print(df1)
#กำหนดค่าในการค้นหา
filt = (df1['BBF'] == bbfday) & (df1['รับ'] != "0") #เช็คว่าของเข้าวันนี้รึเปล่า
filt2 = (df1['BBF'] == bbfday) & (df1[today] != "0") #BBFพรุ่งนี้ 
filt3 = (df1['BBF'] == n2day) & (df1[today] != "0") #BBF 2วัน
filt4 = (df1['BBF'] == n3day) & (df1[today] != "0") #BBF 3วัน
# Source Data
checkdelivery = df1.loc[filt]
exp1 = df1.loc[filt2]
exp2 = df1.loc[filt3]
exp3 = df1.loc[filt4]
checkdelivery.reset_index(drop=True, inplace=True)
exp1.reset_index(drop=True, inplace=True)
exp2.reset_index(drop=True, inplace=True)
exp3.reset_index(drop=True, inplace=True)
#แปลงตารางไว้หาข้อมูล
checkdelivery[yes] = checkdelivery[yes].replace(['-'], '0')
checkdelivery = checkdelivery.copy()
checkdelivery = checkdelivery.astype({'รับ': int,today: int,yes: int})
checkdelivery['test'] = (checkdelivery['รับ'] - checkdelivery[today])

#ฟังก์ชั่นส่งข้อมูลเข้าไลน์ x = ตารางข้อมูล ,  y = วันBBF ที่ต้องการ 
def convertforline(x,y) :
    x = x.rename(columns={"name":"1",today:"2"})
    x = x[["2","1"]]
    x = x.style.set_properties(**{'text-align': 'left'})
    x.hide(axis="index")
    x.hide(axis="columns")
    x = x.to_string()
    #print(x) #for check program
    return line.sendtext("<<<<<BBF" + str(y)+">>>>>>" +"        "+ x)

def convertforlineSND(x,y) :
    x = x.rename(columns={"name":"1",test:"2"})
    x = x[["2","1"]]
    x = x.style.set_properties(**{'text-align': 'left'})
    x.hide(axis="index")
    x.hide(axis="columns")
    x = x.to_string()
    #print(x) #for check program
    return line.sendtext("<<<ของเก่าBBF" + str(y)+">>>" +"        "+ x)
#CASE 1 ไม่มีของเข้า
if checkdelivery.shape[0] == 0:
    if exp1.shape[0] == 0:
        line.sendtext("BBF>>>> " + str(bbfday) +  ">>>>>ไม่มี  ")
    else:
        convertforline(exp1,bbfday)
    if exp2.shape[0] == 0:
        line.sendtext("BBF>>>> " + str(n2day) +  ">>>>>ไม่มี  ")
    else:
        convertforline(exp2,n2day)

#CASE 2 มีของเข้า
else:
#Step 1 Checkของเก่า BBFO
    case2 = checkdelivery
    filtertest = (case2['test'] < 0) #ขายไม่หมด
    filtertest2 = (case2['BBFO'] == bbfday) & (case2[today] != "0")
    filtertest3 = (case2['BBFO'] == n2day) & (case2[today] != "0") #BBF 2วัน
    sell_not_done = cast2.loc[filtertest]
    sell_not_done['test'] = sell_not_done['test'].abs
    SNDtb = sell_not_done['name','test','BBFO']
    SNDtb2 = sell_not_done[filtertest2]
    SNDtb3 = sell_not_done[filtertest3]
    convertforlineSND(SNDtb2,bbfday)
    convertforlineSND(SNDtb3,n2day)
#Step 2 Checkของใหม่ BBF
    filterbbf = (case2['BBFO'] == bbfday) & (case2[today] != "0")
    filterbbf2 = (case2['BBFO'] == n2day) & (case2[today] != "0")
    Ntb = case2['name',today,'BBF']
    Ntb2 = Ntb[filterbbf]
    Ntb3 = Ntb[filterbbf2]
    convertforline(Ntb2,bbfday)
    
    convertforline(Ntb3,n2day)
