'''

UCF Crimes: main.py
Written by Ethan Frakes

'''

import discord
from discord.ext import commands
import time
from datetime import date, timedelta
import asyncio
import json
from configparser import ConfigParser
from loadcrimes import crime_load
from sendcrimes import crime_send, list_locations

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix = '-')
client.remove_command('help')

main_config = ConfigParser()
main_config.read('config.ini')

@client.event
async def on_ready():
    print("CrimeBot is online!")
    await client.wait_until_ready()

    while not client.is_closed():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        if current_time == "00:04:30":
            crime_load()

        if current_time == "00:05:00":
            today = date.today()
            yesterday = (today - timedelta(days=1)).strftime("%m/%d/%y")
            await crime_send(client, yesterday, main_config.get("DISCORD", "CRIME_CHANNEL_ID"), main_config.get("DISCORD", "GMAPS_API_KEY"))

        await asyncio.sleep(1)

@client.event
async def on_message(message):
    print('User %s just sent this message in %s: %s' % (message.author, message.channel.name, message.content))

    if message.content.startswith('-loadcrimes'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        crime_load()
    
    elif message.content.startswith('-crimes'):
        str = message.content[8:]
        await crime_send(client, str, main_config.get("DISCORD", "CRIME_CHANNEL_ID"), main_config.get("DISCORD", "GMAPS_API_KEY"))

    elif message.content.startswith('-locations'):
        await list_locations(message)

client.run(main_config.get("DISCORD", "TOKEN"))