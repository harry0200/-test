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
line_bot_api = LineBotApi('JpVMfpzpD+Stu3nfpfB8bWKcsmkCqasZa5rPaYgaQzGP17NqllQM6emvpBm5vHCIyag9ZcC2TIP9sqdUr0ZAMGJNuV/ccL21b79pgTdg7oEQuWzrj4rEkc78jASuSpAZT74uBKzN7ZDvKGInWTVXAgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ca5327b5c7ba783d20a3c85738bfd1a4')

line_bot_api.push_message('U262565b00a73c456ebba11b0bd1e7762', TextSendMessage(text='你可以開始了'))

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
    if re.match('更多資訊',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這是樣板傳送訊息',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/bY07QAW.png',
            title='寵物用品公司',
            text='選單功能',
            actions=[
                PostbackAction(
                    label='官方網站',
                    display_text = '顯示文字',
                    data= '詳細資料',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/'
                ),
                MessageAction(
                    label='購買狗狗商品',
                    text= '實際資料',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/%e7%8b%97%e7%8b%97%e7%94%a2%e5%93%81/'
                ),
                URIAction(
                    label='購買貓咪商品',
                    uri='https://chongwuyongpinzhuanmai.webnode.tw/%e8%b2%93%e5%92%aa%e7%94%a2%e5%93%81/'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
