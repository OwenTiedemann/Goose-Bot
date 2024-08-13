import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
NEWS_CHANNEL_ID = os.environ['NEWS_CHANNEL_ID']

client = commands.Bot(command_prefix=["!"], intents=intents)
client.NEWS_CHANNEL_ID = NEWS_CHANNEL_ID

cogs = ('cogs.MemeCog', 'cogs.FeedsCog')

COUNT = 0


@client.event
async def on_message(message):
    global COUNT
    if message.author == client.user:
        return

    random_value = random.randrange(1, 100)
    print(random_value, COUNT)

    if 1 == random_value:
        await message.reply('What in the fuck is wrong with you, you sick fuck!')
    else:
        COUNT = COUNT + 1


@client.event
async def setup_hook():
    for cog in cogs:
        await client.load_extension(cog)


client.run(DISCORD_TOKEN)
