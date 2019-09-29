from discord.ext import commands
import discord

class Asteria(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.my_channels = {}

  def find_objects(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'Asteria'):
        channels = guild.channels
        for channel in channels:
          self.my_channels[channel.name] = channel
        break

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_objects()

def setup(bot):
  bot.add_cog(Asteria(bot))
