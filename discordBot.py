import discord
import sqlite3
import logging
import os.path
from os import path

from DBHelper import DBHelper

client = discord.Client()

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
        print("DB with new values generated.")
        conn.commit()
        return conn
    return sqlite3.connect('discordBotDB.db')

conn = GenerateDB()
dbHelper = DBHelper(conn)


userFile = open("userToken.txt","r") #enter the discord auth here.

users = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def DBTest(message):
    tokenizedMessage = message.content.split(' ')
    if tokenizedMessage[1] == 'view': # if the second word is view
        if (len(tokenizedMessage) < 3):
            return message.channel.send('Must Include Table Name')
        return message.channel.send(dbHelper.getAll(tokenizedMessage[2]))
    if tokenizedMessage[1] == 'add': # if the second word is view
        return message.channel.send(dbHelper.addUser(tokenizedMessage[2], tokenizedMessage[3]))


@client.event
async def on_message(message): # update this to a database
    if 'db' in message.content.split(' ')[0] and 'Prophecies#9660' == str(message.author):
        await DBTest(message)
    if 'valarant' in message.content.lower():
        await ValarentMessage(message)
    if message.author == client.user:
        return
    if ('hello') in message.content:
        await message.channel.send('Hello, {0.author}!'.format(message))

async def ValarentMessage(message):
    if message.author.name in users['CJ']:
        await message.channel.send('shotguns only')
    if message.author.name in users['Jarren']:
        await message.channel.send('do it for the clip? I told you to say hi to your mom for me you cuck')
    if message.author.name in users['EJ']:
        await message.channel.send('EJ please by the operator ur a liability.')


client.run(userFile.read())