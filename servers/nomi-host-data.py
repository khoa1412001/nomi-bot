from discord.ext import commands
import platform, discord, datetime, pytz, random, asyncio
from modules import chitchat

class NomiHostData(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.my_guild = None
    self.my_channels = {}

  def find_channels(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'nomi-host-data'):
        self.my_guild = guild
        channels = guild.channels
        for channel in channels:
          self.my_channels[channel.name] = channel
        break

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_channels()
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
    str = (
      '```[INFO]```'
      f'Logged as: {self.bot.user.name}#{self.bot.user.discriminator}\n'
      f'OS: {platform.platform()}\n'
      f'Python: {platform.python_version()}\n'
      f'Discord py: {discord.__version__}\n'
      f'Built date: {now}\n'
    )
    await self.my_channels['logs'].send(str)

  @commands.Cog.listener()
  async def on_message(self, message):
    if (message.author.id != self.bot.user.id):
      if 'messages' in self.my_channels:
        str = (
          '```[MESSAGE]```'
          f'[{message.guild}][#{message.channel}]\n'
          f'{message.author}: {message.content}\n'
        )
        await self.my_channels['messages'].send(str)

def setup(bot):
  bot.add_cog(NomiHostData(bot))
