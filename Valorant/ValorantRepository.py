import sqlite3


class ValorantRepository:
    def __init__(self, valarantDB, connection):
        self.datasource = valarantDB
        self.conn = connection


    def refresh(self):
        dict = {}
        cur = self.conn.cursor()

        try:
            cur.execute("SELECT * FROM VALORANT")
        except sqlite3.OperationalError as e:
            return e

        rows = cur.fetchall()

        for row in rows:
            dict[row[0]] = row[1]

        self.datasource = dict

        return dict

    def add(self, discordName, discordId, nickname): #fix this later
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

