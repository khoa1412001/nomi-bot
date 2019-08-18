from discord.ext import commands
import discord, os
from modules import nomi_water_pack, talking_nomi

token = os.getenv('token')
prefix_char = '#'
bot = commands.Bot(
  command_prefix = prefix_char
)

@bot.event
async def on_ready():
  await bot.change_presence(
    activity = discord.Activity(
      type = discord.ActivityType.watching,
      name = 'NTR hentai'
    ),
    status = discord.Status.do_not_disturb
  )

@bot.event
async def on_message(message):
  if (message.content.startswith(prefix_char)):
    await bot.process_commands(message)

talking_nomi.prepare()
nomi_water_pack.prepare()
bot.load_extension('servers.nomi-host-data')
bot.load_extension('servers.umbra')
bot.load_extension('servers.asteria')
bot.run(token)
