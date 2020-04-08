class Command:
    def __init__(self):
        self.commands=\
            [
                "?meme",
                "?youtubemp3",
                "?help",
                "?tugas"
            ]

        self.help_info="Halo, semuanya! Aku Ammaru-kun, chatbot eksploratif yang dibuat oleh Ammar!\n\
            \nAku masih bodoh sih, jadi hanya bisa menerima perintah yang jelas saja. Nih, beberapa hal yang bisa kulakukan:\n\
            \n1. ?meme\
            \n2. ?youtubemp3\
            \n3. ?tugas {nama-tugas} {deadline-tugas} {link-pengumpulan}\
            \n4. ?help\n\
            \nSelamat bersenang-senang!"

    def bot_cmd(self,selected):
        return self.commands[selected]

    def help(self):
        return self.help_info