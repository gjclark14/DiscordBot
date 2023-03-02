import os

import discord
from dotenv import load_dotenv

# https://realpython.com/how-to-make-a-discord-bot-python/

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Members intent is privileged and has to be set in the developer portal
intents = discord.Intents(messages=True, message_content=True, members=True)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    print(f'Recognized that {member.name} joined.')
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}! uwu :3\n'
    )


@client.event
async def on_message(message):
    # This is to ensure that the bot is not replying to itself
    if message.author == client.user:
        print(f'{message.author} == {client.user}')
        return

    print(f'Read message: {message.content}')
    if message.content == '69':
        response = 'nice'
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)
