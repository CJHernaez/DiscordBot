import sqlite3

class ValarantHelper:
        def __init__(self, conn):
            self.conn = conn

        def getMemeByMessage(self, message, users):
            pass # get the name

        def getAllValarant(self, valarantDB):
            stringbuilder = ''
            for userID, meme in valarantDB.items():
                stringbuilder = stringbuilder + str(userID) + ' : ' + meme

            return stringbuilder

        def getMemeByDiscordTag(self, discordTag, valarantDB):
            return valarantDB[discordTag]

        def getMemeByUserId(self, userId, valarantDB):
            return valarantDB[userId]

        def refreshValarants(self):
            dict = {}
            cur = self.conn.cursor()

            try:
                cur.execute("SELECT * FROM VALARANT")
            except sqlite3.OperationalError as e:
                return e

            rows = cur.fetchall()

            for row in rows:
                dict[row[0]] = row[1]

            return dict