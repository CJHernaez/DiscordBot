class UserHelper:
    def __init__(self):
        pass

    def getUserIdByDiscordTag(self, discordTag, userDB):
            return userDB[discordTag][0]
