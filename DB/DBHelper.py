import logging
import sqlite3
from os import path

def GenerateDB():
    logging.info("DB not found. Generating new DB")
    if not path.exists("discordBotDB.db"):
        conn = sqlite3.connect('discordBotDB.db') # generate the db.
        cursor = conn.cursor()
        # Create table - USERS
        cursor.execute('''CREATE TABLE USERS
                     ([ID] INTEGER PRIMARY KEY AUTOINCREMENT,[USERNAME] text, [DISCORD_ID] integer, [COMMON_NAME] text)''')


        examples = [('procrastinise', 2594, 'Jarren'), ('Prophecies', 9660, 'CJ'), ('AirWick', 9172, 'EJ')]
        cursor.executemany("""INSERT INTO USERS
                                 ( USERNAME, DISCORD_ID, COMMON_NAME) 
                                  VALUES 
                                 (?, ?, ?)
                                 """, examples)


        conn.commit()

        ### Generate Valarant Table ###

        cursor = conn.cursor()
        # Create table - USERS
        cursor.execute('''CREATE TABLE VALARANT
                             ([USER_ID] INTEGER PRIMARY KEY ,[MEME] text)''') # set up a foreign key here eventually

        valarantExamples = [(1, "Jarren's Meme"), (2, "CJ's Meme"), (3, "EJ's Meme")]
        cursor.executemany("""INSERT INTO VALARANT
                                         ( USER_ID, MEME) 
                                          VALUES 
                                         (?, ?)
                                         """, valarantExamples)

        conn.commit()




        return conn
    return sqlite3.connect('discordBotDB.db')
