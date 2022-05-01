# line-bot-tmd V2.0 (Develop Processing)
### line bot รายงานสภาพอากาศ ผ่าน การส่ง location ให้บอท โดยใช้ข้อมูลจาก api ของกรมอุตุนิยมวิทยา V.2



ความสามารถของระบบ line bot (Function)
* ใช้ location ในการค้นหาข้อมูล , ใช้ ข้อมูลจาก longdomap เป็นข้อความ
  * พยากรณ์อากาศ รายชั่วโมง เลือกได้ 3ชั่วโมง 6ชั่วโมง 9ชั่วโมง
    * เป็นภาพ infographic (html to image)
  * พยากรณ์อากาศ รายวัน เลือกได้ 1วัน 3วัน 7วัน
    * เป็นภาพ infographic (html to image)
  * ข่าวการพยากรณ์อากาศจากกรมอุตุนืยมวืทยา
    * เป็นภาพ infographic (html to image)

ความสามารถของระบบจัดการ (bankend Function)
* line bot control web
  * broadcast function
  * disble bot
  * change image in menu
* data 
  * เก็บข้อมูลการ requset รายวัน รายอาทิตย์ รายเดือน
* security
  * discord log

## requestment library ของตัวระบบ line bot
* flask
* line-bot-sdk
* requests
* json
* datetime
* pytz
* pyimgur

## programming language
backend
* Python 3.10

fontend
* html
* bootstrap

## line api
> line_bot_api = LineBotApi('Channel_access_token')
> 
> handler = WebhookHandler('Channel_secret')

Channel_access_token หาได้จากหน้า Messaging API ใน developers.line.biz (get form page Messaging API in developers.line.biz)

Channel_secret หาได้จากหน้า Basic setting ใน developers.line.biz (get form page Basic setting in developers.line.biz)


rich menu ทำใน ตัวเว็บ developers.line.biz (make rich menu form developers.line.biz)

## tmd api
> api_tmd = 'api_key'

api key หาได้จาก https://data.tmd.go.th/nwpapi/register เมื่อสมัครจะได้รับ Personal Access Tokens

## Develop Processing
