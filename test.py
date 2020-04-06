from flask import Flask, request, abort
from commands import *

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

line_bot_api = LineBotApi('qklfwQOi7ntjZIOGtGZIvD1FThyS+INMfyII5ohIxIGIqQ7+V5HXgnQNoe5vUjv90D4bsdq1/tTY/pPhmSHw+oYE+bquGs2hokLblhX7gizOyZoEHbW0145VASKCjleebT2Lh8/x0GdezOOO02Qd4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('020171c08d903a98f7b02e07d6373173')


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
    text=event.message.text
    cmd=Command()

    if cmd.bot_cmd(0) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Fitur masih dalam pengembangan"))
    elif cmd.bot_cmd(1) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="FItur masih dalam pengembangan"))
    elif cmd.bot_cmd(2) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=cmd.help()))
    else:
        if 'ammaru-kun' in text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Ga ngerti gue. coba tulis \'?help\'"))


    """
    #Echo Response
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    """


if __name__ == "__main__":
    app.run()