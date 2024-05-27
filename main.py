import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix=["!"], intents=intents)

cogs = ('cogs.MemeCog', 'cogs.FeedsCog')


@client.event
async def setup_hook():
    for cog in cogs:
        await client.load_extension(cog)


client.run(DISCORD_TOKEN)
