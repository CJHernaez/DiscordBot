import sqlite3

from Valorant.ValorantRepository import ValorantRepository


class ValorantHelper:
        def __init__(self, valorantDB, connection):
            self.valorantRepository = ValorantRepository(valorantDB, connection)

        def setUserHelper(self, userHelper):
            self.userHelper = userHelper

        def setMessageHelper(self, messageHelper):
            self.messageHelper = messageHelper

        def Handle(self, message):
            tokenizedMessage = message.content.split(' ')
            if (len(tokenizedMessage) == 1): # text is exactly valarant
                discordTag = self.messageHelper.getDiscordTagByMessage(message)
                userID = self.userHelper.getUserIdByDiscordTag(discordTag)
                return message.channel.send(self.getMemeByUserId(userID)) # return the meme associated to the message
            if tokenizedMessage[1].lower() == 'updatememe':
                self.valorantRepository.updateMeme()

        def getMemeByMessage(self, message):
            discordTag = self.messageHelper.getDiscordTagByMessage(message)
            return self.getMemeByDiscordTag(discordTag)
            pass # get the name

        def getAllValarant(self, valarantDB):
            stringbuilder = ''
            for userID, meme in valarantDB.items():
                stringbuilder = stringbuilder + str(userID) + ' : ' + meme

            return stringbuilder

        def getUserIdByMessage(self, message):
            pass

        def getMemeByDiscordTag(self, discordTag):
            return self.valorantRepository.datasource[self.userHelper.getUserIdByDiscordTag(discordTag)]

        def getMemeByUserId(self, userId):
            return self.valorantRepository.datasource[userId]

        def refresh(self):
            return self.valorantRepository.refresh()