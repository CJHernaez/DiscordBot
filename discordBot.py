import discord

client = discord.Client()

f= open("userToken.txt","r")

users = {}
users['Jarren'] = 'procrastinise#2594'
users['CJ'] = 'Prophecies#9660'
users['EJ'] = 'AirWick#9172'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if 'valarant' in message.content.lower():
        if message.author.name in users['CJ']:
            await message.channel.send('shotguns only')
        if message.author.name in users['Jarren']:
            await message.channel.send('do it for the clip? I told you to say hi to your mom for me you cuck')
        if message.author.name in users['EJ']:
            await message.channel.send('EJ please by the operator ur a liability.')
    if message.author == client.user:
        return

    if ('hello') in message.content:
        await message.channel.send('Hello, {0.author}!'.format(message))

client.run(f.read())