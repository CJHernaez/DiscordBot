import discord
import sqlite3
import logging
import os.path
from os import path

from DBHelper import DBHelper
from MessageHelper import MessageHelper
from UserHelper import UserHelper
from Valarant.ValarantHelper import ValarantHelper

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

conn = GenerateDB()
dbHelper = DBHelper(conn)
valarantHelper = ValarantHelper(conn)
userFile = open("userToken.txt","r") #enter the discord auth here.

users = {}
users = dbHelper.refreshUsers()

valarants = {}
valarants = valarantHelper.refreshValarants()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def DBTest(message):
    tokenizedMessage = message.content.split(' ')
    if tokenizedMessage[1] == 'view': # if the second word is view
        if (len(tokenizedMessage) < 3):
            return message.channel.send('Must Include Table Name')
        return message.channel.send(dbHelper.getAll(tokenizedMessage[2]))
    if tokenizedMessage[1] == 'addUser': # if the second word is view
        return message.channel.send(dbHelper.addUser(tokenizedMessage[2], tokenizedMessage[3]))

    if tokenizedMessage[1] == 'refreshUsers': # if the second word is view
        return message.channel.send(dbHelper.refreshUsers(users))

    if tokenizedMessage[1] == 'getUsers':  # if the second word is view
        return message.channel.send(dbHelper.getUsers(users))

    return message.channel.send('')


@client.event
async def on_message(message): # update this to a database
    if 'db' in message.content.split(' ')[0] and 'Prophecies#9660' == str(message.author):
        await DBTest(message)
    if 'valarant' in message.content.split(' ')[0]:
        await ValarentMessage(message)
    if 'message' in message.content.split(' ')[0]:
        await message.channel.send(messageHelper.getDiscordTagByMessage(message))
    if message.author == client.user:
        return
    if ('hello') in message.content:
        await message.channel.send('Hello, {0.author}!'.format(message))


messageHelper = MessageHelper(users)
userHelper = UserHelper()

async def ValarentMessage(message):
    discordTag = messageHelper.getDiscordTagByMessage(message)
    userID = userHelper.getUserIdByDiscordTag(discordTag, users)
    await message.channel.send(valarantHelper.getMemeByUserId(userID, valarants))
    return



client.run(userFile.read())