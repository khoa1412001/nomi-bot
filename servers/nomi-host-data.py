from discord.ext import commands
import platform, discord, datetime, pytz, random, asyncio
from modules import talking_nomi

class Nomi_Host_Data(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.use_channels = {}

  def find_channels(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'nomi-host-data'):
        channels = guild.channels
        for channel in channels:
          self.use_channels[channel.name] = channel
        break

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_channels()
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
    str = (
      '```[INFO]```\n'
      f'Logged as: {self.bot.user.name}#{self.bot.user.discriminator}\n'
      f'Python: {platform.python_version()}\n'
      f'Discord py: {discord.__version__}\n'
      f'Built date: {now}\n'
    )
    await self.use_channels['logs'].send(str)

  @commands.Cog.listener()
  async def on_message(self, message):
    if (message.author.id != self.bot.user.id):
      if (len(message.mentions) == 1) and (self.bot.user.mentioned_in(message)):
        async with message.channel.typing():
          delay_time = random.choice(range(10, 30)) / 100.0
          await asyncio.sleep(delay_time)
          rely = talking_nomi.parse_sentence(message.content)
          if (rely == 'not found response'):
            req, res, cou = talking_nomi.return_error()
            str = (
              '[ERROR]\n'
              f'request: {req}\n'
              f'count:\n {cou}\n'
            )
            await self.use_channels['no-response'].send(str)
          else:
            await message.channel.send(f'{message.author.mention} {rely}')
      if 'messages' in self.use_channels:
        str = (
          '```[MESSAGE]```\n'
          f'[{message.guild}][#{message.channel}]\n'
          f'{message.author}: {message.content}\n'
        )
        await self.use_channels['messages'].send(str)


def setup(bot):
  bot.add_cog(Nomi_Host_Data(bot))
