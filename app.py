from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from commands import *

"""
Set up for developmet/production phase. Change the URI of the database according to your own needs
"""

app = Flask(__name__)
ENV='dev'

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sixsome1598Edu@localhost/ammaru-kun-chatbot'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sixsome1598Edu@localhost/ammaru-kun-chatbot'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
"""
Create the model for your database. In this chatbot, I use database to store ?tugas information
"""
#Model for the database
db=SQLAlchemy(app)

class Tugas(db.Model):
    __tablename__='tugas'
    id=db.Column(db.Integer, primary_key=True)
    grup=db.Column(db.String(32))
    nama=db.Column(db.String(50),default='???')
    deadline=db.Column(db.String(50),default='???')
    pengumpulan=db.Column(db.String(50),default='???')

    def __init__(self, grup, nama, deadline, pengumpulan):
        self.grup=grup
        self.nama = nama
        self.deadline = deadline
        self.pengumpulan = pengumpulan


"""
Set up for LINE Chatbot settings, Channel Secret, Channel Access, and set up the handler
"""
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('qklfwQOi7ntjZIOGtGZIvD1FThyS+INMfyII5ohIxIGIqQ7+V5HXgnQNoe5vUjv90D4bsdq1/tTY/pPhmSHw+oYE+bquGs2hokLblhX7gizOyZoEHbW0145VASKCjleebT2Lh8/x0GdezOOO02Qd4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('020171c08d903a98f7b02e07d6373173')

"""
Create app route for /callback. It requests LINE to get X-LINE-Signature header valuem and check the validity of channel access token/channel secret
"""
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

"""
Add handler for dealing with text messages input
"""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text
    cmd=Command()

    #If the input is '?meme'
    if cmd.bot_cmd(0) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Fitur masih dalam pengembangan"))
    #If the input is '?youtubemp3'
    elif cmd.bot_cmd(1) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="FItur masih dalam pengembangan"))
    #If the input is '?help'
    elif cmd.bot_cmd(2) in text.split(' ')[0]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=cmd.help()))
    #If the input is '?tugas {nama-tugas} {deadline-tugas} {link-pengumpulan}
    elif cmd.bot_cmd(3) in text.split(' ')[0]:
        pass
    #If the input don't follow any commands set before
    else:
    #If 'ammaru-kun' found in the text
        if 'ammaru-kun' in text.lower():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Ga ngerti gue. coba tulis \'?help\'"))


    """
    #Echo Response
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    """

"""
Run the app if the code is executed as the main program
"""

if __name__ == "__main__":
    app.run()