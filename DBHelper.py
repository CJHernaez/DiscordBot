import sqlite3

class DBHelper:
        def __init__(self, conn):
            self.conn = conn

        def getAll(self, table):
            if table == '':
                return 'Must include table name'
            cur = self.conn.cursor()

            try:
                cur.execute("SELECT * FROM " + table.upper())
            except sqlite3.OperationalError as e:
                return e

            rows = cur.fetchall()

            for row in rows:
                print(row)

            messageBuilder = ''
            for row in rows:
                messageBuilder = messageBuilder + str(row) + '\n'

            return messageBuilder

        def addUser(self, discordTag, nickname):
            splitTag = discordTag.split('#')
            cur = self.conn.cursor()
            try:
                cur.execute("""INSERT INTO USERS
                                                 ( USERNAME, DISCORD_ID, COMMON_NAME) 
                                                  VALUES 
                                                 ({0}, {1}, {2})
                                                 """.format(splitTag[0],splitTag[2],nickname))
                print("DB with new values generated.")
            except:
                return 'Failed to add user:' + str(splitTag[0])

            self.conn.commit()

        def refreshUsers(self):
            dict = {}
            cur = self.conn.cursor()

            try:
                cur.execute("SELECT * FROM USERS")
            except sqlite3.OperationalError as e:
                return e

            rows = cur.fetchall()

            for row in rows:
                dict[str(row[1]) + '#' + str(row[2])] = (row[0], row[1], row[2], row[3])

            return dict


        def getUsers (self, users):
            stringbuilder = ''
            for discordTag, (userID, name, discordId, nickname) in users.items():
                stringbuilder = stringbuilder + str(userID) + ' : ' + name + ' : ' + str(discordId) + ' : ' + discordTag + '\n'

            return stringbuilder