import os
import discord
import requests
import json
import logging
import sys
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import aiohttp
import asyncio
import paramiko

# import subprocess

bot = commands.Bot(command_prefix=".", intents=discord.Intents.default(),
                   case_insensitive=True)

token = os.getenv('token')

logging.basicConfig(filename='console.log',
                    level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


@bot.event
async def on_ready():
    # Marks bot as running
    logging.info('Bot is successfully up and running.')


@bot.event
async def on_message(message):
    timings = bot.get_cog('Timings')
    try:
        await timings.analyze_timings(message)
    except BaseException as error:
        await message.reply(f"An unexpected error occurred: ${error}")


@bot.command()
async def ping(ctx):
    await ctx.send(f'Public bot ping is {round(bot.latency * 1000)}ms')

for file_name in os.listdir('./cogs'):
    if file_name.endswith('_public.py'):
        logging.info(f'Loading extension cogs.{file_name[:-3]}')
        bot.load_extension(f'cogs.{file_name[:-3]}')

bot.run(token)

# full name: message.author.name + "#" + str(message.author.discriminator) + " (" + str(message.author.id) + ")"
