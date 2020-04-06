class Command:
    def __init__(self):
        self.commands=\
            [
                "?meme",
                "?youtubemp3",
                "?help"
            ]

        self.help_info="\
            Halo, aku Ammaru-kun!\n\
            \n[Daftar Perintah]\
            \n[1]. ?meme\
            \n[2]. ?youtubemp3\
            \n[3]. ?help"

    def bot_cmd(self,selected):
        return self.commands[selected]

    def help(self):
        return self.help_info