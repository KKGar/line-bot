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

app = Flask(__name__)

line_bot_api = LineBotApi('7xlI9YiBctP0bY0WzfUUv125GbtZE+CXEAPBdWX0vjQbD3xdbNuATow8gzZA+ge97T8mIgrjwZ+iCq8IcM8UBBQUKcWLAX9ZdVwTokuert2TVPwDhQWAur4e/aFJJIy8zJtOEgDxBtr4WfFfxdAbHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('698e30a39d4840113ce45797b0d2d8b1')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '熊熊看不懂你說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return 

    if msg == ['hi', 'Hi']:
        r = 'hi'
    elif msg == '熊熊':
        r = '熊熊說你好'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()