from flask import Flask, request, abort
from Project import *
import json
import requests
from Project import Config

app = Flask(__name__)
#Channel_access_token = "lC4wc7tnNme8DCAtnsMIJvC+ALCItcOLpbBZt/Zn9acDz/rx0xMhtEFGIKDZx1e7jPSY1itedeRsyuhl6eSxAsf1PAHtaoN3HIylnCT5KHxDjV/6nBIFzeDO4W3VPMBdAP471xFtKOh/R9v8/+5XwwdB04t89/1O/w1cDnyilFU="
Channel_access_token = Config.Channel_access_token

@app.route('/')
def hello():
    return 'hello Top', 201

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 201

@app.route('/webhook', methods = ['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(payload)
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'bot' in message:
            Reply_messasge = 'Bot running'
            ReplyMessage(Reply_token, Reply_messasge, Channel_access_token)


        elif "bbf" in message:
            Reply_messasge = 'ยังไม่ได้ทำ'
            ReplyMessage(Reply_token, Reply_messasge, Channel_access_token)

        elif "Menu"or"คู่มือ" in message:
            Reply_messasge = 'เลือกพิมพ์คำว่า : >bbf< : >ตารางงาน< : >สินค้าในstock<'
            ReplyMessage(Reply_token, Reply_messasge, Channel_access_token)

        elif "ตารางงาน" in message:
            Reply_messasge = 'ยังไม่ได้ทำตารางาน'
            ReplyMessage(Reply_token, Reply_messasge, Channel_access_token)

        elif "สินค้า"or"stock" in message:
            Reply_messasge = 'ยังไม่ได้ทำstock'
            ReplyMessage(Reply_token, Reply_messasge, Channel_access_token)

        return request.json, 201

    elif request.method == 'GET':
        return 'this is method GET!!!', 201

    else:
        abort(400)
