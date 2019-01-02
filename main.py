import os,datetime,random,asyncio
import discord,utils
from discord.ext import commands as cmds

prefix_char=utils.get_object('prefix_char')
bot=cmds.Bot(command_prefix=prefix_char)
bot.remove_command('help')
    
async def init_activity():
  activity=discord.Activity(name='NTR hentai.',type=discord.ActivityType.watching)
  await bot.change_presence(activity=activity)

async def log(content,use_time=True):
  print(content)
  channel=utils.get_object('log_channel')
  if channel==None:
    print('Error: Not found log channel.')
    return
  if use_time:
    await channel.send(f'[{str(datetime.datetime.now())}]\n{content}')
  else:
    await channel.send(content)

@bot.event
async def on_ready():
  await init_activity()
  utils.set_object('log_channel', bot.get_channel(utils.get_object('log_channel_id')))
  msg=(
    '```'
    f'version: {str(datetime.datetime.now())}\n'
    f'discord.py: {discord.__version__}\n'
    '```'
  )
  await log(msg,use_time=False)

@bot.event
async def on_message(message):
  guild, channel, sender, msg=message.guild, message.channel, message.author, message. content
  if sender.id!=bot.user.id:
    if len(message.mentions)==1 and bot.user.mentioned_in(message):
      async with channel.typing():
        delay_time=int(random.choice(range(40, 100))) / 100.0
        #rely=utils.to_emoji(logic.req_to_res(msg))
        await asyncio.sleep(delay_time)
        #await channel.send(f'{sender.mention} {rely}')
    if channel.id!=utils.objects['log_channel_id']:
      await log(f'[{guild.name.upper()}][#{channel.name}]{sender.name}#{sender.discriminator}\n{msg}')
  if msg.startswith(prefix_char):
    await bot.process_commands(message)
    
bot.run(os.getenv('token'))
