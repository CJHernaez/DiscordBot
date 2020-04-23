import discord
import sqlite3
import logging
import os.path
from os import path

from DB.DBHelper import GenerateDB
from DBHelper import DBHelper
from MessageHelper import MessageHelper
from Repositories.UserRepository import UserRepository
from UserHelper import UserHelper
from Valarant.ValarantHelper import ValarantHelper

client = discord.Client()


conn = GenerateDB()
dbHelper = DBHelper(conn)
valarantHelper = ValarantHelper(conn)
userFile = open("userToken.txt","r")

users = {}

messageHelper = MessageHelper(users)
userHelper = UserHelper(users, conn)

users = userHelper.refresh()

dbHelper.setUserHelper(userHelper)

valarants = {}
valarants = valarantHelper.refreshValarants()




@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message): # update this to a database
    tokenizedMessage = message.content.split(' ')
    if ([x for x in message.author.roles if x.name == "Dev"]):
        print('User is a dev')
        if 'db' in tokenizedMessage[0] and 'Prophecies#9660' == str(message.author):
            await dbHelper.getAllFromTable(message)
        if 'user' in tokenizedMessage[0]:
            await userHelper.Handle(message)
        if 'valarant' in tokenizedMessage[0]:
            await ValarentMessage(message)
        if 'message' in tokenizedMessage[0]:
            await message.channel.send(messageHelper.getDiscordTagByMessage(message))
        if message.author == client.user:
            return
    if ('hello') in message.content:
        await message.channel.send('Hello, {0.author}!'.format(message))


async def ValarentMessage(message):
    discordTag = messageHelper.getDiscordTagByMessage(message)
    userID = userHelper.getUserIdByDiscordTag(discordTag, users)
    await message.channel.send(valarantHelper.getMemeByUserId(userID, valarants))
    return


client.run(userFile.read())