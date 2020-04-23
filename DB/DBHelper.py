import logging
import sqlite3
from os import path

def GenerateDB():
    if not path.exists("discordBotDB.db"):
        print("DB not found. Generating new DB")
        conn = sqlite3.connect('discordBotDB.db') # generate the db.
        cursor = conn.cursor()
        # Create table - USERS
        cursor.execute('''CREATE TABLE USERS
                     ([ID] INTEGER PRIMARY KEY AUTOINCREMENT,[USERNAME] text, [DISCORD_ID] integer, [COMMON_NAME] text unique)''')


        examples = [('procrastinise', 2594, 'Jarren'),
                    ('Prophecies', 9660, 'CJ'),
                    ('AirWick', 9172, 'EJ'),
                    ('A$tros10th', 6646, 'Nazir'),
                    ('Meegs', 1174, 'Miguel'),
                    ('Weegi', 7234, 'Ivan')]
        cursor.executemany("""INSERT INTO USERS
                                 ( USERNAME, DISCORD_ID, COMMON_NAME) 
                                  VALUES 
                                 (?, ?, ?)
                                 """, examples)


        conn.commit()

        ### Generate Valarant Table ###

        cursor = conn.cursor()
        # Create table - USERS
        cursor.execute('''CREATE TABLE VALORANT
                             ([USER_ID] INTEGER PRIMARY KEY ,[MEME] text)''') # set up a foreign key here eventually

        valorantExamples = [(1, "Valorant? You mean the not so faggot friendly stream?"),
                            (2, "You mean shotguns only, no Russian?"),
                            (3, "Valorant? You mean the game where you buy an OP or go 0-26?"),
                            (4, "Valorant? You mean the game where I die in the first 2 seconds of the game for \"information\""),
                            (5, "Valorant? You the game where my best ability is rubber banding?"),
                            (6, "Where'd you get that bike?")]
        cursor.executemany("""INSERT INTO VALORANT
                                         ( USER_ID, MEME) 
                                          VALUES 
                                         (?, ?)
                                         """, valorantExamples)

        conn.commit()




        return conn
    return sqlite3.connect('discordBotDB.db')
