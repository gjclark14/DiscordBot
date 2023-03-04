import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

# https://realpython.com/how-to-make-a-discord-bot-python/

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Members intent is privileged and has to be set in the developer portal
intents = discord.Intents(
    messages=True,
    message_content=True,
    members=True,
    guilds=True,
)

bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    print(f'Recognized that {member.name} joined.')
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}! uwu :3\n'
    )


@bot.command(name='69')
async def sixty_nine(ctx):
    print('!69 encountered')
    response = 'nice'
    await ctx.send(response)


@bot.command(name='whosucks?', help='Tells you who the biggest sucka in the discord is')
async def who_sucks(ctx):
    guild = ctx.guild
    member = random.choice(guild.members)
    if member == bot.user:
        response = f'{member} sucks!\noh wait...'
    else:
        response = f'{member.name} sucks!'
    await ctx.send(response)


@bot.command(name='rolldice', help='Simulates rolling dice.')
async def roll(
        ctx,
        number_of_dice: int = commands.parameter(description='Number of dice'),
        number_of_sides: int = commands.parameter(description='Number of sides per dice')
):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]

    await ctx.send(', '.join(dice))


@bot.command(name='createchannel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='normies'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You don't have the correct role for this command")


bot.run(TOKEN)
