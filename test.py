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

line_bot_api = LineBotApi('qklfwQOi7ntjZIOGtGZIvD1FThyS+INMfyII5ohIxIGIqQ7+V5HXgnQNoe5vUjv90D4bsdq1/tTY/pPhmSHw+oYE+bquGs2hokLblhX7gizOyZoEHbW0145VASKCjleebT2Lh8/x0GdezOOO02Qd4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('020171c08d903a98f7b02e07d6373173')

tugas={}


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
    text = event.message.text

    #Text preprocessing
    splitted_text=text.split(' ')

    if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
        #Code for all conversations if bot called in group.
        if text.startswith('?tugas '):
            if text=='?tugas info':
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text='?tugas adalah fitur yang membantu untuk pencatatan tugas-tugas anggota grup.'),
                        TextSendMessage(text='Gunakan \'?tugas info\' untuk informasi mengenai fitur ini.'),
                        TextSendMessage(text='Gunakan \'?tugas add {nama tugas} {deadline dalam format YYYY/MM/DD HH:MM:SS} {informasi pengumpulan}\' untuk menambahkan tugas'),
                        TextSendMessage(text='Gunakan \'?tugas list\' untuk menampilkan seluruh tugas yang telah tersimpan.'),
                        TextSendMessage(text='Gunakan \'?tugas remove {nomor tugas}\' untuk menghapus tugas pada nomor tersebut'),
                        TextSendMessage(text='Gunakan \'?tugas clear\' untuk menghapus seluruh informasi tugas yang tersimpan'),
                        TextSendMessage(text='Gunakan \'?tugas reminder {on/off}\' untuk menyalakan/mematikan fitur reminder tugas.'),
                        TextSendMessage(text='Selamat nugas, semuanya!')     
                    ]
                )
            elif splitted_text[0:1]==['?tugas','add']:
                if len(splitted_text)>6:
                    line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text='Kirim yang sesuai format, dong. Cek di \'?tugas info\'')
                    )
                    break
                nama_temp=splitted_text[2]
                tanggal_temp=splitted_text[3]
                jam_temp=splitted_text[4]
                info_temp=splitted_text[5]
                if list(tugas.keys()).count(event.source.group_id)==0:
                    tugas[event.source.group_id]=[[nama_temp,tanggal_temp,jam_temp,info_temp]]
                else:
                    tugas[event.source.group_id].append([nama_temp,tanggal_temp,jam_temp,info_temp])
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Informasi tugas %s sudah disimpan.'%(nama_temp))
                )
            elif text=='?tugas list':
                if list(tugas.keys()).count(event.source.group_id)==0:
                    line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text='Belum ada informasi tugas apa pun yang tersimpan.')
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        [TextSendMessage(text='%d. tugas %s, deadline %s %s, dikumpulkan di %s'%(i+1,l[0],l[1],l[2],l[4])) for i,l in enumerate(tugas[event.source.group_id])]
                    )
            elif splitted_text[0:1]==['?tugas','remove']:
                if len(splitted_text)>3:
                    line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text='Kirim yang sesuai format, dong. Cek di \'?tugas info\'')
                    )
                    break
                indexremove=int(splitted_text[2])-1
                del tugas[event.source.group_id][indexremove]
                line_bot_api.reply_message(
                    event.rely_token, TextSendMessage(text='Informasi tugas ke-%s sudah dihapus.'%(splitted_text[2]))
                )
            elif text=='?tugas clear':
                del tugas[event.source.group_id]
            elif splitted_text[0:1]==['?tugas','reminder']:
                #Input code for reminder here
            else:
                line_bot_api.reply_message(
                    event.reply_token,[
                        TextSendMessage(text='Maaf, aku ga ngerti apa yang kamu mau.'),
                        TextSendMessage(text='Coba tulis \'?tugas info\'')
                    ]
                )


        elif text.startswith('?jurnal'):
            #Nyari informasi tentang jurnal
            pass

        elif text=='cabut lu mar':
            if isinstance(event.source, SourceGroup):
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text='Oke. Dadah semuanya!'),
                        TextSendMessage(text='Jangan kangen ya.')
                        ]
                    )
                line_bot_api.leave_group(event.source.group_id)
            elif isinstance(event.source, SourceRoom):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Oke. Dadah semuanya!'))
                line_bot_api.leave_room(event.source.room_id)
    else:
        #Code for all conversations in 1:1 convo
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Hahaha."))


if __name__ == "__main__":
    app.run()