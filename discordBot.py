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
from Valorant.ValorantHelper import ValorantHelper

client = discord.Client()


conn = GenerateDB()


userFile = open("userToken.txt","r")

#Configure User Helper
users = {}
userHelper = UserHelper(users, conn)
users = userHelper.refresh()

#Configure Message Helper
messageHelper = MessageHelper(users)

#Configure DB Helper
dbHelper = DBHelper(conn)
dbHelper.setUserHelper(userHelper)

#Configure valorant Repo and Helper
valorants = {}
valorantHelper = ValorantHelper(valorants, conn)
valorants = valorantHelper.refresh()
valorantHelper.setUserHelper(userHelper)
valorantHelper.setMessageHelper(messageHelper)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    tokenizedMessage = message.content.split(' ')
    if ([x for x in message.author.roles if x.name == "Dev"]): #dont touch this unless you know what you are doing - CJ 2020
        print('User is a dev')
        if 'db' in tokenizedMessage[0] :
            await dbHelper.getAllFromTable(message)
        if 'user' in tokenizedMessage[0]:
            await userHelper.Handle(message)
        if 'valorant' in tokenizedMessage[0]:
            await valorantHelper.Handle(message)
        if 'message' in tokenizedMessage[0]:
            await message.channel.send(messageHelper.getDiscordTagByMessage(message))
    else:
        if 'valorant' in message.content.lower():
            await message.channel.send(valorantHelper.getMemeByMessage(message))

    if ('hello') in message.content:
        await message.channel.send('Hello, {0.author}!'.format(message))





client.run(userFile.read())