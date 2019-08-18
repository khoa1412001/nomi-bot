from discord.ext import commands
import platform, discord, datetime, pytz, random, asyncio
from modules import talking_nomi

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
      f'Python: {platform.python_version()}\n'
      f'Discord py: {discord.__version__}\n'
      f'Built date: {now}\n'
    )
    await self.my_channels['logs'].send(str)

  @commands.Cog.listener()
  async def on_message(self, message):
    if (message.author.id != self.bot.user.id):
      if (len(message.mentions) == 1) and (self.bot.user.mentioned_in(message)):
        async with message.channel.typing():
          delay_time = random.choice(range(45, 100)) / 100.0
          await asyncio.sleep(delay_time)
        logic = talking_nomi.Logic(message.content)
        req, res, cou = logic.request, logic.response, logic.counts
        if (res == 'not found response'):
          str = (
            '```[ERROR]```'
            f'No response found.\n',
            f'request: {req}\n'
          )
          await self.my_channels['talking'].send(str)
        else:
          await message.channel.send(f'{message.author.mention} {res}')
          str = (
            '```[DEBUG]```'
            f'request: {req}\n',
            f'response: {res}\n',
            f'counts: {cou}\n'
          )
          await self.my_channels['talking'].send(str)
      if 'messages' in self.my_channels:
        str = (
          '```[MESSAGE]```'
          f'[{message.guild}][#{message.channel}]\n'
          f'{message.author}: {message.content}\n'
        )
        await self.my_channels['messages'].send(str)


def setup(bot):
  bot.add_cog(NomiHostData(bot))
