from discord.ext import commands
import discord, random, asyncio
from modules import chitchat

class ChitChat(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.log_channel = None

  def find_objects(self):
    cog = self.bot.get_cog('NomiHostData')
    self.log_channel = cog.my_channels['chitchat']
 
  def log(self, text):
    if self.log_channel is not None:
      await self.log_channel.send(text)

  @commands.Cog.listener()
  async def on_ready(self):
    await asyncio.sleep(3)
    self.find_objects()

  @commands.Cog.listener()
  async def on_message(self, message):
    if (message.author.id != self.bot.user.id):
      if (len(message.mentions) == 1) and (self.bot.user.mentioned_in(message)):
        async with message.channel.typing():
          delay_time = random.choice(range(45, 100)) / 100.0
          await asyncio.sleep(delay_time)
        logic = chitchat.Logic(message.content)
        if not logic.response == 'not found response':
          await message.channel.send(f'{message.author.mention} {logic.response}')
        str = (
          '```[DEBUG]```'
          f'request: {logic.request}\n'
          f'response: {logic.response}\n'
          f'counts: {logic.counts}\n'
        )
        self.log(str)

def setup(bot):
  bot.add_cog(ChitChat(bot))
