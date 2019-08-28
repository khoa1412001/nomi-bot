from discord.ext import commands
import discord, os, random, asyncio
from modules import water_pack, chitchat, paylak

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
      name = 'NTR hentai.'
    ),
    status = discord.Status.do_not_disturb
  )

@bot.event
async def on_message(message):
  if (message.author.id != bot.user.id):
    if (len(message.mentions) == 1) and (bot.user.mentioned_in(message)):
      async with message.channel.typing():
        delay_time = random.choice(range(45, 100)) / 100.0
        await asyncio.sleep(delay_time)
      logic = chitchat.Logic(message.content)
      req, res, cou = logic.request, logic.response, logic.counts
      if (res == 'not found response'):
        str = (
          '```[ERROR]```'
          f'No response found.\n'
          f'request: {req}\n'
        )
        cog = bot.get_cog('NomiHostData')
        await cog.my_channels['talking'].send(str)
      else:
        await message.channel.send(f'{message.author.mention} {res}')
        str = (
          '```[DEBUG]```'
          f'request: {req}\n'
          f'response: {res}\n'
          f'counts: {cou}\n'
        )
        cog = bot.get_cog('NomiHostData')
        await cog.my_channels['talking'].send(str)
  if (message.content.startswith(prefix_char)):
    await bot.process_commands(message)


chitchat.prepare()
water_pack.prepare()
paylak.prepare()
bot.load_extension('servers.nomi-host-data')
bot.load_extension('servers.umbra')
bot.load_extension('servers.asteria')
bot.run(token)
