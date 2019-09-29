from discord.ext import commands
import os, discord, asyncio, datetime, pytz
from modules import water_pack

class Umbra(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.my_guild = None
    self.my_channels = {}
    self.last_online = {}

  def find_objects(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'Umbra'):
        self.my_guild = guild
        channels = guild.channels
        for channel in channels:
          self.my_channels[channel.name] = channel
        break

  async def send_packs(self):
    await self.bot.wait_until_ready()
    while (True):
      image_url = water_pack.o.get_random(['hasunoai'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['cosplay'].send(embed = embed)

      image_url = water_pack.o.get_random(['hanime'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['qbu-nsfw'].send(embed = embed)

      image_url = water_pack.o.get_random(['ulzzang_face', 'ulzzang__girlz'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['ulzzang'].send(embed = embed)

      image_url = water_pack.o.get_random(['favorite_asian_girls', 'instababes.asian'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['asian'].send(embed = embed)

      image_url = water_pack.o.get_random(['vietnamesexybabe', 'vneseg', 'angels.in.vn', 'girl_xinh'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['cây-nhà-lá-vườn'].send(embed = embed)
      
      image_url = water_pack.o.get_random(['hoingamgaitay'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['not-for-qbu'].send(embed = embed)
      
      image_url = water_pack.o.get_random(['69pretty.official'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['mixed'].send(embed = embed)
      
      await asyncio.sleep(5400)
        
  @commands.Cog.listener()
  async def on_ready(self):
    self.find_objects()
    loop = asyncio.get_event_loop()
    loop.create_task(self.send_packs())
    loop.create_task(self.print_last_online())

def setup(bot):
  bot.add_cog(Umbra(bot))
