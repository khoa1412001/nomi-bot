from discord.ext import commands
import discord
import logging

token = 'NTI5Nzc0NjYyMDcxMjIyMjcy.XT3Chg.w-vPKWvpXTIW4XTMwLGyPnzXlcY'
prefix_char = '#'
bot = commands.Bot(
  command_prefix = prefix_char
)
log = {}

def init_log():
  logger = logging.getLogger('discord')
  logger.setLevel(logging.DEBUG)
  handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
  handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
  logger.addHandler(handler)


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

@bot.command
async def ping(ctx):
  ctx.send('pong')

init_log()
bot.load_extension('servers.nomi-host-data')
bot.load_extension('servers.umbra')
bot.run(token)