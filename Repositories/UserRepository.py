import sqlite3


class UserRepository:
    def __init__(self, userDB, connection):
        self.datasource = userDB
        self.conn = connection


    def refresh(self):
        dict = {}
        cur = self.conn.cursor()

        try:
            cur.execute("SELECT * FROM USERS")
        except sqlite3.OperationalError as e:
            return e

        rows = cur.fetchall()

        for row in rows:
            dict[str(row[1]) + '#' + str(row[2])] = (row[0], row[1], row[2], row[3])

        self.datasource = dict

        return dict

    def getDiscordTagByNickname(self, nicknameToMatch):
            for (id, name, discId, nickname) in self.datasource.values():
                if nickname.lower() == nicknameToMatch.lower():
                    return name+'#'+ str(discId)
            return 'Nickname ' + nicknameToMatch  + ' Not Found'


    def getUserIdByDiscordTag(self, discordTag):
        tokenizedTag = discordTag.split('#')
        for (id, name, discId, nickname) in self.datasource.values():
            if name.lower() == tokenizedTag[0].lower() and discId == int(tokenizedTag[1]):
                return id
        return 'Discord Tag' + discordTag + ' Not Found'

    def getUserIdByNickname(self, nicknameToMatch):
        for (id, name, discId, nickname) in self.datasource.values():
            if nickname.lower() == nicknameToMatch.lower():
                return id
        return 'Nickname ' + nicknameToMatch + ' Not Found'


    def add(self, discordName, discordId, nickname):
        cur = self.conn.cursor()

        userToAdd = discordName + '#' + str(discordId) + ' : ' + discordName
        statement = """INSERT INTO USERS( USERNAME, DISCORD_ID, COMMON_NAME) 
                                              VALUES 
                                             (?, ?, ?)
                                             """
        dataTuple = (discordName, discordId, nickname)

        try:

            cur.execute(statement,dataTuple)
            self.conn.commit()
        except:
            return 'Failed to add user:' + userToAdd

        print("User" + userToAdd + ' added. id: ' + str(cur.lastrowid))
        self.datasource[discordName + '#' + str(discordId)] = (cur.lastrowid, discordName, discordId, nickname)
        return userToAdd + ' added'

    def deleteUserByDiscordTag(self, discordTag):
        cur = self.conn.cursor()

        tokenizedTag = discordTag.split('#')
        sql = """DELETE FROM USERS WHERE USERNAME = ? AND DISCORD_ID = ?"""

        try:

            cur.execute(sql,(tokenizedTag[0], int(tokenizedTag[1])))
            self.conn.commit()
        except:
            return 'Failed to delete user:' + discordTag

        print("User" + discordTag + ' deleted. id: ' + str(cur.lastrowid))
        del self.datasource[discordTag]
        return discordTag + ' deleted'