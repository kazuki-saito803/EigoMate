import os
import logging
import requests
import azure.functions as func
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
FAST_URL = os.getenv('FAST_URL')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route(route="eigomatefunc")
def http_trigger_line(req: func.HttpRequest) -> func.HttpResponse:
    signature = req.headers.get('X-Line-Signature')
    body = req.get_body().decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature")
        return func.HttpResponse("Invalid signature", status_code=400)

    return func.HttpResponse('OK', status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    api_message = requests.get(FAST_URL)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{api_message}Hello world')
    )