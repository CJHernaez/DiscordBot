
class MessageHelper:
        def __init__(self, users):
            self.conn = users


        def getDiscordTagByMessage(self, message):
            #generate the full discord name
            return message.author.name + '#' + message.author.discriminator
