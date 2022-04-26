# line-bot-tmd
### line bot รายงานสภาพอากาศ ผ่าน การส่ง location ให้บอท โดยใช้ข้อมูลจาก api ของกรมอุตุนิยมวิทยา

ความสามารถของระบบ (Fuction)
* ใช้ location ในการค้นหาข้อมูล
  * พยากรณ์อากาศ 3ชั่วโมง
  * พยากรณ์อากาศ วันนี้
  * พยากรณ์อากาศ 3วัน
  * ส่งข้อความ link ติดต่อผู้พัฒนา

## requestment ของตัวระบบ
* flask
* line-bot-sdk
* requests
* json
* datetime

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

## Preview
![Image](https://i.imgur.com/shRM4s2.png)

## ทดสอบ ระบบได้ที่ Line: รายงานสภาพอากาศ (Test line bot account)
ID สำหรับแอดไลน์บอท (ID line add friend bot)

> @911xspfk

QRCODE ADD ไลน์ (QRCODE line add friend bot)

![Image](https://qr-official.line.me/sid/L/911xspfk.png)
