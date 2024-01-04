# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('6BHlbOR673DiFlcS3JhClIBBZ3QmB8UT2skmk00loO2pzdi+BMVVCnDqLe7GaOEbqVFtoAd1ZU5AW+BhiTqlwI5U5QJzGS2LuBd3vWuMQrf1MHE86jWf1075E+EM47uwlziD7JnYDkn1pQ617axphwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2e0a240a4422579dde659987460cccc7')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('購買商品',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這是樣板傳送訊息',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/ZHf1apg.jpg',
            title='寵物用品公司',
            text='選單功能',
            actions=[
                URIAction(
                    label='官方網站',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/'
                ),
                URIAction(
                    label='狗狗產品',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/%e7%8b%97%e7%8b%97%e7%94%a2%e5%93%81/'
                ),
                URIAction(
                    label='貓咪產品',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/%e8%b2%93%e5%92%aa%e7%94%a2%e5%93%81/'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif re.match('線上客服',message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請稍等，以幫您聯絡客服人員。'))
    elif re.match('店家資訊',message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='寵物用品專賣門市\n台中市沙鹿區台灣大道七段200號, 433 台中市\n\n電話號碼\n04-26328001\n\n電子郵件\ns1091935@gm.pu.edu.tw\n\n服務時間\n星期一 ~ 星期五： 8:00 - 18:00\n假日：不營業\n特殊節日：另公告之'))
    elif re.match('詢問指令',message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='本機器人擁有以下指令:\n---------------------------------------\n購買商品\n線上客服\n店家資訊\n詢問指令'))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
