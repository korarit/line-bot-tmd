from flask import Flask, request, abort, render_template, session, url_for, redirect, flash
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, CarouselColumn, MessageAction, CarouselTemplate
)

from bs4 import BeautifulSoup

import requests
import json
import pytz
import os
import pymysql

from datetime import (date, timedelta, datetime)

from slugify import slugify

app = Flask(__name__, template_folder='html')
app.static_folder = 'static'

#api line bot key
line_bot_api = LineBotApi('')
handler = WebhookHandler('')

#api key กรมอุตุนิยมวิทยา
api_tmd = ''

#Database SQL
username_sql = ""
databasename_sql = ""
password_sql = ""
server_sql = ""
port_sql = "3306"

#menu_select สำหรับใช้ในการเลือก menu
menu_select = None

#menu_select สำหรับใช้ในการเลือก function
count_data = None

#menu_select สำหรับใช้ในการเลือก function
select_function = None

#set timezone
tz = pytz.timezone('Asia/Bangkok')

@app.route("/callback", methods=['POST'])
def callback():

    #ประกาศตัวแปร menu_select , select_function , count_data เป็น global ให้ updateได้
    global menu_select
    global select_function
    global count_data

    # get request body as text
    body = request.json

    #type message form user
    types = body['events'][0]['message']['type']
    list_message_hour = [ '3_hours', '6_hours', '9_hours' ]
    list_message_day = ['1_day', '3_days', '7_days']
    list_message_news = ['1_news','2_news']

    if types == "text":

        message_text = str(body['events'][0]['message']['text'])

        if message_text == "พยากรณ์อากาศ รายชั่วโมง":
            if menu_select is None:
                menu_select = 2

                carousel_template_message = TemplateSendMessage(
                                                alt_text='Menu',
                                                template=CarouselTemplate(
                                                    columns=[
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ 3 ชั่วโมง',
                                                            text='พยากรณ์อากาศ ชั่วโมงปัจจุบัน และอีก 2ชั่วโมงถัดไป',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก 3 ชั่วโมง',
                                                                    text='3_hours'
                                                                )
                                                            ]
                                                        ),
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ 6 ชั่วโมง',
                                                            text='พยากรณ์อากาศ ชั่วโมงปัจจุบัน และอีก 5ชั่วโมงถัดไป',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก 6 ชั่วโมง',
                                                                    text='6_hours'
                                                                )
                                                            ]
                                                        ),
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ 9 ชั่วโมง',
                                                            text='พยากรณ์อากาศ ชั่วโมงปัจจุบัน และอีก 8ชั่วโมงถัดไป',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก 9 ชั่วโมง',
                                                                    text='9_hours'
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )

                line_bot_api.reply_message(body['events'][0]['replyToken'], carousel_template_message)
            else:
                menu_select = None
                select_function = None
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
        elif message_text == "พยากรณ์อากาศ รายวัน":
            if menu_select is None:
                menu_select = 2

                carousel_template_message = TemplateSendMessage(
                                                alt_text='Menu',
                                                template=CarouselTemplate(
                                                    columns=[
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ วันนี้',
                                                            text='พยากรณ์อากาศ วันนี้',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก วันนี้',
                                                                    text='1_day'
                                                                )
                                                            ]
                                                        ),
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ 3 วัน',
                                                            text='พยากรณ์อากาศ วันนี้ และอีก 2 วันถัดไป',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก 3 วัน',
                                                                    text='3_days'
                                                                )
                                                            ]
                                                        ),
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศ 7 วัน',
                                                            text='พยากรณ์อากาศ วันนี้ และอีก 6 วันถัดไป',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก 7 วัน',
                                                                    text='7_days'
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )

                line_bot_api.reply_message(body['events'][0]['replyToken'], carousel_template_message)
            else:
                menu_select = None
                select_function = None
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))

        elif message_text == "ข่าวสภาพอากาศ":
            if menu_select is None:
                menu_select = 2

                carousel_template_message = TemplateSendMessage(
                                                alt_text='Menu',
                                                template=CarouselTemplate(
                                                    columns=[
                                                        CarouselColumn(
                                                            title='พยากรณ์อากาศประจำวัน	',
                                                            text='Infographic พยากรณ์อากาศประจำวัน จากกรมอุตุนิยมวิทยา',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก',
                                                                    text='1_news'
                                                                )
                                                            ]
                                                        ),
                                                        CarouselColumn(
                                                            title='เตือนภัยพื้นที่เสียงภัยฝนหนัก',
                                                            text='Infographic เตือนภัยพื้นที่เสียงภัยฝนหนัก จากกรมอุตุนิยมวิทยา',
                                                            actions=[
                                                                MessageAction(
                                                                    label='เลือก',
                                                                    text='2_news'
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )

                line_bot_api.reply_message(body['events'][0]['replyToken'], carousel_template_message)
            else:
                menu_select = None
                select_function = None
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
                    
        elif message_text == "ติดต่อผู้พัฒนา":
            if menu_select is None:
                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='====== Facebook ======\n\nhttps://www.facebook.com/krt.korarit\n\n====== Youtube =======\n\nhttps://www.youtube.com/channel/UC3ZDblNrSZRnJe_-0Zv52QA\n\n====== Github ========\n\nhttps://github.com/korarit'))
            else:
                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
        elif message_text in list_message_hour:
            if menu_select == 2:
                get_count = message_text.split("_")
                count_data = int(get_count[0]) - 1

                select_function = 'hours'
                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาแชร์ location'))
                menu_select = None
            else:
                select_function = None
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
        elif message_text in list_message_day:
            if menu_select == 2:
                get_count = message_text.split("_")
                count_data = int(get_count[0]) - 1

                select_function = 'day'
                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาแชร์ location'))
                menu_select = None
            else:
                select_function = None
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
        elif message_text in list_message_news:
            if menu_select == 2:

                menu_select = None
                #ดึงวันที่ปัจจุบัน
                today = date.today()
                day = str(today.strftime("%Y-%m-%d")) #วันทีสำหรับใช้ในการดึงข้อมูล

                get_count = message_text.split("_")
                count_datas = int(get_count[0])

                conn = pymysql.connect(host=server_sql, user=username_sql, password=password_sql, database=databasename_sql)
                cur = conn.cursor()
                sql = "SELECT link FROM news Where date=%s and type=%s"
                cur.execute(sql, (day, count_datas))

                result = cur.fetchone()

                print(result)
                conn.close()

                line_bot_api.reply_message(body['events'][0]['replyToken'], ImageSendMessage(original_content_url=result[0], preview_image_url=result[0]))

            else:
                count_data = None

                line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือกใหม่อีกครั้ง'))
        else:
            line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='ไม่สามารถพิมพ์ข้อความเพื่อคุยกับ บอทได้ในขณะนี้'))
    elif types == "location":

        if select_function is not None:

            if select_function == "hours":

                lat = body['events'][0]['message']['latitude']

                lon = body['events'][0]['message']['longitude']

                txtresult = get_hour(lat,lon,count_data)

                replyObj = TextSendMessage(text=txtresult)

                line_bot_api.reply_message(body['events'][0]['replyToken'], replyObj)

                print(str(lat) +" , "+ str(lon))

                menu_select = None
                select_function = None
                count_data = None

            elif select_function == "day":

                lat = body['events'][0]['message']['latitude']

                lon = body['events'][0]['message']['longitude']

                txtresult = get_day(lat,lon,count_data)

                replyObj = TextSendMessage(text=txtresult)

                line_bot_api.reply_message(body['events'][0]['replyToken'], replyObj)

                menu_select = None
                select_function = None
                count_data = None

        else:

            line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาเลือก menu ใหม่อีกครั้ง'))

            menu_select = None
            select_function = None
            count_data = None
    else:

        line_bot_api.reply_message(body['events'][0]['replyToken'], TextSendMessage(text='กรุณาส่งเป็น location และกรุณาเลือก menu ใหม่อีกครั้ง!'))

        menu_select = None
        select_function = None
        count_data = None

    return ''


def get_hour(lat,lon,hour):

        #ดึงวันที่ปัจจุบัน
        today = date.today()

        day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล

        #ดึงชั่วโมงปัจจุบัน
        hour_now = datetime.now().astimezone(tz)
        hournow_text = hour_now.strftime("%H")

        #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา

        url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"


        querystring = {"lat":lat, "lon":lon, "fields":"tc,rain,cond", "date":day, "hour":hournow_text, "duration":"9"}


        headers = {

            'accept': "application/json",

            'authorization': "Bearer " + api_tmd,

        }


        response = requests.request("GET", url, headers=headers, params=querystring)


        #นำข้อมูลมาใช้
        getdata = json.loads(response.text)

        print(response.text)

        i = 0
        data_return = ''
        while i <= hour:
            #ดึงชั่วโมงถัดไป
            next_time = datetime.now().astimezone(tz) + timedelta(hours=i)
            time_text = next_time.strftime("%H:%M:%S")

            ##นำข้อมูลใน array getdata มาใช้##
            #ดึงข้อมูล สภาพอากาศทั่วไป
            cond_time = get_cond(getdata['WeatherForecasts'][0]['forecasts'][i]['data']['cond'])

            #ดึงข้อมูล อุณหภูมิ 
            tc_time = getdata['WeatherForecasts'][0]['forecasts'][i]['data']['tc']

            #ดึงข้อมูล ฝนสะสม 
            rain_time = getdata['WeatherForecasts'][0]['forecasts'][i]['data']['rain']

            data_returns = 'เวลา {0}น. \nสภาพอากาศ : {1} \nอุณหภูมิ : {2}  °C\nปริมาณฝนสะสม : {3}  mm\n=======================\n'.format(time_text, cond_time, tc_time, rain_time)
            data_return = data_return + data_returns

            i = i + 1
        return data_return

def get_day(lat,lon,day_count):
    
    #ดึงวันที่ปัจจุบัน

    today = date.today()

    day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล

    #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา

    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at"


    querystring = {"lat":lat, "lon":lon, "fields":"tc_min,tc_max,rain,cond", "date":day, "hour":"8", "duration":"8"}


    headers = {

        'accept': "application/json",

        'authorization': "Bearer " + api_tmd,

    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #นำข้อมูลมาเป็น array
    getdata = json.loads(response.text)

    print(response.text)

    i = 0
    data_return = ''
    while i <= day_count:
        #วันที่
        next_day = date.today() + timedelta(days=i)
        day_text = next_day.strftime("%d / %m / %Y")

        ##นำข้อมูลใน array getdata มาใช้##
        #ดึงข้อมูล สภาพอากาศทั่วไป
        cond_time = get_cond(getdata['WeatherForecasts'][0]['forecasts'][i]['data']['cond'])

        #ดึงข้อมูล อุณหภูมิ 
        tcmin_data = getdata['WeatherForecasts'][0]['forecasts'][i]['data']['tc_min']

        tcmax_data = getdata['WeatherForecasts'][0]['forecasts'][i]['data']['tc_max']

        #ดึงข้อมูล ฝนสะสม
        rain_data = getdata['WeatherForecasts'][0]['forecasts'][i]['data']['rain']

        data_returns = 'วันที่ {0} \nสภาพอากาศ : {1} \nอุณหภูมิต่ำสุด : {2}  °C\nอุณหภูมิสูงสุด : {3}  °C\nปริมาณฝนสะสม : {4} mm\n=======================\n'.format(day_text, cond_time, tcmin_data, tcmax_data, rain_data)
        data_return = data_return + data_returns

        i = i + 1
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

@app.route("/")
def index():

    #ดึงวันที่ปัจจุบัน
    today = date.today()

    day = str(today.strftime("%Y%m%d")) #วันทีสำหรับใช้ในการดึงข้อมูล

    insight = line_bot_api.get_insight_followers(day)
    return render_template('index.html', follower=insight.followers)

@app.route("/login")
def loginform():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username ='test'
    password = 'test'
    user_login = request.form.get('username')
    pass_login = request.form.get('password')
    if user_login == username and pass_login == password:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', alerts=1)

@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')

@app.route('/dashboard', methods=['POST'])
def dashboard_text():
    text_broadcast = request.form.get('text_forbroadcast')
    image_broadcast = request.form.get('image_forbroadcast')
    if text_broadcast != '':
        line_bot_api.broadcast(TextSendMessage(text=text_broadcast))
        return render_template('dashboard.html', alerts=1)
    else:
        return render_template('dashboard.html', alerts=2)

@app.route('/hour', methods=['GET'])
def hour_graphic():

    #get post data
    lat = str(request.args.get('lat'))
    lon = str(request.args.get('lon'))
    hour = int(request.args.get('hours'))

    #ดึงวันที่ปัจจุบัน
    today = date.today()

    day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล

    #ดึงชั่วโมงปัจจุบัน
    hour_now = datetime.now().astimezone(tz)
    hournow_text = hour_now.strftime("%H")

    #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"

    querystring = {"lat":lat, "lon":lon, "fields":"tc,rain,cond,rh", "date":day, "hour":hournow_text, "duration":hour}

    headers = {

        'accept': "application/json",

        'authorization': "Bearer " + api_tmd,

    }

    response = requests.request("GET", url, headers=headers, params=querystring)


    #นำข้อมูลมาใช้
    getdata = json.loads(response.text)

    print(response.text)

    i = 0
    date_list = []
    get_hour_data = getdata['WeatherForecasts'][0]['forecasts']
    hourss = int(hour - 1)
    while i <= hour:
        #ดึงชั่วโมงถัดไป
        next_time = datetime.now().astimezone(tz) + timedelta(hours=i)
        time_text = next_time.strftime("%H:00:00")
        date_list.append(time_text)

        i = i + 1

    cond_list = []
    s = 0
    while s <= hourss:
        get_text_cond = getdata['WeatherForecasts'][0]['forecasts'][s]['data']['cond']
        get_text = get_cond(get_text_cond)
        cond_list.append(get_text)
        
        s = s + 1
    
    print(cond_list)
    print(date_list)
    
    return render_template('hour.html', data_row=get_hour_data, date=date_list, conds=cond_list, hours=hour)

@app.route('/day', methods=['GET'])
def day_graphic():

    #get post data
    lat = str(request.args.get('lat'))
    lon = str(request.args.get('lon'))
    days = int(request.args.get('days'))

    #ดึงวันที่ปัจจุบัน
    today = date.today()

    day = today.strftime("%Y-%m-%d") #วันทีสำหรับใช้ในการดึงข้อมูล

    #ดึงชั่วโมงปัจจุบัน
    hour_now = datetime.now().astimezone(tz)
    hournow_text = hour_now.strftime("%H")

    #ดึงข้อมูลจาก api กรมอุตุนิยมวิทยา
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at"

    querystring = {"lat":lat, "lon":lon, "fields":"tc_min,tc_max,rain,cond,rh", "date":day, "hour":hournow_text, "duration":days}

    headers = {

        'accept': "application/json",

        'authorization': "Bearer " + api_tmd,

    }

    response = requests.request("GET", url, headers=headers, params=querystring)


    #นำข้อมูลมาใช้
    getdata = json.loads(response.text)

    print(response.text)

    i = 0
    date_list = []
    get_day_data = getdata['WeatherForecasts'][0]['forecasts']
    dayss = int(days - 1)
    while i <= days:
        #ดึงชั่วโมงถัดไป
        next_day = date.today() + timedelta(days=i)
        day_text = next_day.strftime("%d/%m/%Y")
        date_list.append(day_text)

        i = i + 1

    cond_list = []
    s = 0
    while s <= dayss:
        get_text_cond = getdata['WeatherForecasts'][0]['forecasts'][s]['data']['cond']
        get_text = get_cond(get_text_cond)
        cond_list.append(get_text)
        
        s = s + 1
    
    print(cond_list)
    print(date_list)
    
    return render_template('day.html', data_row=get_day_data, date=date_list, conds=cond_list, day=days)

@app.route("/webscraping")
def web_scraping():

    #ดึงวันที่ปัจจุบัน
    today = date.today()
    day = str(today.strftime("%Y-%m-%d")) #วันทีสำหรับใช้ในการดึงข้อมูล

    url = "https://www.tmd.go.th/index.php"
    res = requests.get(url)
    res.encoding = "utf-8"

    #ทำเว็ป scraping
    soup = BeautifulSoup(res.text, 'html.parser')
    courses = soup.find_all(width='130')

    course_list = []

    for course in courses:
        obj = course.get('src')

        course_list.append(obj)

    image_link1 = str(course_list[1])
    image_link2 = str(course_list[2])

    link_text1 = image_link1.replace('./', "https://www.tmd.go.th/")
    link_text2 = image_link2.replace('./', "https://www.tmd.go.th/")

    url1 = slugify(link_text1)
    url2 = slugify(link_text2)

    link_url1 = url1.replace('https-www-tmd-go-th-programs-uploads-forecast-resized-', "https://www.tmd.go.th/programs/uploads/forecast/")
    getlink_url1 = link_url1.replace("-dfth1-", "_DFTH1_")
    change_link1 = getlink_url1.replace("-jpg", ".jpg")

    link_url2 = url2.replace('https-www-tmd-go-th-programs-uploads-forecast-resized-', "https://www.tmd.go.th/programs/uploads/forecast/")
    getlink_url2 = link_url2.replace("-dfth2-", "_DFTH2_")
    change_link2 = getlink_url2.replace("-jpg", ".jpg")

    conn = pymysql.connect(host=server_sql, user=username_sql, password=password_sql, database=databasename_sql)
    cur = conn.cursor()

    sql_check = "SELECT link From news where date=%s "
    cur.execute(sql_check, (day))
    result = cur.rowcount

    if result > 1:
        sql = "UPDATE news SET link=%s where date=%s and type=%s"
        cur.execute(sql, (change_link1, day, 1))
        cur.execute(sql, (change_link2, day, 2))
        conn.commit()
    else:
        sql = "INSERT INTO news (link, date, type) VALUES (%s, %s,%s)"
        cur.execute(sql, (change_link1, day, 1))
        cur.execute(sql, (change_link2, day, 2))
        conn.commit()
    conn.close()
    return "finish"

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
