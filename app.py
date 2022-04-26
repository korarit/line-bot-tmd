from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import json

from datetime import (date, timedelta, datetime)

app = Flask(__name__)

#api line bot key
line_bot_api = LineBotApi('Z73uaOfQbjn3zjPJq9NQ9lVesn3YbDmm/3aQb2nktCKCWHmHSxQsCQv8Wz8oh1fgm/74pzVHHJee9Te2jiWAAFcvK5MwRIo3b4ne68e+3mIJ0qLBGXGJcXmWLYHe7kVpdJkekF3kOSLRfawbFmsYEQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('60c9d887805e00521665083b6735ddf7')

data_select = 'not_have'

#api key กรมอุตุนิยมวิทยา
api_tmd = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIyYTFkNjY4M2MwYTBmMzcwNDNhMmNkZTA1ODUyMTliOGZhYjdiMjQzZWYzNDAyMTY2ZGY0MDQ4ZTA3MGVmYzAxNGRlMThmYmYxYTQzM2YyIn0.eyJhdWQiOiIyIiwianRpIjoiYjJhMWQ2NjgzYzBhMGYzNzA0M2EyY2RlMDU4NTIxOWI4ZmFiN2IyNDNlZjM0MDIxNjZkZjQwNDhlMDcwZWZjMDE0ZGUxOGZiZjFhNDMzZjIiLCJpYXQiOjE2Mjg5MzI0MjgsIm5iZiI6MTYyODkzMjQyOCwiZXhwIjoxNjYwNDY4NDI4LCJzdWIiOiI5NTQiLCJzY29wZXMiOltdfQ.WpR-KbNJrJm6rmcWdHHyKG-COOL1bBA_wulgD1o7-5axdOWgNhEKx4TQiUNefXE9MqCtC1bRR7-nHTyaN7awhMS6reU2qciV4ULJRKOKTRV5ap1JdpZxakkU0QvE4TMgxhLTEZYiZdl4t_Y7UiIxAQo-75hXMNu-rGoM5KknRp2NAZbnEOnrFMAVBUwi0H7woj1XH9lUXWZ8W87-vHdOO7_ng1KtH21QCGVR1xmnr2vfp3Z766BxXlb_CODOIf3RFFyZWDcZwZxgibmSOad-YAl4R5SU21zetJyMFNS_6X5W5_3S-3AVpHiyn1XoXXkryPSRyzIIFkjTyDc0dj8bC-G5im9iyN-jB47PXfVSaDa1M7t3EGOnGpJdlBO_W1WiHLRNznFAmptL35yFEvPXy9x744vAzXRxTWFGepTjpiyXKE7mOPiajaFfjdKp05WCEfYXZxfM1evIbPieNTUd1KLVhqEi0e433V5-JkEt7udCmX-p6iCj1QNdTzc1ckDnXzdR_LVDNqtYa7y5YdEBwAs8qJGt-SArsvol0riCS-CWkYlOc5PkOGgX9ia4aDpnVcMXMVBEJRkPUT1jRBw6_lUG3kelBbMVJcDoPH32fg33RXz4EYugUY4wS7YiPFrpIzQ-5WCnexjeWGr6PmNqIe8yc-QqGnv246vlyjmU0IU'

@app.route("/callback", methods=['POST'])
def callback():
    global data_select
    # get request body as text
    body = request.json

    #get reply tonken
    Reply_token = body['events'][0]['replyToken']

    #type message form user
    types = body['events'][0]['message']['type']

    if types == "text":
        message_text = str(body['events'][0]['message']['text'])

        if message_text == "พยากรณ์อากาศ 3ชั่วโมง":
            if data_select == "not_have":
                data_select = 'พยากรณ์อากาศ 3ชั่วโมง'
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาส่ง location เพื่อค้นหาข้อมูล'))
            else:
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
                data_select = "not_have"  
        elif message_text == "พยากรณ์อากาศ วันนี้":
            if data_select == "not_have":
                data_select = 'พยากรณ์อากาศ วันนี้'
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาส่ง location เพื่อค้นหาข้อมูล'))
            else:
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
                data_select = "not_have"
                
        elif message_text == "พยากรณ์อากาศ 3วัน":

            if data_select == "not_have":
                data_select = 'พยากรณ์อากาศ 3วัน'
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาส่ง location เพื่อค้นหาข้อมูล'))
            else:
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
                data_select = "not_have"
                
        elif message_text == "ติดต่อผู้พัฒนา":

            if data_select == "not_have":
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='====== Facebook ======\n\nhttps://www.facebook.com/krt.korarit\n\n====== Youtube =======\n\nhttps://www.youtube.com/channel/UC3ZDblNrSZRnJe_-0Zv52QA\n\n====== Github ========\n\nhttps://github.com/korarit'))
            else:
                line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
                data_select = "not_have"

        else:
            line_bot_api.reply_message(Reply_token, TextSendMessage(text='ไม่สามารถพิมพ์ข้อความเพื่อคุยกับ บอทได้ในขณะนี้'))
    #check message type is location
    elif types == "location":
        if data_select == "not_have":
            line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาเลือก ฟังก์ชั่นการพยากรณ์อากาศ'))
        else:
            if data_select == "พยากรณ์อากาศ 3ชั่วโมง":
                lat = body['events'][0]['message']['latitude']
                lon = body['events'][0]['message']['longitude']
                txtresult = hour3(lat,lon)
                replyObj = TextSendMessage(text=txtresult)
                line_bot_api.reply_message(Reply_token, replyObj)
                data_select = "not_have"
            elif data_select == "พยากรณ์อากาศ วันนี้":
                lat = body['events'][0]['message']['latitude']
                lon = body['events'][0]['message']['longitude']
                txtresult = day_now(lat,lon)
                replyObj = TextSendMessage(text=txtresult)
                line_bot_api.reply_message(Reply_token, replyObj)
                data_select = "not_have"
            elif data_select == "พยากรณ์อากาศ 3วัน":
                lat = body['events'][0]['message']['latitude']
                lon = body['events'][0]['message']['longitude']
                txtresult = day3(lat,lon)
                replyObj = TextSendMessage(text=txtresult)
                line_bot_api.reply_message(Reply_token, replyObj)
                data_select = "not_have"
    else:
        line_bot_api.reply_message(Reply_token, TextSendMessage(text='กรุณาส่งเป็น location!'))
    return ''

def hour3(lat,lon):
        #ดึงวันที่ปัจจุบัน
        today = date.today()
        day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล

        #ดึงเวลาปัจจุบัน
        time_now = datetime.now()
        current_time = time_now.strftime("%H") #วันทีสำหรับใช้ในการดึงข้อมูล
        #วันทีสำหรับใช้ในการส่งหา user
        time_text = time_now.strftime("%H:%M:%S") #เวลาปัจจุบัน

        #1 ชั่วโมงถัดไป
        next_time2 = datetime.now() + timedelta(hours=1)
        time2_text = next_time2.strftime("%H:%M:%S")  #เวลาสำหรับใช้ในการส่งหา user
        #2 ชั่วโมงถัดไป
        next_time3 = datetime.now() + timedelta(hours=2)
        time3_text = next_time3.strftime("%H:%M:%S") #เวลาสำหรับใช้ในการส่งหา user

        #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา
        url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"

        querystring = {"lat":lat, "lon":lon, "fields":"tc,rain,cond", "date":day, "hour":"8", "duration":"3"}

        headers = {
            'accept': "application/json",
            'authorization': "Bearer " + api_tmd,
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        #นำข้อ
        getdata = json.loads(response.text)
        print(response.text)

        ##นำข้อมูลใน array getdata มาใช้##
        #ดึงข้อมูล สภาพอากาศทั่วไป ของชั่วโมงปัจจุบัน และ 2ชั่วโมงถัดไป แล้วแปลงเป็นคำที่เข้าใจโดยใช้ fuction get_cond
        cond_time1 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][0]['data']['cond'])
        cond_time2 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][1]['data']['cond'])
        cond_time3 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][2]['data']['cond'])

        #ดึงข้อมูล อุณหภูมิ ของชั่วโมงปัจจุบัน และ 2ชั่วโมงถัดไป หน้วยเป็นองศา
        tc_time1 = getdata['WeatherForecasts'][0]['forecasts'][0]['data']['tc']
        tc_time2 = getdata['WeatherForecasts'][0]['forecasts'][1]['data']['tc']
        tc_time3 = getdata['WeatherForecasts'][0]['forecasts'][2]['data']['tc']


        data_return = 'เวลา ' + time_text + '\nสภาพอากาศ : ' + cond_time1 + '\nอุณหภูมิ : ' + str(tc_time1) + ' °C\n======================='+'\nเวลา ' + time2_text + '\nสภาพอากาศ : ' + cond_time2 + '\nอุณหภูมิ : ' + str(tc_time2) + ' °C\n======================='+'\nเวลา ' + time3_text + '\nสภาพอากาศ : ' + cond_time3 + '\nอุณหภูมิ : ' + str(tc_time3) + ' °C\n======================='
        return data_return

def day_now(lat,lon):
    
    #ดึงวันที่ปัจจุบัน
    today = date.today()
    day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล
    #วันทีสำหรับใช้ในการส่งหา user
    day_text = today.strftime("%d / %m / %Y") #วันปัจจุบัน

    #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at"

    querystring = {"lat":lat, "lon":lon, "fields":"tc_min,tc_max,rain,cond", "date":day, "hour":"8", "duration":"1"}

    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + api_tmd,
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #นำข้อ
    getdata = json.loads(response.text)

    ##นำข้อมูลใน array getdata มาใช้##
    #ดึงข้อมูล สภาพอากาศทั่วไป ของวันปัจจุบันและวันถัดไป แล้วแปลงเป็นคำที่เข้าใจโดยใช้ fuction get_cond
    cond_data1 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][0]['data']['cond'])

    #ดึงข้อมูล อุณหภูมิต่ำสุด ของวันปัจจุบันและวันถัดไป หน้วยเป็นองศา
    tcmin_data1 = getdata['WeatherForecasts'][0]['forecasts'][0]['data']['tc_min']

    #ดึงข้อมูล อุณหภูมิสูงสุด ของวันปัจจุบันและวันถัดไป หน้วยเป็นองศา
    tcmax_data1 = getdata['WeatherForecasts'][0]['forecasts'][0]['data']['tc_max']

    print(response.text)

    data_return = 'วันที่ ' + day_text + '\nสภาพอากาศ : ' + cond_data1 + '\nอุณหภูมิต่ำสุด : ' + str(tcmin_data1) + ' °C\nอุณหภูมิสูงสุด : ' + str(tcmax_data1) + ' °C\n======================='
    return data_return

def day3(lat,lon):
    
    #ดึงวันที่ปัจจุบัน
    today = date.today()
    day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล
    #วันทีสำหรับใช้ในการส่งหา user
    day_text = today.strftime("%d / %m / %Y") #วันปัจจุบัน

    #วันถัดไป
    nextday = date.today() + timedelta(days=1)
    day2_text = nextday.strftime("%d / %m / %Y")

    #วันที่3
    nextday = date.today() + timedelta(days=2)
    day3_text = nextday.strftime("%d / %m / %Y")

    #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at"

    querystring = {"lat":lat, "lon":lon, "fields":"tc_min,tc_max,rain,cond", "date":day, "hour":"8", "duration":"3"}

    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + api_tmd,
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #นำข้อ
    getdata = json.loads(response.text)

    ##นำข้อมูลใน array getdata มาใช้##
    #ดึงข้อมูล สภาพอากาศทั่วไป ของวันปัจจุบันและวันถัดไป แล้วแปลงเป็นคำที่เข้าใจโดยใช้ fuction get_cond
    cond_data1 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][0]['data']['cond'])
    cond_data2 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][1]['data']['cond'])
    cond_data3 = get_cond(getdata['WeatherForecasts'][0]['forecasts'][2]['data']['cond'])

    #ดึงข้อมูล อุณหภูมิต่ำสุด ของวันปัจจุบันและวันถัดไป หน้วยเป็นองศา
    tcmin_data1 = getdata['WeatherForecasts'][0]['forecasts'][0]['data']['tc_min']
    tcmin_data2 = getdata['WeatherForecasts'][0]['forecasts'][1]['data']['tc_min']
    tcmin_data3 = getdata['WeatherForecasts'][0]['forecasts'][2]['data']['tc_min']

    #ดึงข้อมูล อุณหภูมิสูงสุด ของวันปัจจุบันและวันถัดไป หน้วยเป็นองศา
    tcmax_data1 = getdata['WeatherForecasts'][0]['forecasts'][0]['data']['tc_max']
    tcmax_data2 = getdata['WeatherForecasts'][0]['forecasts'][1]['data']['tc_max']
    tcmax_data3 = getdata['WeatherForecasts'][0]['forecasts'][2]['data']['tc_max']

    print(response.text)

    data_return = 'วันที่ ' + day_text + '\nสภาพอากาศ : ' + cond_data1 + '\nอุณหภูมิต่ำสุด : ' + str(tcmin_data1) + ' °C\nอุณหภูมิสูงสุด : ' + str(tcmax_data1) + ' °C\n======================='+'\nวันที่ ' + day2_text + '\nสภาพอากาศ : ' + cond_data2 + '\nอุณหภูมิต่ำสุด : ' + str(tcmin_data2) + ' °C\nอุณหภูมิสูงสุด : ' + str(tcmax_data2) + ' °C\n======================='+'\nวันที่ ' + day3_text + '\nสภาพอากาศ : ' + cond_data3 + '\nอุณหภูมิต่ำสุด : ' + str(tcmin_data3) + ' °C\nอุณหภูมิสูงสุด : ' + str(tcmax_data3) + ' °C\n======================='
    return data_return

def get_cond(cond):
    if cond == 1:
        return 'ท้องฟ้าแจ่มใส'
    if cond == 2:
        return 'มีเมฆบางส่วน'
    if cond == 3:
        return 'เมฆเป็นส่วนมาก'
    if cond == 4:
        return 'มีเมฆมาก'
    if cond == 5:
        return 'ฝนตกเล็กน้อย'
    if cond == 6:
        return 'ฝนปานกลาง'
    if cond == 7:
        return 'ฝนตกหนัก'
    if cond == 8:
        return 'ฝนฟ้าคะนอง'
    if cond == 9:
        return 'อากาศหนาวจัด'
    if cond == 10:
        return 'อากาศหนาว'
    if cond == 11:
        return 'อากาศเย็น'
    if cond == 12:
        return 'อากาศร้อนจัด'

if __name__ == "__main__":
    app.run()